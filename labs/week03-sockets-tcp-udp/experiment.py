import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.sockets.echo import tcp_echo_client, udp_echo_client


def main() -> None:
    print("Start the TCP server on 127.0.0.1:9001 and UDP server on 127.0.0.1:9002 first.")
    print("TCP:", tcp_echo_client("127.0.0.1", 9001, b"week03").decode())
    print("UDP:", udp_echo_client("127.0.0.1", 9002, b"week03").decode())


if __name__ == "__main__":
    main()
