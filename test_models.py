from dotenv import load_dotenv
import os
from google import genai

print("Loading API Key...")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ GOOGLE_API_KEY NOT FOUND")
    quit()

client = genai.Client(api_key=api_key)

print("\nAvailable Models:\n")
for m in client.models.list():
    print(m.name)
