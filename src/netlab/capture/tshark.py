from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class TSharkStatus:
    available: bool
    path: str | None
    version: str | None


def tshark_status() -> TSharkStatus:
    path = shutil.which("tshark")
    if path is None:
        return TSharkStatus(False, None, None)
    try:
        completed = subprocess.run([path, "--version"], capture_output=True, text=True, check=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return TSharkStatus(False, path, None)
    first_line = completed.stdout.splitlines()[0] if completed.stdout else None
    return TSharkStatus(True, path, first_line)


def build_capture_command(interface: str, output: str, capture_filter: str = "", packets: int | None = None) -> list[str]:
    command = ["tshark", "-i", interface, "-w", output]
    if capture_filter:
        command.extend(["-f", capture_filter])
    if packets is not None:
        command.extend(["-c", str(packets)])
    return command


def build_read_command(pcap: str, display_filter: str = "", fields: list[str] | None = None) -> list[str]:
    command = ["tshark", "-r", pcap]
    if display_filter:
        command.extend(["-Y", display_filter])
    if fields:
        command.extend(["-T", "fields"])
        for field in fields:
            command.extend(["-e", field])
    return command


def run_tshark(command: list[str]) -> str:
    completed = subprocess.run(command, capture_output=True, text=True, check=True)
    return completed.stdout
