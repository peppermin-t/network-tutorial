import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.protocols.frames import parse_ethernet_frame, parse_ipv4_packet, parse_tcp_segment
from netlab.protocols.length_prefixed import LengthPrefixedProtocol


def main() -> None:
    raw = LengthPrefixedProtocol.encode(b"first") + LengthPrefixedProtocol.encode(b"second")
    protocol = LengthPrefixedProtocol()
    print("# Length-prefixed stream")
    print("after 3 bytes:", protocol.feed(raw[:3]))
    print("after 8 bytes:", protocol.feed(raw[3:8]))
    print("after rest:", protocol.feed(raw[8:]))

    print()
    print("# Packet/header/payload thinking")
    tcp = struct.pack("!HHIIHHHH", 12345, 80, 1, 0, 0x5002, 1024, 0, 0) + b"GET / HTTP/1.1\r\n\r\n"
    ip = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(tcp), 0, 0, 64, 6, 0, b"\x0a\x00\x00\x01", b"\x0a\x00\x00\x02")
    ethernet = b"\xaa\xbb\xcc\xdd\xee\xff" + b"\x11\x22\x33\x44\x55\x66" + struct.pack("!H", 0x0800) + ip + tcp
    frame = parse_ethernet_frame(ethernet)
    packet = parse_ipv4_packet(frame.payload)
    segment = parse_tcp_segment(packet.payload)
    print(frame)
    print(packet)
    print(segment)


if __name__ == "__main__":
    main()
