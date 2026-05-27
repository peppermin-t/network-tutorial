from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Metrics:
    counters: Counter[str] = field(default_factory=Counter)

    def increment(self, name: str, value: int = 1) -> None:
        self.counters[name] += value

    def render_prometheus(self) -> str:
        lines = []
        for name, value in sorted(self.counters.items()):
            safe = name.replace(".", "_").replace("-", "_")
            lines.append(f"# TYPE {safe} counter")
            lines.append(f"{safe} {value}")
        return "\n".join(lines) + ("\n" if lines else "")
