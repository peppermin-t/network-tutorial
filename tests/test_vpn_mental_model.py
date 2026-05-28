import unittest

from netlab.vpn.mental_model import CommandResult, ObservationCommand, format_snapshot, platform_commands, run_observation_commands


class VpnMentalModelTest(unittest.TestCase):
    def test_platform_command_suggestions_are_not_empty(self) -> None:
        for system in ("Windows", "Linux", "Darwin"):
            self.assertTrue(platform_commands(system))

    def test_commands_do_not_include_network_mutations(self) -> None:
        dangerous_phrases = {
            " route add ",
            " route delete ",
            " ip route add ",
            " ip route del ",
            " flush ",
            " set-dnsclientserveraddress",
            " netsh ",
            " iptables ",
            " nft ",
            " pfctl ",
        }
        for system in ("Windows", "Linux", "Darwin"):
            displays = [command.display.lower() for command in platform_commands(system)]
            for display in displays:
                padded = f" {display} "
                for phrase in dangerous_phrases:
                    self.assertNotIn(phrase, padded)

    def test_missing_command_does_not_crash(self) -> None:
        command = ObservationCommand("missing", ("definitely-not-a-netlab-command",), "missing command test")
        results = run_observation_commands([command], timeout=0.1)

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].available)
        self.assertIn("command not found", results[0].output)

    def test_markdown_snapshot_formatter_is_stable(self) -> None:
        command = ObservationCommand("route table", ("route", "print"), "read routes")
        result = CommandResult(command, True, 0, "default route")

        markdown = format_snapshot([result], "Snapshot")

        self.assertIn("# Snapshot", markdown)
        self.assertIn("## route table", markdown)
        self.assertIn("`route print`", markdown)
        self.assertIn("default route", markdown)


if __name__ == "__main__":
    unittest.main()
