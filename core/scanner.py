import os
import requests
from utils.colors import Colors
from utils.helpers import is_payload_reflected, load_payloads_from_file

def inject_payload(url, payload):
    if "?" in url and "=" in url:
        base, param = url.split("?", 1)
        param_pairs = param.split("&")
        injected = []
        for pair in param_pairs:
            if "=" in pair:
                k, _ = pair.split("=", 1)
                injected.append(f"{k}={payload}")
            else:
                injected.append(pair)
        return f"{base}?{'&'.join(injected)}"
    else:
        return f"{url}?payload={payload}"

def load_payloads(folder="payloads"):
    payloads = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            with open(path, "r") as f:
                payloads.extend([line.strip() for line in f if line.strip()])
    return payloads

def scan_url_with_payloads(url, payloads):
    for payload in payloads:
        target = url.replace("FUZZ", payload)
        try:
            res = requests.get(target, timeout=5)
            print(f"{Colors.OKBLUE}[+] Testing: {target}{Colors.ENDC}")
            if payload in res.text:
                print(f"{Colors.OKGREEN}[VULNERABLE] Payload: {payload}{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}[NOT VULNERABLE] Payload: {payload}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}[x] Error: {e}{Colors.ENDC}")

def scan_target(url, payload_list):
    for payload in payload_list:
        test_url = url.replace("FUZZ", payload.strip())
        try:
            res = requests.get(test_url, timeout=5)
            print(f"{Colors.OKBLUE}[+] Replaying to: {test_url}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}[+] Status Code: {res.status_code}")
            print(f"[+] Response Length: {len(res.text)}{Colors.ENDC}")
            if payload.strip() in res.text:
                print(f"{Colors.WARNING}[!] Payload terdeteksi di response. [MUNGKIN VULN]{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}[x] Error saat request: {e}{Colors.ENDC}")

def scan_vulns(url, stealth=False):
    payloads = load_payloads()
    print(f"{Colors.OKCYAN}[+] Starting vulnerability scan for: {url}{Colors.ENDC}")
    scan_url_with_payloads(url, payloads)
