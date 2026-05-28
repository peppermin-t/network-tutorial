import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.common.retry import RetryPolicy
from netlab.faults.model import classify_failure


def main() -> None:
    print("transient failure retry success")
    attempts = {"count": 0}

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise OSError("simulated upstream reset")
        return "ok"

    policy = RetryPolicy(max_attempts=3, backoff_seconds=0)
    print("result:", policy.run(flaky))
    print("attempts:", attempts["count"])

    print()
    print("slow operation retry risk")
    slow_attempts = {"count": 0}

    def slow_then_timeout() -> str:
        slow_attempts["count"] += 1
        time.sleep(0.02)
        raise TimeoutError("simulated read timeout after upstream work started")

    started = time.perf_counter()
    try:
        policy.run(slow_then_timeout, retry_on=(TimeoutError,))
    except TimeoutError as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        print("result:", type(exc).__name__)
        print("attempts:", slow_attempts["count"])
        print("elapsed_ms:", elapsed_ms)
        print("risk: retrying slow model work can multiply upstream/GPU load if earlier attempts are still running")

    print()
    print("layer classification hints")
    for name in ("connection-refused", "read-timeout", "upstream-slow", "gateway-timeout", "retry-storm", "too-many-requests"):
        scenario = classify_failure(name)
        print(f"{scenario.name}: layer={scenario.layer}; expected={scenario.expected_client_result}")


if __name__ == "__main__":
    main()
