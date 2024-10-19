import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  safety_settings  =  [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

def execute_command(command):
    """Executes the given terminal command and prints the output."""
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        else:  # Unix-based systems
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error executing command: {e}")

while True:
    user_input = input("$ask ")

    # Use Gemini API to get the corresponding command
    if os.name == 'nt':  # Windows
        chat_session = model.start_chat(
            history=[
                {
                "role": "user",
                "parts": [
                    "Translate the following user intent into a Windows Command Prompt command. Give only the command and nothing else:",
                ],
                },
                {
                "role": "model",
                "parts": [
                    "Please provide the user intent you would like translated into a Windows Command Prompt command.\n",
                ],
                },
            ]
        )
    else:  # Unix-based systems
        chat_session = model.start_chat(
        history=[
            {
            "role": "user",
            "parts": [
                "Translate the following user intent into a terminal command. Give only the command and nothing else:",
            ],
            },
            {
            "role": "model",
            "parts": [
                "Please provide the user intent you would like translated into a terminal command. \n",
            ],
            },
        ]
    )

    response = chat_session.send_message(user_input)
    command = response.text.strip() # Extract the command from the response

    print(f"> Execute \"{command}\"? [y/N] ", end="")
    confirmation = input().lower()
    if confirmation == "y":
        execute_command(command)