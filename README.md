# Free AI Chatbot
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://free-ai-chatbot.streamlit.app)
[![Docker Image](https://img.shields.io/badge/docker-ready-blue.svg)](#option-2-run-with-docker)

Chatbot with access to free text models routed by OpenRouter

## All Available Models
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

> [!WARNING]
> Models may be temporarily unavailable if their upstream provider experiences downtime or have rate limited

## Try Demo on Streamlit
1. Go to https://free-ai-chatbot.streamlit.app/
2. Select a model and start chatting, you can also change model mid-conversation

> [!WARNING]
> Chat logs are not permanent. Streamlit Community Cloud wipes the files once the session is inactive.

> [!TIP]
> Download your chat logs before leaving. You can re-upload them in future sessions.

## Installation Guide

### Prerequisites
- Python 3.13 (for running locally)
- Docker (for running with Docker)
- An API key from [OpenRouter](https://openrouter.ai/) (free acccount)

### Setup
1. Clone the repository
    ```bash
    git clone https://github.com/wykay/OpenRouter-Chatbot.git
    cd OpenRouter-Chatbot
    ```
2. Configure environment variable
    ```bash
    cp .env.example .env
    ```
3. Open .env and insert your credential

> [!TIP]
> As a safety precaution, you may set the key's credit limit to 1e-99 in OpenRouter dashboard to prevent unexpected billing

### Option 1: Run Locally with Python
1. Set up a virtual environment
    Windows (PowerShell)
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
    macOS / Linux:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
3. Navigate to project root and run
    ```powershell
    python -m streamlit run main.py
    ```

### Option 2: Run with Docker
1. Build the image
    ```bash
    docker build -t free-ai-chatbot .
    ```
2. Run with environment file
    ```bash
    docker run --rm -p 8080:8080 --env-file .env free-ai-chatbot
    ```
3. To persist chat session logs locally between runs, attach a host volume:
    ```bash
    mkdir -p conversations
    docker run --rm -p 8080:8080 --env-file .env -v "$(pwd)/conversations:/app/conversations" free-ai-chatbot
    ```

### Setting Up Google AI Studio (BYOK)
API Key from Google AI Studio is recommended for OpenRouter to access its model (e.g. Gemma)
1. Obtain an API Key from [Google AI Studio](https://aistudio.google.com/)
2. In [OpenRouter](https://openrouter.ai/), navigate to Dashboard > Workspace > BYOK
3. Find "Google AI Studio" in the list of providers and paste the key
