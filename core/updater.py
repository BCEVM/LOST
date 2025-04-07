# core/updater.py

import os
import subprocess
from utils.colors import Colors

def run_update():
    print(f"{Colors.OKCYAN}[+] Mengecek update dari GitHub...{Colors.ENDC}")
    
    try:
        if os.path.exists(".git"):
            subprocess.run(["git", "pull"], check=True)
            print(f"{Colors.OKGREEN}[+] Tools berhasil diperbarui.{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}[!] Bukan direktori git, tidak bisa update otomatis.{Colors.ENDC}")
            print(f"{Colors.OKBLUE}[i] Clone ulang dari GitHub untuk dapat fitur update.{Colors.ENDC}")
    except subprocess.CalledProcessError:
        print(f"{Colors.FAIL}[x] Gagal update tool. Cek koneksi atau konflik repo.{Colors.ENDC}")
