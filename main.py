import os
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
import threading
import sys

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
            
        # Hide input elements and show confirmation
        input_entry.pack_forget()
        icon_label.pack_forget()

        # Start pulsing animation
        input_entry.configure(bg="#2a2a3f")
        # animate_processing()
        
        # Get command in background thread
        def get_command_thread():
            command = get_command(user_input)
            root.after(0, lambda: show_confirmation(command))
        
        threading.Thread(target=get_command_thread, daemon=True).start()

    # def animate_processing():
    #     """Creates a pulsing glow effect while processing"""
    #     colors = ["#2a2a3f", "#2a2a4f", "#2a2a5f", "#2a2a4f"]
    #     def pulse(index=0):
    #         # Only continue animation if window still exists and hasn't been destroyed
    #         if input_entry.winfo_exists() and not root.winfo_exists():
    #             return
    #         try:
    #             input_entry.configure(bg=colors[index])
    #             root.after_id = root.after(200, lambda: pulse((index + 1) % len(colors)))
    #         except tk.TclError:
    #             return  # Silently exit if window was destroyed
    #     pulse()

    def show_confirmation(command):
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
        yes_btn = tk.Button(confirm_frame, text="Yes", command=lambda: confirm_execute(command),
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
                confirm_execute(command)
            else:
                root.destroy()

        # Bind arrow keys and enter for selection
        root.bind('<Left>', lambda e: move_selection(-1))
        root.bind('<Right>', lambda e: move_selection(1))
        root.bind('<Return>', lambda e: select_current())

    def confirm_execute(command):
        root.destroy()
        execute_command(command)

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
    """Gets the command from Gemini API based on user input."""
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