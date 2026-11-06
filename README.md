# Free AI Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)
[![Docker Image](https://img.shields.io/badge/docker-ready-blue.svg)](#run-with-docker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Chatbot with access to free text models routed by OpenRouter

## All Models Available
- [NVIDIA: Nemotron 3 Ultra](https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free)
- [NVIDIA: Nemotron 3.5 Super VL](https://openrouter.ai/nvidia/nemotron-3.5-super-vl:free)
- [NVIDIA: Nemotron 3.5 Lightning](https://openrouter.ai/nvidia/nemotron-3.5-lightning:free)
- [NVIDIA: Nemotron 3 Nano Omni](https://openrouter.ai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free)
- [Google: Gemma 4 26B A4B](https://openrouter.ai/google/gemma-4-26b-a4b-it:free)
- [Google: Gemma 4 31B](https://openrouter.ai/google/gemma-4-31b-it:free)
- [Cohere: North Mini Code](https://openrouter.ai/cohere/north-mini-code:free)
- [Recursive: Flint](https://openrouter.ai/recursive/flint-v1.0:free)
- [LiquidAI: LFM2.5-2.6B](https://openrouter.ai/liquid/lfm-2.5-2.6b:free)
- [两点工作室 (Dots Studio): Dots3-Note Preview](https://openrouter.ai/dots-studio/dots-3-note-preview:free) (Leaving on 31 December 2026)
- [星辰 (XingChen): Xing4.0 29B A4B](https://openrouter.ai/xingchen-agi/xing4.0-29b-a4b:free)
    > Models may be temporarily unavailable if their upstream provider experiences downtime

## Try Demo on Streamlit
1. Click on the streamlit.app link on this project
2. Select a model and start chatting
    > Chat logs are not permanent as Streamlit Community Cloud will wipe the files once session is inactive

    > Download your chat logs before leaving to save your conversation locally, which you can re-upload in future sessions

## Installation Guide

### Prerequisites
- Python 3.10+ or Docker installed
- An [OpenRouter API Key](https://openrouter.ai/) (free account)

### Option 1: Run Locally with Python
1. Clone the repository
    ```bash
    git clone https://github.com/wykay/OpenRouter-Chatbot.git
    ```
2. Set up a virtual enviroment
    Windows (Powershell)
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
    macOS / Linux:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Configure enviroment variable
    ```bash
    cp .env.example .env
    ```
    Open .env and insert your credential
    > As a safety precaution, you may set the key's credit limit to 1e-99 in OpenRouter dashboard to prevent unexpected billing
5. Navigate to project root and run
    ```powershell
    python -m streamlit run main.py
    ```
    Click on the Local URL, which should be http://localhost:8501

### Option 2: Run with Docker
```bash
# Build the image
docker build -t free-ai-chatbot .

# Run with environment file (port 8080 or default 8501)
docker run --rm -p 8080:8080 --env-file .env free-ai-chatbot
```

To persist chat session logs locally between runs, attach a host volume:

```bash
docker run --rm -p 8080:8080 --env-file .env -v "$(pwd)/logs:/app/logs" free-ai-chatbot
```

### Setting Up Google AI Studio (BYOK)
API Key from Google AI Studio is recommended for OpenRouter to access its model (e.g. Gemma)
1. Obtain an API Key from [Google AI Studio](https://aistudio.google.com/)
2. In [OpenRouter](https://openrouter.ai/), navigate to Dashboard > Workspace > BYOK
3. Find "Google AI Studio" in the list of providers and paste the key
