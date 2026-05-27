from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    timeout_seconds: float = 1.0
    backoff_seconds: float = 0.1

    def validate(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        if self.backoff_seconds < 0:
            raise ValueError("backoff_seconds must be >= 0")

    def run(self, operation: Callable[[], T], retry_on: tuple[type[BaseException], ...] = (OSError,)) -> T:
        self.validate()
        last_error: BaseException | None = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                return operation()
            except retry_on as exc:
                last_error = exc
                if attempt == self.max_attempts:
                    break
                time.sleep(self.backoff_seconds * attempt)
        assert last_error is not None
        raise last_error
