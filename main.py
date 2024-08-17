import os
import getpass
import subprocess
import google.generativeai as genai
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter

# Replace with your actual Gemini API credentials
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key here")

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
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error executing command: {e}")

# Load documents from your filesystem
loader = TextLoader("gay.txt") # Replace with your file path
documents = loader.load()
# Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# Create embeddings and store them in a vectorstore
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.from_documents(docs, embeddings)

# Create the LangChain QA chain
# qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=vectorstore.as_retriever())  # Original
qa = RetrievalQA.from_chain_type(llm=GoogleGenerativeAIEmbeddings(model="models/embedding-001"), chain_type="stuff", retriever=vectorstore.as_retriever())

while True:
    user_input = input("$ask ")

    # If the user input starts with "fs ", use LangChain for file-related queries
    if user_input.startswith("fs "):
        query = user_input[3:]  # Remove the "fs " prefix
        result = qa.run(query)
        print(result)
    else:
        # Use Gemini API to get the corresponding command for other queries
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