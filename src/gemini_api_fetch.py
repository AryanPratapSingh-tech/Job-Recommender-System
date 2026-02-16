import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Create model ONCE (best practice)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def ask_Gemini(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
