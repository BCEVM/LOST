import requests
import os
from dotenv import load_dotenv
from utils.colors import Colors

# Baca file .env
load_dotenv()

# Ambil API key dari file .env
HF_API_KEY = os.getenv("HF_API_KEY")
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query_hf(prompt):
    if not HF_API_KEY:
        print(f"{Colors.FAIL}[AI] HF_API_KEY tidak ditemukan di .env{Colors.ENDC}")
        return None

    payload = {
        "inputs": prompt,
        "options": {"use_cache": True}
    }

    try:
        print(f"{Colors.OKCYAN}[AI] Mengirim prompt ke HuggingFace...{Colors.ENDC}")
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "")
        else:
            return str(result)
    except Exception as e:
        print(f"{Colors.FAIL}[AI] Gagal query ke HF: {e}{Colors.ENDC}")
        return None
