from netlab.common.retry import RetryPolicy


def main() -> None:
    attempts = {"count": 0}

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise OSError("simulated upstream reset")
        return "ok"

    print(RetryPolicy(max_attempts=3, backoff_seconds=0).run(flaky))
    print("attempts:", attempts["count"])


if __name__ == "__main__":
    main()
