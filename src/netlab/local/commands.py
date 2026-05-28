from __future__ import annotations

import platform
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class SafeCommand:
    label: str
    argv: tuple[str, ...]
    note: str
    execute_by_default: bool = True

    @property
    def display(self) -> str:
        return " ".join(self.argv)


@dataclass(frozen=True)
class SafeCommandResult:
    command: SafeCommand
    available: bool
    returncode: int | None
    output: str


def week01_commands(system: str | None = None) -> list[SafeCommand]:
    current = _system(system)
    if current == "windows":
        return [
            SafeCommand("ip and dns config", ("ipconfig", "/all"), "Interfaces, IP addresses, DHCP, gateway, DNS servers."),
            SafeCommand("route table", ("route", "print"), "Default route and more-specific routes."),
            SafeCommand("route table compact", ("netstat", "-rn"), "Alternative route table view."),
        ]
    if current == "darwin":
        return [
            SafeCommand("interface config", ("ifconfig",), "Interface addresses and link state."),
            SafeCommand("route table", ("netstat", "-rn"), "Default route and more-specific routes."),
            SafeCommand("dns config", ("scutil", "--dns"), "Resolver and DNS server configuration."),
        ]
    return [
        SafeCommand("interface config", ("ip", "addr"), "Interface addresses and link state."),
        SafeCommand("route table", ("ip", "route"), "Default route and more-specific routes."),
        SafeCommand("dns config", ("resolvectl", "dns"), "Resolver DNS servers if systemd-resolved is present."),
    ]


def week02_commands(system: str | None = None) -> list[SafeCommand]:
    current = _system(system)
    if current == "windows":
        return [
            SafeCommand("arp table", ("arp", "-a"), "Local IP-to-MAC cache."),
            SafeCommand("loopback ping", ("ping", "127.0.0.1"), "ICMP reachability to the local host."),
            SafeCommand("manual traceroute", ("tracert", "example.com"), "Optional route shape to a public test host.", False),
        ]
    if current == "darwin":
        return [
            SafeCommand("arp table", ("arp", "-a"), "Local IP-to-MAC cache."),
            SafeCommand("loopback ping", ("ping", "-c", "2", "127.0.0.1"), "ICMP reachability to the local host."),
            SafeCommand("manual traceroute", ("traceroute", "example.com"), "Optional route shape to a public test host.", False),
        ]
    return [
        SafeCommand("neighbor table", ("ip", "neigh"), "Local neighbor cache; use arp -a if ip is unavailable."),
        SafeCommand("loopback ping", ("ping", "-c", "2", "127.0.0.1"), "ICMP reachability to the local host."),
        SafeCommand("manual traceroute", ("traceroute", "example.com"), "Optional route shape to a public test host.", False),
    ]


def run_safe_commands(commands: list[SafeCommand], timeout: float = 3.0) -> list[SafeCommandResult]:
    results: list[SafeCommandResult] = []
    for command in commands:
        if not command.execute_by_default:
            results.append(SafeCommandResult(command, _available(command.argv[0]), None, "skipped by default; run manually if useful"))
            continue
        if not _available(command.argv[0]):
            results.append(SafeCommandResult(command, False, None, "command not found"))
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
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append(SafeCommandResult(command, True, None, f"{type(exc).__name__}: {exc}"))
            continue
        output = (completed.stdout + completed.stderr).strip()
        results.append(SafeCommandResult(command, True, completed.returncode, output or "(no output)"))
    return results


def format_command_report(results: list[SafeCommandResult], title: str) -> str:
    lines = [f"# {title}", "", f"- Platform: {platform.platform()}", ""]
    for result in results:
        lines.extend(
            [
                f"## {result.command.label}",
                "",
                f"- Command: `{result.command.display}`",
                f"- Note: {result.command.note}",
                f"- Available: {str(result.available).lower()}",
            ]
        )
        if result.returncode is not None:
            lines.append(f"- Return code: {result.returncode}")
        lines.extend(["", "```text", _truncate(result.output), "```", ""])
    return "\n".join(lines).rstrip() + "\n"


def safety_statement() -> str:
    return (
        "These helpers only run read-only observation commands. "
        "They do not change routes, firewall rules, DNS settings, interfaces, or VPN configuration."
    )


def _system(system: str | None) -> str:
    return (system or platform.system()).lower()


def _available(program: str) -> bool:
    return shutil.which(program) is not None


def _truncate(text: str, limit: int = 4000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n... truncated ..."
