from __future__ import annotations

import contextlib
import time
import uuid
from dataclasses import dataclass, field


def new_trace_id() -> str:
    return uuid.uuid4().hex


@dataclass
class Span:
    name: str
    trace_id: str
    start: float = field(default_factory=time.perf_counter)
    end: float | None = None
    error: str | None = None

    @property
    def elapsed_ms(self) -> float:
        current = self.end if self.end is not None else time.perf_counter()
        return round((current - self.start) * 1000, 3)


@contextlib.contextmanager
def span(name: str, trace_id: str | None = None):
    item = Span(name=name, trace_id=trace_id or new_trace_id())
    try:
        yield item
    except Exception as exc:
        item.error = type(exc).__name__
        raise
    finally:
        item.end = time.perf_counter()
