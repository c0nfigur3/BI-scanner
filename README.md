# BI-scanner

**Modern Blue Iris JSON brute-force + enumeration scanner (Python 3)**  
Works on Blue Iris 5.x/6.x with or without “Use secure session keys”.

**Repo:** https://github.com/c0nfigur3/BI-scanner  
**Author:** c0nfigur3

### Original Credit
This project is a **complete modernization** of the original [Legoclones/blueiris-scanner](https://github.com/Legoclones/blueiris-scanner).  

The legacy script worked great on Blue Iris 4.x but failed with errors on the updated JSON `cmd=login` flow in newer versions. After hitting this issue across multiple real-world BI environments, I rewrote the core login logic (correct MD5 challenge-response `username:session:password`, proper `.json()` handling, argparse, delay control, etc.) while keeping the original tool’s fast and lightweight spirit.

### Features
- Anonymous access detection
- Native `cmd=login` challenge-response
- Returns usable session token for full API access (cameras, alerts, config, etc.)
- Built-in delay to avoid IP bans
- Clean argparse CLI
- Ready for GitHub versioning and community contributions

### Installation
```bash
git clone https://github.com/c0nfigur3/BI-scanner.git
cd BI-scanner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
