import google.generativeai as genai
from app.config import GEMINI_API_KEY, GEMINI_MODEL

def init_gemini_model():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(GEMINI_MODEL)

