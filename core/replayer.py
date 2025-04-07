# core/replayer.py

import requests
from utils.colors import Colors
from utils.helpers import is_payload_reflected

def replay(url, payload):
    target = inject_payload(url, payload)
    print(f"{Colors.OKBLUE}[+] Replaying to: {target}{Colors.ENDC}")

    try:
        res = requests.get(target, timeout=10)
        status = res.status_code
        length = len(res.text)

        print(f"{Colors.OKGREEN}[+] Status Code: {status}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}[+] Response Length: {length}{Colors.ENDC}")

        if is_payload_reflected(res, payload):
            print(f"{Colors.WARNING}[!] Payload terdeteksi di response. [MUNGKIN VULN]{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}[x] Payload tidak muncul di response.{Colors.ENDC}")

    except Exception as e:
        print(f"{Colors.FAIL}[x] Gagal konek: {e}{Colors.ENDC}")

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
