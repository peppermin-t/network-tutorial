from netlab.sockets.echo import tcp_echo_client, udp_echo_client


def main() -> None:
    print("Start the TCP and UDP echo servers from README first.")
    print("TCP:", tcp_echo_client("127.0.0.1", 9001, b"week01").decode())
    print("UDP:", udp_echo_client("127.0.0.1", 9002, b"week01").decode())


if __name__ == "__main__":
    main()
