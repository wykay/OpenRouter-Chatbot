import json
from pathlib import Path
from nicegui import run, ui
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
ui.add_css("""
.nicegui-markdown > :last-child { margin-bottom: 0 !important; }
.msg-meta { font-size: 0.7rem; opacity: 0.6; line-height: 1; }
.msg-link { cursor: pointer; text-decoration: underline; }
.msg-link:hover { opacity: 1; }
""")

state = {"context": None, "pending": None}  # pending = message awaiting a reply

def load_conversation(name):
    return json.loads((CONV_DIR / name).read_text())

def normalize(name):
    """Accept 'x', 'x.json' or 'conversations/x.json' and return 'x.json'."""
    name = Path(str(name)).name
    return name if name.endswith(".json") else name + ".json"

@ui.refreshable
def sidebar():
    ui.button("New chat", icon="add", on_click=new_chat).classes("w-full")
    for f in sorted(CONV_DIR.glob("*.json"), reverse=True):
        color = "primary" if f.name == state["context"] else "grey-8"
        ui.button(f.name, on_click=lambda n=f.name: select(n)) \
            .props(f"flat no-caps align=left color={color}").classes("w-full")

def show_details(m):
    reasoning = "\n\n".join(
        d["text"] for d in (m.get("reasoning_details") or []) if d.get("text")
    )
    runtime = m.get("runtime")

    with ui.dialog().props("full-width") as dialog, \
            ui.card().style("width: 90vw; max-width: 1100px;"):
        ui.label("Response details").classes("text-lg font-bold")
        ui.label(f"Model: {m.get('model', 'unknown')}")
        ui.label(f"Runtime: {runtime:.6f} s" if runtime is not None else "Runtime: unknown")
        ui.label("Reasoning").classes("font-bold mt-2")
        with ui.scroll_area().style("height: 60vh; width: 100%;"):
            ui.markdown(reasoning or "_No reasoning recorded._")
        ui.button("Close", on_click=dialog.close).props("flat")

    dialog.on("hide", dialog.delete)
    dialog.open()

@ui.refreshable
def messages():
    if state["context"] is None and not state["pending"]:
        ui.label("New chat").classes("text-grey")
        return
    if state["context"] is not None:
        for m in load_conversation(state["context"]):
            with ui.chat_message(sent=m["role"] == "user").classes("w-full"):
                with ui.column().classes("gap-1"):
                    ui.markdown(m["content"])
                    with ui.row().classes("items-center gap-2 msg-meta"):
                        ui.label(m.get("timestamp", ""))
                        if m["role"] == "assistant":
                            ui.label("Details") \
                                .classes("msg-link") \
                                .on("click", lambda m=m: show_details(m))
    if state["pending"]:
        with ui.chat_message(sent=True).classes("w-full"):
            ui.markdown(state["pending"])
        with ui.chat_message(sent=False).classes("w-full"):
            ui.spinner("dots", size="lg")

def refresh_all():
    sidebar.refresh()
    messages.refresh()
    scroll.scroll_to(percent=1.0)

def select(name):
    state["context"] = name
    refresh_all()

def new_chat():
    state["context"] = None
    refresh_all()

async def send():
    text = box.value.strip()
    if not text or state["pending"]:
        return
    box.value = ""
    state["pending"] = text
    send_btn.disable()
    refresh_all()

    filename = await run.io_bound(
        or_client.complete_request, model_select.value, text, state["context"]
    )

    if filename:
        state["context"] = filename
    else:
        ui.notify("Request failed, see console", type="negative")
        box.value = text
    state["pending"] = None
    send_btn.enable()
    refresh_all()

ui.query(".nicegui-content").classes("p-0")

with ui.row().classes("w-full h-screen no-wrap gap-0"):
    with ui.column().classes("w-72 h-full p-3 border-r overflow-auto"):
        sidebar()

    with ui.column().classes("flex-grow h-full p-3 no-wrap"):
        scroll = ui.scroll_area().classes("flex-grow w-full")
        with scroll:
            messages()
        with ui.row().classes("w-full items-end no-wrap"):
            box = ui.textarea(placeholder="Type a message...") \
                .props("outlined autogrow").classes("flex-grow") \
                .on("keydown.ctrl.enter", send)
            model_select = ui.select(MODELS, value=MODELS[0]).props("outlined").classes("w-64")
            send_btn = ui.button("Send", icon="send", on_click=send)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Free AI Chatbot", host="0.0.0.0", port=8080, reload=False)