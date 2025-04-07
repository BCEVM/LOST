#!/usr/bin/env python3

import argparse
from core import scanner, replayer, updater, crawler, dorker
from utils.colors import banner, info
from utils.colors import Colors, banner

banner()
print(f"{Colors.OKBLUE}[+] Starting scan...{Colors.ENDC}")

def load_payloads_from_file(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []
        
def main():
    banner()

    parser = argparse.ArgumentParser(description="LOST - Lightweight Offensive Scanner Tool")
    parser.add_argument('--url', help='Target URL (e.g. http://target.com/page.php?id=1)')
    parser.add_argument('--scan', action='store_true', help='Scan target for common vulns')
    parser.add_argument('--replay', action='store_true', help='Replay URL with payload')
    parser.add_argument('--payload', help='Manual payload for replay')
    parser.add_argument('--update', action='store_true', help='Update tool from GitHub')
    parser.add_argument('--stealth', action='store_true', help='Use stealth mode (random UA, delay, proxy)')
    parser.add_argument('--dork', help='Search targets using dork')
    parser.add_argument('--crawl', action='store_true', help='Crawl target for internal URLs')

    args = parser.parse_args()

    if args.update:
        updater.update_tool()
        return

    if args.dork:
        dorker.search_dorks(args.dork)
        return

    if args.crawl and args.url:
        crawler.crawl(args.url)
        return

    if args.replay and args.url and args.payload:
        replayer.replay_mode(args.url, args.payload)
        return

    if args.scan and args.url:
        scanner.scan_vulns(args.url, stealth=args.stealth)
        return
    parser.add_argument('--ai', help='Prompt untuk AI (HuggingFace)', required=False)
    if args.ai:
    from ai.engine import query_hf
    result = query_hf(args.ai)
    if result:
        print(f"\n{Colors.OKGREEN}[AI Response]:{Colors.ENDC}\n{result}")
    else:
        print(f"{Colors.FAIL}[x] Gagal mendapatkan respon dari AI.{Colors.ENDC}")
    sys.exit()
    
    parser.print_help()

if __name__ == "__main__":
    main()
