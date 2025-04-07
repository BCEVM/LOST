# utils/helpers.py

import requests

def get_status_code(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except:
        return None

def get_response_length(url):
    try:
        response = requests.get(url, timeout=10)
        return len(response.text)
    except:
        return 0

def is_payload_reflected(response, payload):
    return payload in response.text
    
def load_payloads_from_file(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []
