# BI-scanner

**Modern Blue Iris JSON brute-force + enumeration scanner (Python 3)**  
Works on Blue Iris 5.x/6.x with or without “Use secure session keys”.

**Repo:** https://github.com/c0nfigur3/BI-scanner  
**Author:** c0nfigur3

### Original Credit
This project is a **complete modernization** of the original [Legoclones/blueiris-scanner](https://github.com/Legoclones/blueiris-scanner).  

The legacy script worked great on Blue Iris 4.x but failed on the updated JSON `cmd=login` flow. After hitting this issue across multiple real-world BI environments, the core login logic was rewritten (correct MD5 `username:session:password`, proper `.json()` handling, argparse, delay control, etc.) while keeping the original tool’s fast and lightweight spirit.

### Features
- Anonymous access detection
- Native `cmd=login` challenge-response
- Returns usable session token for full API access
- Built-in delay to avoid IP bans
- Dynamic combo mode (`-c`) + `--try-user-as-pass`
- Full native support for Kali’s `rockyou.txt.gz`
- Installable as a proper CLI command (`blue-i`)

### Installation (Kali / Linux)
```bash
git clone https://github.com/c0nfigur3/BI-scanner.git
cd BI-scanner
python3 -m venv venv
source venv/bin/activate
pip install -e .
