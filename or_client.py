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

class OpenRouterError(Exception):
    """Carries a readable message plus raw details for debugging."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details


def complete_request(model, message, filename=None):
    start_time = time.perf_counter()
    now = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if filename:
        filename = Path(filename).name
        path = CONV_DIR / filename
        with open(path, "r") as file:
            prompt = json.load(file)
    else:
        filename = f"conv_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        path = CONV_DIR / filename
        prompt = []

    prompt.append({"timestamp": now(), "role": "user", "content": message})

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OpenRouterAPI')}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": model,
                "messages": [{"role": m["role"], "content": m["content"]} for m in prompt],
                "reasoning": {"enabled": True},
            }),
            timeout=120,
        )
    except requests.exceptions.RequestException as e:
        raise OpenRouterError(f"Network error: {type(e).__name__}: {e}")

    try:
        responses = response.json()
    except ValueError:
        raise OpenRouterError(
            f"HTTP {response.status_code}: response was not valid JSON",
            details=response.text[:2000],
        )

    if "error" in responses:
        error = responses["error"]
        raise OpenRouterError(
            f"HTTP {response.status_code} | code {error.get('code')}: {error.get('message')}",
            details=responses,  # includes metadata.raw, provider_name, etc.
        )

    if not responses.get("choices"):
        raise OpenRouterError("Response had no 'choices'", details=responses)

    choice = responses["choices"][0]
    reply = choice["message"]

    if not reply.get("content"):
        raise OpenRouterError(
            f"Model returned empty content (finish_reason: {choice.get('finish_reason')})",
            details=responses,
        )

    prompt.append({
        "timestamp": now(),
        "runtime": time.perf_counter() - start_time,
        "role": "assistant",
        "model": model,
        "content": reply["content"],
        "reasoning_details": reply.get("reasoning_details"),
    })

    with open(path, "w") as file:
        json.dump(prompt, file, indent=4)

    return filename