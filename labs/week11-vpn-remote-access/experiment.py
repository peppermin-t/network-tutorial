import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.vpn.mental_model import format_snapshot, platform_commands, run_observation_commands, safety_statement


def main() -> None:
    commands = platform_commands()
    print(safety_statement())
    print()
    print("Suggested read-only commands:")
    for command in commands:
        marker = "auto" if command.execute_by_default else "manual"
        print(f"- [{marker}] {command.display} - {command.note}")
    print()
    print(format_snapshot(run_observation_commands(commands), "VPN Mental Model Snapshot"))


if __name__ == "__main__":
    main()
