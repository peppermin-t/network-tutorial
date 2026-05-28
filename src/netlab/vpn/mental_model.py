from __future__ import annotations

import platform
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class ObservationCommand:
    label: str
    argv: tuple[str, ...]
    note: str
    execute_by_default: bool = True

    @property
    def display(self) -> str:
        return " ".join(self.argv)


@dataclass(frozen=True)
class CommandResult:
    command: ObservationCommand
    available: bool
    returncode: int | None
    output: str


def platform_commands(system: str | None = None) -> list[ObservationCommand]:
    current = (system or platform.system()).lower()
    if current == "windows":
        return [
            ObservationCommand("route table", ("route", "print"), "Shows default route and specific routes."),
            ObservationCommand("ip config", ("ipconfig", "/all"), "Shows interfaces and DNS server settings."),
            ObservationCommand("dns query", ("nslookup", "example.com"), "Tests public DNS resolution."),
            ObservationCommand("route table compact", ("netstat", "-rn"), "Alternative route table view."),
            ObservationCommand("powershell routes", ("powershell", "-NoProfile", "-Command", "Get-NetRoute | Select-Object -First 30"), "PowerShell route view.", False),
            ObservationCommand("powershell dns", ("powershell", "-NoProfile", "-Command", "Get-DnsClientServerAddress | Select-Object -First 30"), "PowerShell DNS server view.", False),
            ObservationCommand("powershell resolve", ("powershell", "-NoProfile", "-Command", "Resolve-DnsName example.com"), "PowerShell DNS query.", False),
            ObservationCommand("traceroute", ("tracert", "example.com"), "Route shape to a public test name.", False),
        ]
    if current == "darwin":
        return [
            ObservationCommand("route table", ("netstat", "-rn"), "Shows default route and specific routes."),
            ObservationCommand("dns config", ("scutil", "--dns"), "Shows resolver configuration."),
            ObservationCommand("dns query", ("dig", "example.com"), "Tests public DNS resolution."),
            ObservationCommand("traceroute", ("traceroute", "example.com"), "Route shape to a public test name.", False),
        ]
    return [
        ObservationCommand("route table", ("ip", "route"), "Shows default route and specific routes."),
        ObservationCommand("dns config", ("resolvectl", "dns"), "Shows systemd-resolved DNS servers."),
        ObservationCommand("dns query", ("dig", "example.com"), "Tests public DNS resolution."),
        ObservationCommand("traceroute", ("traceroute", "example.com"), "Route shape to a public test name.", False),
    ]


def run_observation_commands(commands: list[ObservationCommand] | None = None, timeout: float = 3.0) -> list[CommandResult]:
    results: list[CommandResult] = []
    for command in commands or platform_commands():
        if not command.execute_by_default:
            results.append(CommandResult(command, _is_available(command.argv[0]), None, "skipped by default; run manually if useful"))
            continue
        if not _is_available(command.argv[0]):
            results.append(CommandResult(command, False, None, "command not found"))
            continue
        try:
            completed = subprocess.run(
                command.argv,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                errors="replace",
            )
            output = (completed.stdout + completed.stderr).strip()
            results.append(CommandResult(command, True, completed.returncode, output or "(no output)"))
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append(CommandResult(command, True, None, f"{type(exc).__name__}: {exc}"))
    return results


def format_snapshot(results: list[CommandResult], title: str = "Network Snapshot") -> str:
    lines = [f"# {title}", "", f"- Platform: {platform.platform()}", ""]
    for result in results:
        lines.append(f"## {result.command.label}")
        lines.append("")
        lines.append(f"- Command: `{result.command.display}`")
        lines.append(f"- Note: {result.command.note}")
        lines.append(f"- Available: {str(result.available).lower()}")
        if result.returncode is not None:
            lines.append(f"- Return code: {result.returncode}")
        lines.append("")
        lines.append("```text")
        lines.append(_truncate(result.output))
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def safety_statement() -> str:
    return (
        "This helper only runs read-only observation commands with short timeouts. "
        "It does not modify routes, firewall rules, DNS settings, interfaces, or VPN configuration."
    )


def _is_available(program: str) -> bool:
    return shutil.which(program) is not None


def _truncate(text: str, limit: int = 4000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n... truncated ..."
