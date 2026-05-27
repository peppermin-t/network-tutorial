import unittest

from netlab.common.retry import RetryPolicy


class RetryPolicyTest(unittest.TestCase):
    def test_retries_until_success(self) -> None:
        calls = {"count": 0}

        def operation() -> str:
            calls["count"] += 1
            if calls["count"] < 2:
                raise OSError("temporary")
            return "ok"

        result = RetryPolicy(max_attempts=3, backoff_seconds=0).run(operation)

        self.assertEqual(result, "ok")
        self.assertEqual(calls["count"], 2)

    def test_validates_attempts(self) -> None:
        with self.assertRaises(ValueError):
            RetryPolicy(max_attempts=0).validate()


if __name__ == "__main__":
    unittest.main()
