import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.tls.simple import https_get


def main() -> None:
    cipher, body = https_get("example.com", 443, "/")
    print("cipher:", cipher)
    print(body[:120].decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
