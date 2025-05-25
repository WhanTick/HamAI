from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv
from speech_corrector import expand_slang



# Load env vars
load_dotenv()

# eleven LABSSS
from elevenlabs.client import ElevenLabs
from elevenlabs import play

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def say(text_to_say):
    text_to_say = expand_slang(text_to_say)
    audio = elevenlabs.text_to_speech.convert(
        text=f"{text_to_say}",
        voice_id=os.getenv("VOICE_ID"),
        model_id=os.getenv("MODEL_ID"),
        output_format=os.getenv("OUTPUT_FORMAT"),
        language_code=os.getenv("LANGUAGE_CODE"),
    )

    play(audio)

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory_data = json.load(f)
        return [
            types.Content(
                role=item["role"],
                parts=[types.Part.from_text(text=part["text"]) for part in item["parts"]]
            )
            for item in memory_data
        ]

def save_memory(contents):
    memory_data = [
        {
            "role": content.role,
            "parts": [{"text": part.text} for part in content.parts]
        }
        for content in contents
    ]
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=2)

def chat_with_memory():
    client = genai.Client(
        vertexai=True,
        project=os.getenv("PROJECT_ID"),
        location=os.getenv("LOCATION"),

    )

    with open(os.getenv("SYSTEM_PROMPT_PATH"), "r", encoding="utf-8") as f:
        system_prompt = f.read()

    contents = load_memory()

    generate_content_config = types.GenerateContentConfig(
        temperature=2,
        top_p=0.95,
        max_output_tokens=8192,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
        ],
        system_instruction=[types.Part.from_text(text=system_prompt)],
    )

    print("Start chatting (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break

        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))

        response = client.models.generate_content(
            model=os.getenv("MODEL_ENDPOINT"),
            contents=contents,
            config=generate_content_config,
        )

        reply = response.candidates[0].content.parts[0].text
        print("AI:", reply)
        say(reply)

        contents.append(types.Content(role="model", parts=[types.Part.from_text(text=reply)]))

        # Save updated memory
        save_memory(contents)

chat_with_memory()
