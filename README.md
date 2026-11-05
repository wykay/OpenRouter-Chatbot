# Free AI Chatbot
Chatbot with access to free models routed by OpenRouter

Models Available
- [NVIDIA: Nemotron 3 Ultra](https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free)
- [NVIDIA: Nemotron 3.5 Super VL](https://openrouter.ai/nvidia/nemotron-3.5-super-vl:free)
- [NVIDIA: Nemotron 3.5 Lightning](https://openrouter.ai/nvidia/nemotron-3.5-lightning:free)
- [Cohere: North Mini Code](https://openrouter.ai/cohere/north-mini-code:free)
- [Dots Studio: Dots3-Note Preview](https://openrouter.ai/dots-studio/dots-3-note-preview:free)
- [Google: Gemma 4 26B A4B](https://openrouter.ai/google/gemma-4-26b-a4b-it:free)

Coming Soon
- [NVIDIA: Nemotron 3.5 Content Safety](https://openrouter.ai/nvidia/nemotron-3.5-content-safety:free)
- [NVIDIA: Nemotron 3 Nano Omni](https://openrouter.ai/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free)
- [星辰(XingChen): Xing4.0 29B A4B](https://openrouter.ai/xingchen-agi/xing4.0-29b-a4b:free)
- [Recursive: Flint](https://openrouter.ai/recursive/flint-v1.0:free)
- [LiquidAI: LFM2.5-2.6B](https://openrouter.ai/liquid/lfm-2.5-2.6b:free)
- [Google: Gemma 4 31B](https://openrouter.ai/google/gemma-4-31b-it:free)

## Try Demo on Streamlit
1. Click on the streamlit.app link on this project
2. Select a model and start chatting
    > Keep in mind that the chat log are not permanent as Streamlit will remove the files once session is inactive

## Run Project Locally
### Set OpenRouter API Key
1. Go to [OpenRouter](https://openrouter.ai/)
2. Navigate to Dashboard > Workspace > API Keys
3. Click on "New key", enter a name and define expiration date. 
    > As a safety precaution, you may set the credit limit to as little as possible (0.0001 to 1e-99) and disable Reset Limit.
4. Go to this project and create .env file by copying from .env.example file
5. Copy the API key and paste it on the file

### Set Google AI API Key
API Key from Google AI Studio is required for OpenRouter to access its model (e.g. Gemma)
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Navigate to Dashboard > API Keys
3. Click on "Create API Key", enter a name and select a project
4. Go to [OpenRouter](https://openrouter.ai/)
5. Navigate to Dashboard > Workspace > BYOK
6. Find "Google AI Studio" in the list of providers
7. Click on "Add key", enter a name, paste the key, and other settings

### Run Project Folder
1. Create virtual enviroment
    ```terminal
    python -m venv venv && source venv/bin/activate</code>
    ```
2. Install dependencies
    ```terminal
    <code>pip install -r requirements.txt</code>
    ```
3. Run
    ```terminal
    <code>python main.py</code>
    ```

### Run Project in Docker
Requires [Docker](https://docs.docker.com/get-docker/).

1. Build the image:
   ```bash
   docker build -t my-app .
   ```
2. Run it:
   ```bash
   docker run --rm -p 8080:8080 --env-file .env my-app
   ```
3. Open http://localhost:8080
    > The API key is passed at runtime through `--env-file` and is not stored in the image (`.env` is excluded via `.dockerignore`).

To keep chat logs after the container stops, mount a volume:
```bash
docker run --rm -p 8080:8080 --env-file .env -v "$(pwd)/logs:/app/logs" my-app
```

### Run Project from a Docker Registry
Pull and run the published image (you still need your own `.env`):
```bash
docker run --rm -p 8080:8080 --env-file .env yourname/my-app:1.0
```
