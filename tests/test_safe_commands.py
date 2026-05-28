import unittest

from netlab.local.commands import SafeCommand, run_safe_commands, week01_commands, week02_commands


class SafeCommandsTest(unittest.TestCase):
    def test_week01_and_week02_command_suggestions_are_not_empty(self) -> None:
        for system in ("Windows", "Linux", "Darwin"):
            self.assertTrue(week01_commands(system))
            self.assertTrue(week02_commands(system))

    def test_week01_and_week02_commands_do_not_include_mutations(self) -> None:
        dangerous_phrases = {
            " route add ",
            " route delete ",
            " ip route add ",
            " ip route del ",
            " netsh ",
            " set-dnsclientserveraddress ",
            " iptables ",
            " nft ",
            " pfctl ",
            " firewall-cmd ",
        }
        for factory in (week01_commands, week02_commands):
            for system in ("Windows", "Linux", "Darwin"):
                for command in factory(system):
                    padded = f" {command.display.lower()} "
                    for phrase in dangerous_phrases:
                        self.assertNotIn(phrase, padded)

    def test_missing_command_does_not_crash(self) -> None:
        command = SafeCommand("missing", ("definitely-not-a-netlab-command",), "missing command test")
        results = run_safe_commands([command], timeout=0.1)

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].available)
        self.assertIn("command not found", results[0].output)


if __name__ == "__main__":
    unittest.main()
