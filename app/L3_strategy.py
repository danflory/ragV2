import logging
from google import genai
from google.genai import types
from .config import CONFIG

# --- Configuration ---
GOOGLE_API_KEY = CONFIG.L3_KEY

# THE STRATEGY ROOT: Gemini 3 Pro (Preview)
# Replaces the old 'gemini-1.5-pro' which caused the 404 error.
MODEL_NAME = "gemini-3-pro-preview" 

logger = logging.getLogger("AGY_L3")

async def ask_gemini_pro(prompt_text: str) -> str:
    """
    L3 Handler: Sends prompt to Google Gemini 3 Pro.
    """
    
    if not GOOGLE_API_KEY:
        logger.error("❌ L3 Key (GOOGLE_API_KEY) missing in .env.")
        return "[System Error: L3 Key Missing]"

    try:
        # Initialize the client with the key
        client = genai.Client(api_key=GOOGLE_API_KEY)
        
        # Use the Async Client (.aio)
        response = await client.aio.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=4096
            )
        )
        
        return response.text

    except Exception as e:
        logger.error(f"L3 (Gemini) Error: {e}")
        return f"[L3 Strategy Error: {str(e)}]"