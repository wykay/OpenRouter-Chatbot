import json
from pathlib import Path
import streamlit as st
import or_client

MODEL_FILE = json.loads((Path(__file__).parent / "models.json").read_text())
CODE_TO_NAME = {m["code"]: m["name"] for m in MODEL_FILE}
MODELS = list(CODE_TO_NAME)  # all codes, in file order

def label(code):
    return CODE_TO_NAME.get(code, code)

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
                st.write(f"**Model:** {label(m.get('model', 'unknown'))}")
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
    model = st.selectbox("Model", MODELS, index=0, format_func=label)
    
    st.divider()
    MODES = {
        "End": "end",
        "Retry same model": "retry",
        "Switch model": "switch",
    }
    after_timeout = st.radio("After timeout / 429 / 504", list(MODES), index=0)
    max_wait = st.slider(
        "Max total wait (s)", 10, 180, 60,
        disabled=MODES[after_timeout] != "retry",
    )
    
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
if st.session_state.get("notice"):
    st.toast(st.session_state.pop("notice"))

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
        status = st.empty()
        order = [model] + [m for m in MODELS if m != model]

        def on_wait(delay, e):
            status.warning(f"{label(model)} busy (HTTP {e.status_code}). Retrying in {delay}s...")

        def on_switch(old, new, e):
            status.warning(f"{label(old)} failed (HTTP {e.status_code}). Trying {label(new)}...")

        try:
            with st.spinner("Thinking..."):
                filename, used = or_client.complete_with_policy(
                    order, prompt, st.session_state.context,
                    mode=MODES[after_timeout], max_wait=max_wait,
                    on_wait=on_wait, on_switch=on_switch,
                )
        except or_client.OpenRouterError as e:
            status.empty()
            st.error(f"**{label(model)}** failed: {e}")
            if e.details:
                with st.expander("Raw error details"):
                    if isinstance(e.details, (dict, list)):
                        st.json(e.details)
                    else:
                        st.code(e.details, language=None)
            st.code(prompt, language=None)
        except Exception as e:
            status.empty()
            st.exception(e)
            st.code(prompt, language=None)
        else:
            if used != model:
                st.session_state.notice = f"{label(model)} was busy, answered by {label(used)}"
            st.session_state.context = normalize(filename)
            st.rerun()
