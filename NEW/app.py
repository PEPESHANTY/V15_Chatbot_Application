# app.py
import os, json, uuid, time
from pathlib import Path

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

# Import your compiled LangGraph and state types from final.py
from final import graph  # your compiled LangGraph with MemorySaver checkpointer

# ---------- Config ----------
CHAT_DIR = Path("./chats")
CHAT_DIR.mkdir(exist_ok=True)

# ---------- Helpers ----------
def _thread_path(thread_id: str) -> Path:
    return CHAT_DIR / f"{thread_id}.json"

def load_threads_index():
    """
    Build an index of saved chats from files.
    Returns newest-first list of dicts: {"id": <uuid>, "title": "Chat N", "updated": <mtime>}
    """
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
        # Fallback if file missing (shouldn't happen often)
        return {"id": thread_id, "title": f"Chat {thread_id[:8]}", "messages": []}
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_thread(thread: dict):
    p = _thread_path(thread["id"])
    with p.open("w", encoding="utf-8") as f:
        json.dump(thread, f, ensure_ascii=False, indent=2)

def _extract_chat_numbers(threads_index):
    """
    Extract list of integers from titles in the format 'Chat N'.
    """
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
    """
    Finds the next sequential chat number based on existing chats.
    """
    existing = load_threads_index()
    nums = _extract_chat_numbers(existing)
    return (max(nums) + 1) if nums else 1

def new_thread():
    """
    Create a new thread with a UUID id but a sequential human title 'Chat N'.
    """
    tid = str(uuid.uuid4())
    chat_num = get_next_chat_number()
    thread = {"id": tid, "title": f"Chat {chat_num}", "messages": []}
    save_thread(thread)
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

# ---------- Streamlit State ----------
if "current_thread" not in st.session_state:
    # pick most recent, else create one
    existing = load_threads_index()
    st.session_state.current_thread = existing[0]["id"] if existing else new_thread()

if "rename_buffer" not in st.session_state:
    st.session_state.rename_buffer = ""

# ---------- Sidebar (thread list / actions) ----------
st.sidebar.title("RiceAI Chats")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.current_thread = new_thread()
    st.rerun()

threads = load_threads_index()
if not threads:
    st.sidebar.info("No chats yet. Start a new one!")
else:
    # Select chat (labels show 'Chat N')
    ids = [t["id"] for t in threads]
    labels = [t["title"] for t in threads]
    # Default selection is the current thread id
    idx = ids.index(st.session_state.current_thread) if st.session_state.current_thread in ids else 0
    choice = st.sidebar.selectbox("Open chat", options=list(range(len(ids))), format_func=lambda i: labels[i], index=idx)
    st.session_state.current_thread = ids[choice]

    # Rename / Delete
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
                # switch to most recent or create new
                left = load_threads_index()
                st.session_state.current_thread = left[0]["id"] if left else new_thread()
                st.rerun()

# ---------- Main area ----------
current_id = st.session_state.current_thread
thread = load_thread(current_id)

# Title shows the clean "Chat N"
st.title(thread.get("title", "Chat"))

# Show history (only Human/AI)
for m in thread["messages"]:
    role = m.get("type")
    content = m.get("content", "")
    msg_obj = HumanMessage(content=content) if role == "human" else AIMessage(content=content)
    render_message(msg_obj)

# Chat input
prompt = st.chat_input("Ask about rice farming, AWD, fertilizer, IPM…")

if prompt:
    # 1) Show user msg
    user_msg = HumanMessage(content=prompt)
    st.chat_message("user").markdown(prompt)

    # 2) Invoke your LangGraph with THIS thread_id to keep memory isolated
    input_data = {"question": user_msg}
    result = graph.invoke(
        input=input_data,
        config={"configurable": {"thread_id": current_id}},  # <= per-thread memory
    )

    # 3) Extract latest AI reply from state
    ai_text = "No response."
    if isinstance(result, dict) and "messages" in result:
        replies = [m for m in result["messages"] if isinstance(m, AIMessage)]
        if replies:
            ai_text = replies[-1].content

    # 4) Show assistant reply
    st.chat_message("assistant").markdown(ai_text)

    # 5) Save visible transcript for this chat
    thread["messages"].append({"type": "human", "content": prompt})
    thread["messages"].append({"type": "ai", "content": ai_text})
    save_thread(thread)
