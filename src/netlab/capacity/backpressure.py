from __future__ import annotations

import statistics
import threading
import time
from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class BackpressureDecision:
    accepted: bool
    status_code: int
    reason: str
    layer: str = "Capacity"


class BackpressureGate:
    """A small semaphore-backed capacity gate for server-side experiments."""

    def __init__(self, max_concurrency: int) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be >= 1")
        self.max_concurrency = max_concurrency
        self._semaphore = threading.BoundedSemaphore(max_concurrency)
        self._in_flight = 0
        self._lock = threading.Lock()

    @property
    def in_flight(self) -> int:
        with self._lock:
            return self._in_flight

    def try_acquire(self) -> BackpressureDecision:
        if not self._semaphore.acquire(blocking=False):
            return BackpressureDecision(False, 429, "Too Many Requests")
        with self._lock:
            self._in_flight += 1
        return BackpressureDecision(True, 200, "OK")

    def release(self) -> None:
        with self._lock:
            if self._in_flight <= 0:
                raise RuntimeError("release called without acquire")
            self._in_flight -= 1
        self._semaphore.release()


@dataclass(frozen=True)
class LoadResult:
    total: int
    successes: int
    failures: int
    timeouts: int
    p50_ms: float
    p95_ms: float


def run_concurrent_load(requests: int, concurrency: int, operation: Callable[[], int]) -> LoadResult:
    if requests < 1:
        raise ValueError("requests must be >= 1")
    if concurrency < 1:
        raise ValueError("concurrency must be >= 1")

    latencies: list[float] = []
    statuses: list[int | None] = []
    lock = threading.Lock()
    next_index = 0

    def worker() -> None:
        nonlocal next_index
        while True:
            with lock:
                if next_index >= requests:
                    return
                next_index += 1
            started = time.perf_counter()
            status: int | None
            try:
                status = operation()
            except TimeoutError:
                status = None
            except OSError:
                status = 0
            elapsed_ms = (time.perf_counter() - started) * 1000
            with lock:
                latencies.append(elapsed_ms)
                statuses.append(status)

    threads = [threading.Thread(target=worker) for _ in range(min(concurrency, requests))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    sorted_latencies = sorted(latencies)
    p50 = statistics.median(sorted_latencies)
    p95 = sorted_latencies[max(0, min(len(sorted_latencies) - 1, int(len(sorted_latencies) * 0.95) - 1))]
    successes = sum(1 for status in statuses if status is not None and 200 <= status < 400)
    timeouts = sum(1 for status in statuses if status is None)
    return LoadResult(len(statuses), successes, len(statuses) - successes, timeouts, round(p50, 3), round(p95, 3))
