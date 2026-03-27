# BlueIris Scanner
After encountering multiple environments with Blue Iris setups, I decided to write this Python scanner.

## Installation
```bash
git clone https://github.com/Legoclones/blueiris-scanner
cd blueiris-scanner
pip3 install requests
```

## Run
```bash
python3 blueiris_scanner.py -H https://link.to.camera [-u userfile.txt] [-p passwordfile.txt] [-v]
```

If a userfile and password file are passed in, the scanner will also brute force credentials. If either of those files aren't passed it, the credentials won't be brute forced.

## Disclaimer
I don't intend to maintain this tool or ensure it works for newer versions (it was tested on `BlueServer/4.8.6.3`), however if you'd like to contribute feel free to make a pull request!
