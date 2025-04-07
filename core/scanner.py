# core/scanner.py

import requests
from utils.colors import Colors
from utils.helpers import get_status_code, get_response_length, is_payload_reflected
from utils.helpers import load_payloads_from_file

PAYLOADS = {
    "XSS": load_payloads_from_file("payloads/xss.txt"),
    "SQLi": load_payloads_from_file("payloads/sqli.txt"),
    "LFI": load_payloads_from_file("payloads/lfi.txt")
}

# Payload dasar (nanti bisa ditaruh di file atau modul payload terpisah)
PAYLOADS = {
    "XSS": ['<script>alert(1)</script>', '" onerror=alert(1) ', "'><svg/onload=alert(1)>"],
    "SQLi": ["'", "' OR 1=1--", '" OR "1"="1'],
    "LFI": ["../../../../etc/passwd", "..%2F..%2F..%2Fetc%2Fpasswd"]
}

def scan(url):
    print(f"{Colors.OKCYAN}[+] Starting vulnerability scan for: {url}{Colors.ENDC}")

    for vuln_type, payloads in PAYLOADS.items():
        print(f"{Colors.HEADER}[*] Testing for {vuln_type}...{Colors.ENDC}")
        for payload in payloads:
            target = inject_payload(url, payload)
            try:
                res = requests.get(target, timeout=10)
                status = res.status_code
                length = len(res.text)
                reflected = is_payload_reflected(res, payload)

                print(f"{Colors.OKBLUE}[+] Replaying to: {target}{Colors.ENDC}")
                print(f"{Colors.OKGREEN}[+] Status Code: {status}{Colors.ENDC}")
                print(f"{Colors.OKCYAN}[+] Response Length: {length}{Colors.ENDC}")

                if reflected:
                    print(f"{Colors.WARNING}[!] Payload terdeteksi di response. [MUNGKIN VULN]{Colors.ENDC}")
            except:
                print(f"{Colors.FAIL}[x] Gagal konek ke {target}{Colors.ENDC}")

def inject_payload(url, payload):
    if "?" in url and "=" in url:
        base, param = url.split("?", 1)
        param_pairs = param.split("&")
        injected = []
        for pair in param_pairs:
            if "=" in pair:
                k, v = pair.split("=", 1)
                injected.append(f"{k}={payload}")
            else:
                injected.append(pair)
        return f"{base}?{'&'.join(injected)}"
    else:
        return f"{url}?payload={payload}"
