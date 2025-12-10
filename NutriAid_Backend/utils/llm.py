import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/gemini-2.5-flash"

def ask_gemini(prompt):
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    return response.text
