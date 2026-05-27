from netlab.protocols.length_prefixed import LengthPrefixedProtocol


def main() -> None:
    raw = LengthPrefixedProtocol.encode(b"first") + LengthPrefixedProtocol.encode(b"second")
    protocol = LengthPrefixedProtocol()
    print("after 3 bytes:", protocol.feed(raw[:3]))
    print("after 8 bytes:", protocol.feed(raw[3:8]))
    print("after rest:", protocol.feed(raw[8:]))


if __name__ == "__main__":
    main()
