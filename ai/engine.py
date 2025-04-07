# ai/engine.py

import requests
from utils.colors import Colors

HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_KEY = "PASTE_YOUR_HF_TOKEN_HERE"  # Nanti kamu bisa ganti di .env atau config

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query_hf(prompt):
    payload = {
        "inputs": prompt,
        "options": {"use_cache": True}
    }

    try:
        print(f"{Colors.OKCYAN}[AI] Mengirim prompt ke HuggingFace...{Colors.ENDC}")
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        generated = response.json()

        if isinstance(generated, list):
            return generated[0].get("generated_text", "")
        else:
            return str(generated)
    except Exception as e:
        print(f"{Colors.FAIL}[AI] Gagal query ke HF: {e}{Colors.ENDC}")
        return None
