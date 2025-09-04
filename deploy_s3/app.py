# app.py — Streamlit UI for RiceAI with S3-backed chat list + local materialization
# Titles are human-friendly (no thread IDs shown anywhere).

import os
import json
import uuid
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

# Import compiled graph + S3 helpers from final.py
from final import (
    graph,
    stream_answer,
    append_chat_event,
    backup_sqlite_now,
    ensure_thread_local_copy,
    s3,                       # boto3 client configured in final.py
    AWS_BUCKET,
    S3_PREFIX_CHATS,
    CHAT_DIR as EVENTS_DIR,   # where the JSONL event logs live locally (NEW/chats)
)

# ---- Optional imports from final.py (metadata helpers). Fallbacks if not present. ----
HAS_META = True
try:
    from final import read_meta, write_meta, list_chats_with_titles, rename_chat  # type: ignore
except Exception:
    HAS_META = False
    def read_meta(thread_id: str) -> Dict[str, Any]: return {}
    def write_meta(thread_id: str, meta: Dict[str, Any]) -> None: ...
    def list_chats_with_titles() -> List[Dict[str, Any]]: return []
    def rename_chat(thread_id: str, new_title: str) -> None: ...

# ------------- Env -------------
load_dotenv()

# ------------- Local UI storage (for titles + visible transcript) -------------
# NOTE: This is ONLY for Streamlit rendering. Source of truth for events is JSONL in NEW/chats (and S3).
CHAT_DIR = Path("./chats")
CHAT_DIR.mkdir(exist_ok=True)

def _thread_path(thread_id: str) -> Path:
    return CHAT_DIR / f"{thread_id}.json"

def load_thread(thread_id: str):
    p = _thread_path(thread_id)
    if not p.exists():
        return {"id": thread_id, "title": "New chat", "messages": []}
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_thread(thread: dict):
    p = _thread_path(thread["id"])
    with p.open("w", encoding="utf-8") as f:
        json.dump(thread, f, ensure_ascii=False, indent=2)

# ---------- Event log helpers ----------
def _event_path(thread_id: str) -> Path:
    """Local path to the JSONL event log created by final.append_chat_event()."""
    return EVENTS_DIR / f"{thread_id}.jsonl"

def _s3_chat_key(thread_id: str) -> str:
    prefix = (S3_PREFIX_CHATS or "").strip("/")
    return f"{prefix}/{thread_id}.jsonl" if prefix else f"{thread_id}.jsonl"

def _summarize(text: str, n: int = 48) -> str:
    text = " ".join((text or "").split())
    text = re.sub(r"[`*_#\[\]()<>{}|\\]", "", text).strip()
    return (text[:n] + "…") if len(text) > n else text

def _first_user_prompt_from_events(thread_id: str) -> Optional[str]:
    p = _event_path(thread_id)
    if not p.exists():
        return None
    try:
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                role = (obj.get("role") or obj.get("type") or "").lower()
                if role in ("user", "human"):
                    return (obj.get("content") or "").strip()
    except Exception:
        return None

def _created_at_from_events(thread_id: str) -> Optional[datetime]:
    p = _event_path(thread_id)
    if not p.exists():
        return None
    try:
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                ts = obj.get("ts")
                if isinstance(ts, int):
                    return datetime.fromtimestamp(ts, tz=timezone.utc)
    except Exception:
        return None

def _title_from_meta(thread_id: str) -> Optional[str]:
    if not HAS_META:
        return None
    try:
        meta = read_meta(thread_id) or {}
        t = (meta.get("title") or "").strip()
        return t or None
    except Exception:
        return None

# strip trailing " · ab12cd" patterns if they were stored previously
_HEX6 = re.compile(r"\s*[·\-–]\s*[0-9a-f]{6}\s*$", re.I)
def _sanitize_title(t: str) -> str:
    if not t:
        return "New chat"
    return _HEX6.sub("", t).strip() or "New chat"

def derive_title(thread_id: str) -> str:
    """
    Priority:
    1) S3 meta title (if final.py supports it)
    2) existing local UI title (./chats/<id>.json)
    3) 'First user message' summary
    4) Date-only fallback (no thread id)
    """
    # (1) meta
    meta_title = _title_from_meta(thread_id)
    if meta_title:
        return _sanitize_title(meta_title)

    # (2) local UI
    ui = _thread_path(thread_id)
    if ui.exists():
        try:
            with ui.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("title"):
                return _sanitize_title(data["title"])
        except Exception:
            pass

    # (3) first user message
    first = _first_user_prompt_from_events(thread_id)
    if first:
        return _sanitize_title(_summarize(first))

    # (4) date-only fallback
    dt = _created_at_from_events(thread_id)
    d = dt.astimezone().strftime("%Y-%m-%d") if dt else "New chat"
    return d

