# Free AI Chatbot
Chatbot with access to free models routed by OpenRouter

## OpenRouter API Key
1. Go to https://openrouter.ai/
2. Navigate to Dashboard > Workspace > API Keys
3. Click on "New key", enter a name and define expiration date. 
4. As a safety precaution, you may set the credit limit to as little as possible (0.0001 to 1e-99) and disable Reset Limit.
5. Go to this project and create .env file by copying from .env.example file
6. Copy the API key and paste it on the file

## Google AI API Key
API Key from Google AI Studio is required for OpenRouter to access its model (e.g. Gemma)
1. Go to https://aistudio.google.com/
2. Navigate to Dashboard > API Keys
3. Click on "Create API Key", enter a name and select a project
4. Go to https://openrouter.ai/
5. Navigate to Dashboard > Workspace > BYOK
6. Find "Google AI Studio" in the list of providers
7. Click on "Add key", enter a name, paste the key, and other settings

## Setup This Project and Run
1. <code>.venv\Scripts\activate</code>
2. <code>pip install -r requirements.txt</code>
3. <code>python main.py</code>