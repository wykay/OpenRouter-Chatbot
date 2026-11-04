import json
from pathlib import Path

import streamlit as st

import or_client

MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3.5-super-vl:free",
    "nvidia/nemotron-3.5-lightning:free",
    "cohere/north-mini-code:free",
    "dots-studio/dots-3-note-preview:free",
    "google/gemma-4-26b-a4b-it:free",
]

CONV_DIR = Path("conversations")
CONV_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Free AI Chatbot", layout="wide")

# Per-visitor state (unlike a module-level dict, this is not shared between users)
if "context" not in st.session_state:
    st.session_state.context = None  # filename of the open conversation


def load_conversation(name):
    try:
        return json.loads((CONV_DIR / name).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def normalize(name):
    """Accept 'x', 'x.json' or 'conversations/x.json' and return 'x.json'."""
    name = Path(str(name)).name
    return name if name.endswith(".json") else name + ".json"


def select(name):
    st.session_state.context = name


def new_chat():
    st.session_state.context = None


def render_message(m):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("timestamp"):
            st.caption(m["timestamp"])
        if m["role"] == "assistant":
            with st.expander("Details"):
                reasoning = "\n\n".join(
                    d["text"]
                    for d in (m.get("reasoning_details") or [])
                    if d.get("text")
                )
                runtime = m.get("runtime")
                st.write(f"**Model:** {m.get('model', 'unknown')}")
                st.write(
                    f"**Runtime:** {runtime:.6f} s"
                    if runtime is not None
                    else "**Runtime:** unknown"
                )
                st.write("**Reasoning**")
                st.markdown(reasoning or "_No reasoning recorded._")


# ---------- Sidebar ----------
with st.sidebar:
    st.button("New chat", icon=":material/add:", on_click=new_chat, use_container_width=True)
    model = st.selectbox("Model", MODELS)
    st.divider()
    for f in sorted(CONV_DIR.glob("*.json"), reverse=True):
        st.button(
            f.name,
            key=f"conv_{f.name}",
            on_click=select,
            args=(f.name,),
            type="primary" if f.name == st.session_state.context else "secondary",
            use_container_width=True,
        )

# ---------- Chat history ----------
if st.session_state.context is None:
    st.caption("New chat")
else:
    for m in load_conversation(st.session_state.context):
        render_message(m)

# ---------- Input ----------
prompt = st.chat_input("Type a message...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            filename = or_client.complete_request(model, prompt, st.session_state.context)

    if filename:
        st.session_state.context = normalize(filename)
        st.rerun()
    else:
        st.error("Request failed, check the app logs.")
        st.code(prompt, language=None)  # so you can copy your message and retry
