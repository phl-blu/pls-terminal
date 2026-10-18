from google import genai
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client =  genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="give me the command for windows on how to find my network protocols. just the command, no explanation neeeded. return in 1 line.",
)

response_text = response.text.replace("`","")
response_text = response_text.replace("'","")

result = subprocess.run(response_text, check=True, shell=True)
