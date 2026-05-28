import unittest

from netlab.faults.model import classify_failure


class FaultModelTest(unittest.TestCase):
    def test_classifies_retry_storm_as_capacity(self) -> None:
        scenario = classify_failure("retry-storm")

        self.assertEqual(scenario.layer, "Capacity")
        self.assertIn("retry", scenario.expected_client_result)

    def test_core_engineering_failures_are_classified(self) -> None:
        for name in (
            "connection-refused",
            "connect-timeout",
            "read-timeout",
            "upstream-slow",
            "gateway-timeout",
            "retry-storm",
            "http-500",
            "too-many-requests",
        ):
            scenario = classify_failure(name)
            self.assertTrue(scenario.layer)
            self.assertTrue(scenario.symptom)

    def test_rejects_unknown_failure(self) -> None:
        with self.assertRaises(ValueError):
            classify_failure("unknown")


if __name__ == "__main__":
    unittest.main()
