import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Fetch API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in .env file")

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
    model="gpt-5-nano",
    input="Write a haiku about AI",
    store=True
)

print(response.output_text)
