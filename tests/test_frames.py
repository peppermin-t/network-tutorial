import struct
import unittest

from netlab.protocols.frames import parse_ethernet_frame, parse_ipv4_packet, parse_tcp_segment


class FrameParserTest(unittest.TestCase):
    def test_parse_minimal_ethernet_ipv4_tcp(self) -> None:
        tcp = struct.pack("!HHIIHHHH", 12345, 80, 1, 0, 0x5002, 1024, 0, 0) + b"GET / HTTP/1.1\r\n\r\n"
        ip_header = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(tcp), 0, 0, 64, 6, 0, b"\x0a\x00\x00\x01", b"\x0a\x00\x00\x02")
        ethernet = b"\xaa\xbb\xcc\xdd\xee\xff" + b"\x11\x22\x33\x44\x55\x66" + struct.pack("!H", 0x0800) + ip_header + tcp

        frame = parse_ethernet_frame(ethernet)
        packet = parse_ipv4_packet(frame.payload)
        segment = parse_tcp_segment(packet.payload)

        self.assertEqual(frame.ethertype, 0x0800)
        self.assertEqual(packet.src, "10.0.0.1")
        self.assertEqual(segment.dst_port, 80)
        self.assertTrue(segment.payload.startswith(b"GET"))


if __name__ == "__main__":
    unittest.main()
