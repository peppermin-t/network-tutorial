import unittest

from netlab.capture.tshark import build_capture_command, build_read_command


class TSharkCommandTest(unittest.TestCase):
    def test_build_capture_command(self) -> None:
        command = build_capture_command("lo", "out.pcapng", "tcp port 8080", 10)

        self.assertEqual(command, ["tshark", "-i", "lo", "-w", "out.pcapng", "-f", "tcp port 8080", "-c", "10"])

    def test_build_read_command_with_fields(self) -> None:
        command = build_read_command("out.pcapng", "http", ["ip.src", "tcp.dstport"])

        self.assertEqual(command, ["tshark", "-r", "out.pcapng", "-Y", "http", "-T", "fields", "-e", "ip.src", "-e", "tcp.dstport"])


if __name__ == "__main__":
    unittest.main()
