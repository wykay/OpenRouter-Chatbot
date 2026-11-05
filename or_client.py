import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

CONV_DIR = Path(__file__).parent / "conversations"
CONV_DIR.mkdir(exist_ok=True)

load_dotenv()

def complete_request(model, message, filename=None):
    start_time = time.perf_counter()
    now = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # filename is always a bare name like "conv_2026....json"
    if filename:
        filename = Path(filename).name          # safety: strip any folder
        path = CONV_DIR / filename
        with open(path, "r") as file:
            prompt = json.load(file)
    else:
        filename = f"conv_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        path = CONV_DIR / filename
        prompt = []

    prompt.append({"timestamp": now(), "role": "user", "content": message})

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OpenRouterAPI')}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": model,
            # send only what the API expects, not timestamp/runtime/etc.
            "messages": [{"role": m["role"], "content": m["content"]} for m in prompt],
            "reasoning": {"enabled": True},
        }),
    )

    responses = response.json()
    if "error" in responses:
        error = responses["error"]
        print(f"Error with code {error.get('code')}, {error.get('message')}\n\n"
              f"{error.get('metadata', {}).get('raw', '')}\n")
        return None

    reply = responses["choices"][0]["message"]

    prompt.append({
        "timestamp": now(),
        "runtime": time.perf_counter() - start_time,
        "role": "assistant",
        "model": model,
        "content": reply.get("content"),
        "reasoning_details": reply.get("reasoning_details"),
    })

    with open(path, "w") as file:
        json.dump(prompt, file, indent=4)

    return filename
