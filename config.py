import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AUDIO_DIR = "audio"
MODEL_NAME = "gemini-2.5-flash"
TEMPERATURE = 0.7
LANGUAGE = "en-US"