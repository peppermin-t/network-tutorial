import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.local.commands import format_command_report, run_safe_commands, safety_statement, week01_commands
from netlab.local.subnet import classify_address, format_cidr_report


def main() -> None:
    print(safety_statement())
    print()
    print(format_command_report(run_safe_commands(week01_commands()), "Week01 Local IP/Route/DNS Snapshot"))
    print("# CIDR practice")
    for cidr in ("192.168.1.0/24", "10.20.0.0/20", "172.16.10.0/30"):
        print()
        print(format_cidr_report(cidr))
    print()
    print("# Address classification")
    for address in ("127.0.0.1", "192.168.1.10", "8.8.8.8", "169.254.1.20"):
        print(f"{address}={classify_address(address)}")


if __name__ == "__main__":
    main()
