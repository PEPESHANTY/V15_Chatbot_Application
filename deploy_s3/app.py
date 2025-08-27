# app.py — Streamlit UI for RiceAI with S3 write-through logging

import os, json, uuid
from pathlib import Path

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
)

# ------------- Env -------------
load_dotenv()

# ------------- Local UI storage (for titles + visible transcript) -------------
CHAT_DIR = Path("./chats")
CHAT_DIR.mkdir(exist_ok=True)

def _thread_path(thread_id: str) -> Path:
    return CHAT_DIR / f"{thread_id}.json"

def load_threads_index():
    items = []
    for p in sorted(CHAT_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            title = data.get("title") or f"Chat {p.stem[:8]}"
            items.append({"id": data.get("id", p.stem), "title": title, "updated": p.stat().st_mtime})
        except Exception:
            continue
    return items

def load_thread(thread_id: str):
    p = _thread_path(thread_id)
    if not p.exists():
        return {"id": thread_id, "title": f"Chat {thread_id[:8]}", "messages": []}
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_thread(thread: dict):
    p = _thread_path(thread["id"])
    with p.open("w", encoding="utf-8") as f:
        json.dump(thread, f, ensure_ascii=False, indent=2)

def _extract_chat_numbers(threads_index):
    nums = []
    for t in threads_index:
        title = t.get("title", "")
        if title.startswith("Chat "):
            try:
                nums.append(int(title.split(" ")[1]))
            except Exception:
                pass
    return nums

def get_next_chat_number():
    existing = load_threads_index()
    nums = _extract_chat_numbers(existing)
    return (max(nums) + 1) if nums else 1

def new_thread():
    tid = str(uuid.uuid4())
    chat_num = get_next_chat_number()
    thread = {"id": tid, "title": f"Chat {chat_num}", "messages": []}
    save_thread(thread)
    # ensure S3-side file is pulled (no-op if new)
    ensure_thread_local_copy(tid)
    return tid

def delete_thread(thread_id: str):
    p = _thread_path(thread_id)
    if p.exists():
        p.unlink()

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

# ------------- Sidebar -------------
st.sidebar.title("RiceAI Chats")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.current_thread = new_thread()
    st.rerun()

threads = load_threads_index()
if not threads:
    st.sidebar.info("No chats yet. Start a new one!")
else:
    ids = [t["id"] for t in threads]
    labels = [t["title"] for t in threads]
    idx = ids.index(st.session_state.current_thread) if st.session_state.current_thread in ids else 0
    choice = st.sidebar.selectbox("Open chat", options=list(range(len(ids))), format_func=lambda i: labels[i], index=idx)
    st.session_state.current_thread = ids[choice]

    with st.sidebar.expander("Manage chat"):
        current_meta = next((t for t in threads if t["id"] == st.session_state.current_thread), None)
        if current_meta:
            st.text_input("Title", key="rename_buffer", value=current_meta["title"])
            col1, col2 = st.columns(2)
            if col1.button("Save Title", use_container_width=True):
                thread = load_thread(st.session_state.current_thread)
                thread["title"] = st.session_state.rename_buffer.strip() or thread["title"]
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

# ------------- Main area -------------
current_id = st.session_state.current_thread
# Make sure S3 chat jsonl exists locally for this thread (resume across machines)
ensure_thread_local_copy(current_id)

thread = load_thread(current_id)
st.title(thread.get("title", "Chat"))

for m in thread["messages"]:
    role = m.get("type")
    content = m.get("content", "")
    msg_obj = HumanMessage(content=content) if role == "human" else AIMessage(content=content)
    render_message(msg_obj)

prompt = st.chat_input("Ask about rice farming, AWD, fertilizer, IPM…")

if prompt:
    # 1) Show + persist user message
    st.chat_message("user").markdown(prompt)
    append_chat_event(current_id, "user", prompt)        # <- S3 write-through

    if streaming_ui:
        # 2a) Streaming path (token-by-token)
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

    # 3) Update local visible transcript for UI
    thread["messages"].append({"type": "human", "content": prompt})
    thread["messages"].append({"type": "ai", "content": ai_text})
    save_thread(thread)
