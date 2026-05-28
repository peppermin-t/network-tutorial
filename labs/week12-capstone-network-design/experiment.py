import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.observability.metrics import Metrics
from netlab.observability.trace import span


def main() -> None:
    metrics = Metrics()
    with span("capstone-request") as item:
        metrics.increment("requests.total")
        metrics.increment("model_like_requests.total")
    print(f"trace_id={item.trace_id} elapsed_ms={item.elapsed_ms}")
    print(metrics.render_prometheus())
    print("Design task: complete docs/network-design-template.md for one of the three Week12 scenarios.")


if __name__ == "__main__":
    main()
