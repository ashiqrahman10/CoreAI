import os
import subprocess
import dotenv
from gemini import Client

# Replace with your actual Gemini API credentials
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'

gemini_client = Client(GEMINI_API_KEY)

def execute_command(command):
    """Executes the given terminal command and prints the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error executing command: {e}")

while True:
    user_input = input("$ask ")

    # Use Gemini API to get the corresponding command
    prompt = f"Translate the following user intent into a terminal command: {user_input}"
    response = gemini_client.query(prompt)
    command = response.text.strip() # Extract the command from the response

    print(f"> Execute \"{command}\"? [y/N] ", end="")
    confirmation = input().lower()
    if confirmation == "y":
        execute_command(command)