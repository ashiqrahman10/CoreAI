import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
import threading
import sys
import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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
)

# Initialize sentence transformer model for embeddings
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Setup data storage
data_dir = Path.home() / '.coreai'
data_dir.mkdir(exist_ok=True)

alias_file = data_dir / 'aliases.json'
vector_db_file = data_dir / 'vector_db.json'

# Initialize or load alias mappings
if alias_file.exists():
    with open(alias_file) as f:
        aliases = json.load(f)
else:
    aliases = {}
    with open(alias_file, 'w') as f:
        json.dump(aliases, f)

# Initialize or load vector database
if vector_db_file.exists():
    with open(vector_db_file) as f:
        vector_db = json.load(f)
else:
    vector_db = {
        'queries': [],
        'commands': [],
        'embeddings': []
    }
    with open(vector_db_file, 'w') as f:
        json.dump(vector_db, f)

def save_to_vector_db(query, command):
    """Save successful query-command pairs to vector database"""
    query_embedding = sentence_model.encode(query).tolist()
    
    vector_db['queries'].append(query)
    vector_db['commands'].append(command)
    vector_db['embeddings'].append(query_embedding)
    
    with open(vector_db_file, 'w') as f:
        json.dump(vector_db, f)

def find_similar_command(query, threshold=0.8):
    """Find similar command from vector database"""
    if not vector_db['queries']:
        return None
        
    query_embedding = sentence_model.encode(query)
    db_embeddings = np.array(vector_db['embeddings'])
    
    similarities = cosine_similarity([query_embedding], db_embeddings)[0]
    max_sim_idx = np.argmax(similarities)
    
    if similarities[max_sim_idx] >= threshold:
        return vector_db['commands'][max_sim_idx]
    return None

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

def get_user_input():
    """Gets user input from a UI window."""
    def submit_input():
        user_input = input_entry.get().strip()
        if not user_input:
            return
            
        if user_input.lower() == "exit":
            root.destroy()
            sys.exit()
            
        # Handle alias commands
        if user_input.startswith("alias "):
            parts = user_input[6:].split("=", 1)
            if len(parts) == 2:
                alias_name = parts[0].strip()
                command = parts[1].strip().strip('"\'')
                aliases[alias_name] = command
                with open(alias_file, 'w') as f:
                    json.dump(aliases, f)
                root.destroy()
                print(f"Alias '{alias_name}' created for command: {command}")
                return
                
        # Check if input matches an alias
        if user_input in aliases:
            command = aliases[user_input]
            root.destroy()
            execute_command(command)
            return
            
        # Hide input elements and show confirmation
        input_entry.pack_forget()
        icon_label.pack_forget()

        # Start pulsing animation
        input_entry.configure(bg="#2a2a3f")
        
        # Get command in background thread
        def get_command_thread():
            command = get_command(user_input)
            root.after(0, lambda: show_confirmation(command, user_input))
        
        threading.Thread(target=get_command_thread, daemon=True).start()

    def show_confirmation(command, query):
        # Cancel any pending animation
        if hasattr(root, 'after_id'):
            root.after_cancel(root.after_id)
        
        # Stop animation by changing back to normal color
        try:
            input_entry.configure(bg="#1f1f1f")
        except tk.TclError:
            return  # Window might be already destroyed
            
        # Check if command is too long
        if len(command) > 80:  # Reasonable length for popup box
            root.destroy()
            print("Command too long to display. Please try a simpler request.")
            return
            
        confirm_frame = tk.Frame(main_frame, bg="#1f1f1f")
        confirm_frame.pack(fill=tk.BOTH, expand=True)
        
        confirm_label = tk.Label(confirm_frame, text=f"Execute \"{command}\"?", 
                               font=("Segoe UI", 12), bg="#1f1f1f", fg="white")
        confirm_label.pack(side=tk.LEFT, padx=5)
        
        buttons = []
        yes_btn = tk.Button(confirm_frame, text="Yes", 
                           command=lambda: confirm_execute(command, query),
                           bg="#2f2f2f", fg="white", relief="flat", padx=10)
        yes_btn.pack(side=tk.LEFT, padx=5)
        buttons.append(yes_btn)
        
        no_btn = tk.Button(confirm_frame, text="No", command=root.destroy,
                          bg="#2f2f2f", fg="white", relief="flat", padx=10)
        no_btn.pack(side=tk.LEFT, padx=5)
        buttons.append(no_btn)

        # Initialize selection
        current_selection = 0
        buttons[current_selection].configure(bg="#4f4f4f")

        def move_selection(direction):
            nonlocal current_selection
            buttons[current_selection].configure(bg="#2f2f2f")
            current_selection = (current_selection + direction) % len(buttons)
            buttons[current_selection].configure(bg="#4f4f4f")

        def select_current():
            if current_selection == 0:
                confirm_execute(command, query)
            else:
                root.destroy()

        # Bind arrow keys and enter for selection
        root.bind('<Left>', lambda e: move_selection(-1))
        root.bind('<Right>', lambda e: move_selection(1))
        root.bind('<Return>', lambda e: select_current())

    def confirm_execute(command, query):
        root.destroy()
        execute_command(command)
        save_to_vector_db(query, command)

    def on_escape(event):
        root.destroy()

    root = tk.Tk()
    root.title("CoreAI")
    
    # Calculate position to center horizontally and appear near top of screen
    screen_width = root.winfo_screenwidth()
    window_width = 700
    x_position = (screen_width - window_width) // 2
    root.geometry(f"{window_width}x60+{x_position}+100")
    
    root.configure(bg="#1f1f1f")
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    
    # Main frame
    main_frame = tk.Frame(root, bg="#1f1f1f", padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Search icon/label ($ symbol as placeholder)
    icon_label = tk.Label(main_frame, text="$", font=("Segoe UI", 12), bg="#1f1f1f", fg="#666666")
    icon_label.pack(side=tk.LEFT, padx=(0, 10))
    
    # Input entry
    input_entry = tk.Entry(main_frame, font=("Segoe UI", 12), bg="#1f1f1f", fg="white", 
                          insertbackground="white", relief="flat")
    input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_entry.focus_set()
    
    # Bind events
    root.bind('<Return>', lambda e: submit_input())
    root.bind('<Escape>', on_escape)
    
    # Add subtle border
    border_frame = tk.Frame(root, bg="#333333", height=1)
    border_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()

def get_command(user_input):
    """Gets the command from vector DB or Gemini API based on user input."""
    # First check vector DB for similar commands
    similar_command = find_similar_command(user_input)
    if similar_command:
        return similar_command
        
    # If no similar command found, use Gemini API
    if os.name == 'nt':  # Windows
        chat_session = model.start_chat(
            history=[
                {
                "role": "user",
                "parts": [
                    "Translate the following user intent into a Windows Command Prompt command. Give only the command and nothing else. The command must fit on one line:",
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
                "Translate the following user intent into a terminal command. Give only the command and nothing else. The command must fit on one line:",
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
    return response.text.strip()

while True:
    get_user_input()