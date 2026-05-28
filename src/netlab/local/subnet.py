from __future__ import annotations

import ipaddress
from dataclasses import dataclass


@dataclass(frozen=True)
class CIDRInfo:
    cidr: str
    network_address: str
    broadcast_address: str | None
    prefix_length: int
    netmask: str
    total_addresses: int
    usable_hosts: int
    is_private: bool
    first_usable: str | None
    last_usable: str | None


def parse_cidr(cidr: str) -> CIDRInfo:
    network = ipaddress.ip_network(cidr, strict=False)
    first_usable, last_usable = _usable_bounds(network)
    return CIDRInfo(
        cidr=str(network),
        network_address=str(network.network_address),
        broadcast_address=str(network.broadcast_address) if network.version == 4 else None,
        prefix_length=network.prefixlen,
        netmask=str(network.netmask),
        total_addresses=network.num_addresses,
        usable_hosts=usable_host_count(cidr),
        is_private=network.is_private,
        first_usable=first_usable,
        last_usable=last_usable,
    )


def usable_host_count(cidr: str) -> int:
    network = ipaddress.ip_network(cidr, strict=False)
    if network.version == 6:
        return network.num_addresses
    if network.prefixlen >= 31:
        return network.num_addresses
    return max(network.num_addresses - 2, 0)


def classify_address(address: str) -> str:
    parsed = ipaddress.ip_address(address)
    if parsed.is_loopback:
        return "loopback"
    if parsed.is_link_local:
        return "link-local"
    if parsed.is_private:
        return "private"
    if parsed.is_multicast:
        return "multicast"
    return "public"


def format_cidr_report(cidr: str) -> str:
    info = parse_cidr(cidr)
    lines = [
        f"cidr={info.cidr}",
        f"network_address={info.network_address}",
        f"broadcast_address={info.broadcast_address or 'n/a'}",
        f"prefix_length={info.prefix_length}",
        f"netmask={info.netmask}",
        f"total_addresses={info.total_addresses}",
        f"usable_hosts={info.usable_hosts}",
        f"private={str(info.is_private).lower()}",
        f"first_usable={info.first_usable or 'n/a'}",
        f"last_usable={info.last_usable or 'n/a'}",
    ]
    return "\n".join(lines)


def _usable_bounds(network: ipaddress.IPv4Network | ipaddress.IPv6Network) -> tuple[str | None, str | None]:
    if network.num_addresses == 0:
        return None, None
    if network.version == 4 and network.prefixlen < 31:
        if network.num_addresses <= 2:
            return None, None
        first = network.network_address + 1
        last = network.broadcast_address - 1
        return str(first), str(last)
    return str(network.network_address), str(network.broadcast_address)
