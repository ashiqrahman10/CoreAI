# 🚀 CoreAI

Welcome to the most over-engineered way to interact with your terminal since someone decided to use voice commands in a noisy data center!

## 🤔 What are we looking at over here?
Ever wished you could just talk to your computer and it would understand? Well, now you can! We've rigged up Google's Gemini with some extra bells and whistles to make your command line chats more interesting.

## ✨ Features That'll Blow Your Mind (or at least mildly entertain you)
* 🗣️ **Natural Language Understanding:** Chat with your CLI like it's your friend who knows a lot about computers.
* 🔄 **Command Translation:** Gemini takes your casual banter and turns it into serious command-line instructions.
* 🧠 **RAG Integration:** It remembers stuff you did before, so you don't have to!
* ✅ **User Confirmation:** Because accidentally deleting files is not fun.
* 🛡️ **Error Handling:** It's not perfect, but we're getting there.

## 🏃‍♂️ Get This Party Started
1. **Clone the Repository**
   ```bash
   git clone https://github.com/ashiqrahman10/ai-powered-cli.git
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Gemini API Key**
   * Get your API key from Google
   * Set it and forget it:
     ```bash
     export GEMINI_API_KEY='YOUR_ACTUAL_API_KEY' 
     ```

## 🚀 Usage

1. **Launch the CLI**
   ```bash
   python3 main.py
   ```

2. **Start Chatting!**
   * You'll see the `$ask` prompt.
   * Just type whatever you need (e.g., "Show me all the files in this directory").
   * The system uses its brain to figure out what you mean.
   * Confirm the command it suggests.
   * Type `y` to make it happen.

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