# ---------- S3-aware index + materialization ----------
def load_threads_index():
    """
    Prefer server-side title index if available (final.list_chats_with_titles).
    Otherwise, list S3 objects and derive titles on the fly.
    """
    # Preferred path: use final.py's meta-aware indexer
    if HAS_META:
        try:
            items = list_chats_with_titles()
            if items:
                out = []
                for it in items:
                    tid = it.get("thread_id") or it.get("id")
                    if not tid:
                        continue
                    title = _sanitize_title(it.get("title") or "New chat")
                    updated = it.get("last_msg_at") or it.get("updated") or 0
                    out.append({"id": tid, "title": title, "updated": updated})
                out.sort(key=lambda x: x["updated"], reverse=True)
                if out:
                    return out
        except Exception:
            pass

    # Fallback: list S3 objects under prefix and derive titles from events/meta
    items_by_id: Dict[str, Any] = {}
    try:
        prefix = (S3_PREFIX_CHATS or "").strip("/")
        if prefix:
            prefix += "/"

        token = None
        while True:
            kwargs = dict(Bucket=AWS_BUCKET, Prefix=prefix, MaxKeys=1000)
            if token:
                kwargs["ContinuationToken"] = token
            resp = s3.list_objects_v2(**kwargs)

            for obj in resp.get("Contents", []):
                key = obj["Key"]
                if not key.endswith(".jsonl"):
                    continue
                tid = Path(key).stem

                # Ensure event log exists locally so we can read first prompt / timestamps
                try:
                    ensure_thread_local_copy(tid)
                except Exception:
                    pass

                title = _sanitize_title(derive_title(tid))
                items_by_id[tid] = {
                    "id": tid,
                    "title": title,
                    "updated": obj["LastModified"].timestamp(),
                }

            if not resp.get("IsTruncated"):
                break
            token = resp.get("NextContinuationToken")

        if items_by_id:
            return sorted(items_by_id.values(), key=lambda x: x["updated"], reverse=True)

    except Exception:
        pass

    # Local fallback list (no S3)
    for p in sorted(CHAT_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            tid = data.get("id", p.stem)
            items_by_id[tid] = {
                "id": tid,
                "title": _sanitize_title(data.get("title") or derive_title(tid)),
                "updated": p.stat().st_mtime,
            }
        except Exception:
            continue

    return sorted(items_by_id.values(), key=lambda x: x["updated"], reverse=True)

def materialize_ui_from_s3_if_missing(thread_id: str):
    """
    If ./chats/<id>.json is missing, rebuild it from the JSONL event log.
    """
    ui_path = _thread_path(thread_id)
    if ui_path.exists():
        return

    # Ensure event log exists locally (download from S3 if needed)
    ensure_thread_local_copy(thread_id)

    ev_path = _event_path(thread_id)
    if not ev_path.exists():
        return  # nothing to render

    messages = []
    with ev_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except Exception:
                continue
            role = (evt.get("role") or evt.get("type") or "").lower()
            content = evt.get("content", "")
            if role in ("user", "human"):
                messages.append({"type": "human", "content": content})
            elif role in ("assistant", "ai"):
                messages.append({"type": "ai", "content": content})

    thread = {"id": thread_id, "title": derive_title(thread_id), "messages": messages}
    save_thread(thread)

# ---------- New / Delete helpers ----------
def new_thread():
    """
    Create a brand-new thread locally AND seed an S3 event log immediately,
    so the chat appears in your bucket before the first user message.
    """
    tid = str(uuid.uuid4())
    thread = {"id": tid, "title": "New chat", "messages": []}  # no id in title
    save_thread(thread)

    # Seed S3 JSONL right away (don’t block UI if offline)
    try:
        ensure_thread_local_copy(tid)               # local placeholder if needed
        append_chat_event(tid, "system", "created") # creates & uploads <prefix>/<id>.jsonl
    except Exception:
        pass

    return tid

def delete_thread(thread_id: str):
    """
    Delete local UI transcript, local JSONL, and the backing S3 JSONL.
    """
    # delete local UI transcript
    p = _thread_path(thread_id)
    if p.exists():
        p.unlink(missing_ok=True)

    # delete local event log
    ev = _event_path(thread_id)
    if ev.exists():
        ev.unlink(missing_ok=True)

    # delete from S3
    try:
        s3.delete_object(Bucket=AWS_BUCKET, Key=_s3_chat_key(thread_id))
        # best-effort: remove meta if present
        if HAS_META:
            prefix = (S3_PREFIX_CHATS or "").strip("/")
            meta_key = f"{prefix}/{thread_id}.meta.json" if prefix else f"{thread_id}.meta.json"
            s3.delete_object(Bucket=AWS_BUCKET, Key=meta_key)
    except Exception:
        pass

# ---------- Rendering ----------
def render_message(msg: BaseMessage):
    if isinstance(msg, HumanMessage):
        st.chat_message("user").markdown(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").markdown(msg.content)
    else:
        st.chat_message("assistant").markdown(f"_({msg.__class__.__name__})_ {msg.content}")

# ------------- Streamlit state -------------
if "current_thread" not in st.session_state:
    existing = load_threads_index()
    st.session_state.current_thread = existing[0]["id"] if existing else new_thread()

if "rename_buffer" not in st.session_state:
    st.session_state.rename_buffer = ""

# ---------- Sidebar ----------
st.sidebar.title("RiceAI Chats")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.current_thread = new_thread()
    st.rerun()

threads = load_threads_index()
if not threads:
    st.sidebar.info("No chats yet. Start a new one!")
else:
    ids = [t["id"] for t in threads]
    titles = [t["title"] for t in threads]

    # current selection
    idx = ids.index(st.session_state.current_thread) if st.session_state.current_thread in ids else 0

    # Number newest→oldest (newest has biggest number)
    total = len(ids)

    def label_with_number(i: int) -> str:
        title = titles[i]
        title = (title[:40] + "…") if len(title) > 40 else title
        return f"Chat {total - i} · {title}"   # no id here

    choice = st.sidebar.selectbox(
        "Open chat",
        options=list(range(total)),
        format_func=label_with_number,
        index=idx,
    )
    st.session_state.current_thread = ids[choice]

    with st.sidebar.expander("Manage chat"):
        current_meta = next((t for t in threads if t["id"] == st.session_state.current_thread), None)
        if current_meta:
            st.text_input("Title", key="rename_buffer", value=current_meta["title"])
            col1, col2 = st.columns(2)
            if col1.button("Save Title", use_container_width=True):
                # persist to S3 meta if available
                if HAS_META:
                    try:
                        rename_chat(st.session_state.current_thread, _sanitize_title(st.session_state.rename_buffer.strip()))
                    except Exception:
                        pass
                # always persist to local UI JSON for fast rendering
                thread = load_thread(st.session_state.current_thread)
                thread["title"] = _sanitize_title(st.session_state.rename_buffer.strip()) or thread["title"]
                save_thread(thread)
                st.success("Renamed.")
                st.rerun()
            if col2.button("Delete Chat", type="primary", use_container_width=True):
                delete_thread(st.session_state.current_thread)
                left = load_threads_index()
                st.session_state.current_thread = left[0]["id"] if left else new_thread()
                st.rerun()

st.sidebar.divider()
streaming_ui = st.sidebar.toggle("Stream answer", value=False)
st.sidebar.caption(f"Bucket: {AWS_BUCKET} • Prefix: {S3_PREFIX_CHATS or '(root)'}")

# ------------- Main area -------------
current_id = st.session_state.current_thread

# Ensure we have a local UI transcript built from the S3/JSONL log
materialize_ui_from_s3_if_missing(current_id)

thread = load_thread(current_id)
# show a clean, readable title (no thread id anywhere)
st.title(_sanitize_title(thread.get("title") or derive_title(current_id)))

for m in thread["messages"]:
    role = m.get("type")
    content = m.get("content", "")
    msg_obj = HumanMessage(content=content) if role == "human" else AIMessage(content=content)
    render_message(msg_obj)

prompt = st.chat_input("Ask about rice farming, AWD, fertilizer, IPM…")

if prompt:
    # 1) Show + persist user message (write-through to S3 event log)
    st.chat_message("user").markdown(prompt)
    append_chat_event(current_id, "user", prompt)

    if streaming_ui:
        # 2a) Streaming path
        st_placeholder = st.chat_message("assistant")
        with st_placeholder:
            full = st.write_stream(stream_answer(prompt, current_id))
        ai_text = full if isinstance(full, str) else "".join(full or [])
        append_chat_event(current_id, "assistant", ai_text)
        backup_sqlite_now()
    else:
        # 2b) Non-streaming path
        input_data = {"question": HumanMessage(content=prompt)}
        result = graph.invoke(input=input_data, config={"configurable": {"thread_id": current_id}})
        ai_text = "No response."
        if isinstance(result, dict) and "messages" in result:
            replies = [m for m in result["messages"] if isinstance(m, AIMessage)]
            if replies:
                ai_text = replies[-1].content
        st.chat_message("assistant").markdown(ai_text)
        append_chat_event(current_id, "assistant", ai_text)
        backup_sqlite_now()

    # 3) Update local visible transcript for UI (title may be created from first user line)
    thread["messages"].append({"type": "human", "content": prompt})
    thread["messages"].append({"type": "ai", "content": ai_text})
    # Update the visible title from meta or events if it just got created server-side
    try:
        new_title = _sanitize_title(derive_title(current_id))
        if new_title and new_title != thread.get("title"):
            thread["title"] = new_title
    except Exception:
        pass
    save_thread(thread)
