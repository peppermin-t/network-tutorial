from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EventLogger:
    component: str
    stream: Any = field(default_factory=lambda: sys.stderr)

    def event(self, name: str, **fields: Any) -> None:
        payload = {
            "ts": round(time.time(), 6),
            "component": self.component,
            "event": name,
            **fields,
        }
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True), file=self.stream)
