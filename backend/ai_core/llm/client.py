import os
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()
class LLMClient:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI API KEY is not configured.")

        self.client = Client(api_key=api_key)

    def generate(self,prompt, model="gemini-2.5-flash"):
        response = self.client.models.generate_content(model=model,contents=prompt)
        
        return response.text

