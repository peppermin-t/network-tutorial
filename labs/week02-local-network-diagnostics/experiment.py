import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.local.commands import format_command_report, run_safe_commands, safety_statement, week02_commands


def main() -> None:
    print(safety_statement())
    print()
    print(format_command_report(run_safe_commands(week02_commands()), "Week02 Local Diagnostics Snapshot"))
    print("# Outcome vocabulary")
    print("connection refused = host reachable, TCP stack replied, nothing accepted that port")
    print("connection timeout = no useful reply before timeout; suspect route/firewall/drop/path")
    print("http 500/429 = TCP and HTTP worked; application or capacity layer reported failure")


if __name__ == "__main__":
    main()
