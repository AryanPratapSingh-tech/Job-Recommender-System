import fitz 
import os
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
import requests

#from openai.error import APIConnectionError, APIResponseValidationError, AuthenticationError

#Loading Environment
load_dotenv()
#Loading OpenAI API keys from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

if not OPENAI_API_KEY:
  raise EnvironmentError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_text_from_pdf(pdf_path):
  """
  extracting text from PDF file.
  
  Arguments:
          pdf_path (str): The Path to the pdf file.
          
  Returns:
         str: The extracted text.
      
  """
  document = fitz.open(stream=pdf_path.read(), filetype="pdf")
  text =""

  for page in document:
    text += page.get_text()
  return text


def ask_GPT(prompt, max_tokens=400):
  response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    { "role": "user", "content": prompt }
  ],
  temperature=0.5,
  max_tokens=max_tokens
    )  
  return response.choices[0].message.content.strip()
'''

def ask_llm(prompt, model="llama3"):
  process = subprocess.run(
      ["ollama", "run", model],
      input=prompt,
      text=True,
      capture_output=True
  )
  return process.stdout.strip()


import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_Gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
    return response.text


'''





