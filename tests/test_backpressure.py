import time
import unittest

from netlab.capacity.backpressure import BackpressureGate, run_concurrent_load


class BackpressureTest(unittest.TestCase):
    def test_gate_rejects_when_full(self) -> None:
        gate = BackpressureGate(max_concurrency=1)

        first = gate.try_acquire()
        second = gate.try_acquire()
        gate.release()
        third = gate.try_acquire()
        gate.release()

        self.assertTrue(first.accepted)
        self.assertFalse(second.accepted)
        self.assertEqual(second.status_code, 429)
        self.assertTrue(third.accepted)

    def test_concurrent_load_counts_success_and_timeout(self) -> None:
        calls = {"count": 0}

        def operation() -> int:
            calls["count"] += 1
            if calls["count"] == 2:
                raise TimeoutError("simulated timeout")
            time.sleep(0.001)
            return 200

        result = run_concurrent_load(requests=4, concurrency=2, operation=operation)

        self.assertEqual(result.total, 4)
        self.assertEqual(result.successes, 3)
        self.assertEqual(result.timeouts, 1)
        self.assertEqual(result.failures, 1)


if __name__ == "__main__":
    unittest.main()
