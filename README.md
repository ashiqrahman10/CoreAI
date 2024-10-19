# 🚀 AI-Powered CLI

Harness the power of Google's Gemini large language model to interact with your terminal using natural language!

## ✨ Features

* 🗣️ **Natural Language Understanding:** Communicate with your CLI using everyday language.
* 🔄 **Command Translation:** Gemini interprets your intent and generates the appropriate terminal command.
* ✅ **User Confirmation:** Safety first! Confirm before executing any command.
* 🛡️ **Error Handling:** Robust mechanisms to gracefully manage unexpected situations.

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ashiqrahman10/ai-powered-cli.git
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Gemini API Key**
   * Obtain your API key from Google
   * Set the environment variable:
     ```bash
     export GEMINI_API_KEY='YOUR_ACTUAL_API_KEY' 
     ```

## 🚀 Usage

1. **Launch the CLI**
   ```bash
   python3 main.py
   ```

2. **Start Interacting!**
   * You'll see the `$ask` prompt
   * Type your request naturally (e.g., "Show me all the files in this directory")
   * Review the suggested command
   * Type `y` to execute

## 💡 Example