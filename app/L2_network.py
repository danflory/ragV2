import httpx
import logging
from .config import CONFIG

# --- Configuration ---
API_KEY = CONFIG.L2_KEY
BASE_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

# THE BEAST: Qwen 3 Coder 480B Turbo (MoE)
# Cost: ~$1.20/1M output (Cheaper than GPT-5 Mini, Smarter than 32B)
# 35B Active Parameters means it is fast, but access to 480B knowledge.
CLOUD_MODEL_NAME = "Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo"

logger = logging.getLogger("AGY_L2")

async def ask_gpt_mini(prompt_text: str) -> str:
    """
    L2 Handler: Sends prompt to Qwen 3 Coder 480B Turbo.
    This is a 'Senior Engineer' class model acting as your Critic.
    """
    
    if not API_KEY:
        logger.error("❌ L2 Key (DEEPINFRA_API_KEY) missing in .env")
        return "[System Error: L2 Key Missing]"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": CLOUD_MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful, expert coding assistant. You are critical and precise."},
            {"role": "user", "content": prompt_text}
        ],
        # MoE models like slightly higher temp to engage the right experts
        "temperature": 0.6, 
        "max_tokens": 4096
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(BASE_URL, headers=headers, json=payload)
            
            if response.status_code != 200:
                logger.error(f"L2 DeepInfra Error {response.status_code}: {response.text}")
                return f"[L2 Error: {response.status_code} - {response.text}]"

            data = response.json()
            # This model often uses <think> tags. We pass them through 
            # so you can see its reasoning in the logs.
            return data["choices"][0]["message"]["content"]

    except Exception as e:
        logger.error(f"L2 Exception: {e}")
        return f"[L2 Error: {str(e)}]"