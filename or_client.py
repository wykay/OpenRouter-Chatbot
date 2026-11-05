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

TRANSIENT = {429, 502, 503, 504}

class OpenRouterError(Exception):
    def __init__(self, message, details=None, status_code=None):
        super().__init__(message)
        self.details = details
        self.status_code = status_code

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
        raise OpenRouterError(
            f"Network error: {type(e).__name__}: {e}",
            status_code=504 if isinstance(e, requests.exceptions.Timeout) else None,
        )

    try:
        responses = response.json()
    except ValueError:
        raise OpenRouterError(
            f"HTTP {response.status_code}: response was not valid JSON",
            details=response.text[:2000],
            status_code=response.status_code,
        )

    if "error" in responses:
        error = responses["error"]
        try:
            code = int(error.get("code") or response.status_code)
        except (TypeError, ValueError):
            code = response.status_code
        raise OpenRouterError(
            f"HTTP {response.status_code} | code {error.get('code')}: {error.get('message')}",
            details=responses,
            status_code=code,
        )

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

def complete_with_policy(models, message, filename=None, mode="end",
                         max_wait=60, max_attempts=4, on_wait=None, on_switch=None):
    """Returns (filename, model_used). mode: 'end' | 'retry' | 'switch'."""
    deadline = time.monotonic() + max_wait
    delay = 2
    attempts = 0
    idx = 0
    while True:
        model = models[idx]
        attempts += 1
        try:
            return complete_request(model, message, filename), model
        except OpenRouterError as e:
            transient = e.status_code in TRANSIENT
            if mode == "end" or not transient or attempts >= max_attempts:
                raise

            if mode == "switch":
                if idx + 1 >= len(models):
                    raise
                idx += 1
                if on_switch:
                    on_switch(model, models[idx], e)
                continue

            # mode == "retry": wait grows after each 429/504
            if time.monotonic() + delay > deadline:
                raise
            if on_wait:
                on_wait(delay, e)
            time.sleep(delay)
            delay = min(delay * 2, 30)