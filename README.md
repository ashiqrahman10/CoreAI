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
```
PS D:\Projects\ai-powered-cli> python3 .\main.py
$ask list all files
> Execute "dir /a"? [y/N] y
 Volume in drive D is New Volume
 Volume Serial Number is 6CBF-C757

 Directory of D:\Projects\ai-powered-cli

10/19/2024  08:05 PM    <DIR>          .
10/19/2024  07:36 PM    <DIR>          ..
10/19/2024  07:40 PM                56 .env
10/19/2024  07:59 PM    <DIR>          .git
10/19/2024  07:54 PM             3,308 .gitignore
10/19/2024  07:36 PM            35,823 LICENSE
10/19/2024  07:53 PM             3,015 main.py
10/19/2024  07:59 PM             1,264 README.md
10/19/2024  07:57 PM             3,304 requirements.txt
10/19/2024  07:37 PM    <DIR>          venv
10/19/2024  07:43 PM    <DIR>          wenv
               6 File(s)         46,770 bytes
               5 Dir(s)  776,908,189,696 bytes free

$ask
```

