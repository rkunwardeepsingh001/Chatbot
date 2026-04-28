import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set in the environment. Add it to .env or export it before running.")

def get_ai_response(user_message):
    genai.configure(api_key=API_KEY)

    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        chat = model.start_chat()
        response = chat.send_message(user_message)
        return response.text
    except ResourceExhausted:
        return "The Gemini API limit exceeded. Please try again later."
    except Exception:
        return "The AI service is currently unavailable. Please try again later."
