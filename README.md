# HamAI 🤖💬🔊

HamAI is a Python-based conversational AI project that leverages Google's Generative AI (via Vertex AI) for chat capabilities and ElevenLabs for realistic Text-to-Speech (TTS) output. It features persistent conversation memory and an Indonesian slang corrector to enhance the TTS experience.

## Features ✨

*   **Interactive Chat:** Engage in conversations with Google's powerful generative AI models.
*   **Persistent Memory:** Conversation history is saved to `memory.json` and loaded on startup, allowing the AI to remember previous interactions.
*   **Text-to-Speech:** AI responses are spoken aloud using ElevenLabs' high-quality voice synthesis.
*   **Indonesian Slang Correction:** Common Indonesian slang in AI responses is automatically expanded to its full form before TTS, ensuring clearer and more natural-sounding speech.
*   **Configurable:** Easily configure API keys, model IDs, voice preferences, and system prompts via environment variables.
*   **Custom System Prompt:** Define the AI's persona and instructions through an external system prompt file.

## File Structure 📂
```
HamAI/
├── test_memory.py        # Main application script for chat and TTS
├── speech_corrector.py   # Module for Indonesian slang expansion
├── memory.json           # (Auto-generated) Stores conversation history
├── .env                  # (You need to create this) Stores API keys and configuration
└── system_prompt.txt     # (You need to create this) Contains the AI's system prompt
```


## Prerequisites 📋

*   Python 3.7+
*   Access to Google Cloud Platform:
    *   A Google Cloud Project ID.
    *   Vertex AI API enabled for your project.
    *   Authenticated `gcloud` CLI or Application Default Credentials set up.
*   ElevenLabs Account:
    *   An ElevenLabs API Key.
    *   A Voice ID from ElevenLabs.
    *   (Optional) A specific ElevenLabs Model ID.

## Setup & Installation ⚙️

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/HamAI.git
    cd HamAI
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install google-generativeai python-dotenv elevenlabs
    ```
    *Note: `google-generativeai` is used, which can interface with Vertex AI if configured.*

4.  **Configure Environment Variables:**
    Create a `.env` file in the root of the project directory with the following content. Replace the placeholder values with your actual credentials and preferences:

    ```env
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY"
    VOICE_ID="YOUR_ELEVENLABS_VOICE_ID" # e.g., "21m00Tcm4TlvDq8ikWAM"
    MODEL_ID="eleven_multilingual_v2"  # Or your preferred ElevenLabs model
    OUTPUT_FORMAT="mp3_44100_128"
    LANGUAGE_CODE="id" # Indonesian, matching the slang corrector

    # Google Cloud / Vertex AI Configuration
    PROJECT_ID="your-gcp-project-id"
    LOCATION="your-gcp-project-location" # e.g., "us-central1"
    MODEL_ENDPOINT="gemini-1.0-pro" # Or other compatible model like "gemini-1.5-flash-latest"

    # Application Configuration
    SYSTEM_PROMPT_PATH="system_prompt.txt"
    ```

5.  **Create the System Prompt File:**
    Create a file named `system_prompt.txt` (or the path you specified in `SYSTEM_PROMPT_PATH`) in the project root. This file defines the AI's behavior, personality, and any specific instructions.
    Example `system_prompt.txt`:
    ```txt
    You are HamAI, a friendly and helpful assistant.
    You speak casually but clearly.
    Your responses should be concise and informative.
    You are an expert in Indonesian culture.
    ```

## Running the Application ▶️

Once the setup and configuration are complete, you can run the application:

```bash
python test_memory.py

## Running the Application ▶️

Once the setup and configuration are complete, you can run the application:

```bash
python test_memory.py
```

You will see a prompt:
```
Start chatting (type 'exit' to quit)
You:
```
Type your message and press Enter. The AI's response will be printed to the console and spoken aloud. Type `exit` to end the conversation and save the current session to `memory.json`.

## How `test_memory.py` Works 🧠

1.  **Initialization:**
    *   Loads environment variables from `.env`.
    *   Initializes the ElevenLabs client.
    *   Loads the system prompt from the specified file path.
    *   Loads previous conversation history from `memory.json` (if it exists).

2.  **Chat Loop:**
    *   Prompts the user for input.
    *   If the user types "exit", the loop breaks.
    *   The user's input is added to the `contents` (conversation history).
    *   A request is made to the Google GenAI model (via Vertex AI) with the current `contents` and generation configuration.
    *   The AI's reply is extracted from the response.
    *   The AI's reply is printed to the console.
    *   The `say()` function is called:
        *   The `expand_slang()` function from `speech_corrector.py` processes the reply to convert Indonesian slang to full words.
        *   The processed text is sent to ElevenLabs API for TTS.
        *   The generated audio is played.
    *   The AI's reply is added to the `contents`.
    *   The updated `contents` (conversation history) is saved to `memory.json`.

## How `speech_corrector.py` Works 🗣️

*   It contains a dictionary (`slang_dict`) mapping common Indonesian slang words to their full forms.
*   The `expand_slang(text)` function takes a string as input.
*   It uses regular expressions to split the text into words while preserving punctuation.
*   Each word is checked against the `slang_dict`; if a match is found (case-insensitive), the slang word is replaced by its full form.
*   The processed words are joined back into a string.

This helps in making the TTS output from ElevenLabs sound more formal and understandable, especially when the AI might pick up slang from its training data or conversational context.
