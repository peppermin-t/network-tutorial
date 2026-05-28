import unittest

from netlab.local.subnet import classify_address, parse_cidr, usable_host_count


class SubnetTest(unittest.TestCase):
    def test_parse_cidr_reports_ipv4_network_details(self) -> None:
        info = parse_cidr("192.168.1.10/24")

        self.assertEqual(info.cidr, "192.168.1.0/24")
        self.assertEqual(info.network_address, "192.168.1.0")
        self.assertEqual(info.broadcast_address, "192.168.1.255")
        self.assertEqual(info.prefix_length, 24)
        self.assertEqual(info.netmask, "255.255.255.0")
        self.assertEqual(info.usable_hosts, 254)
        self.assertTrue(info.is_private)
        self.assertEqual(info.first_usable, "192.168.1.1")
        self.assertEqual(info.last_usable, "192.168.1.254")

    def test_public_private_classification(self) -> None:
        self.assertEqual(classify_address("192.168.1.1"), "private")
        self.assertEqual(classify_address("8.8.8.8"), "public")
        self.assertEqual(classify_address("127.0.0.1"), "loopback")
        self.assertEqual(classify_address("169.254.1.20"), "link-local")

    def test_usable_host_count_handles_small_subnets(self) -> None:
        self.assertEqual(usable_host_count("10.0.0.0/30"), 2)
        self.assertEqual(usable_host_count("10.0.0.0/31"), 2)
        self.assertEqual(usable_host_count("10.0.0.1/32"), 1)


if __name__ == "__main__":
    unittest.main()
