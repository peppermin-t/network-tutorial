from __future__ import annotations

import ipaddress
import struct
from dataclasses import dataclass


@dataclass(frozen=True)
class EthernetFrame:
    dst_mac: str
    src_mac: str
    ethertype: int
    payload: bytes


@dataclass(frozen=True)
class IPv4Packet:
    src: str
    dst: str
    protocol: int
    ttl: int
    payload: bytes


@dataclass(frozen=True)
class TCPSegment:
    src_port: int
    dst_port: int
    seq: int
    ack: int
    flags: int
    payload: bytes


@dataclass(frozen=True)
class UDPDatagram:
    src_port: int
    dst_port: int
    length: int
    payload: bytes


def _mac(raw: bytes) -> str:
    return ":".join(f"{b:02x}" for b in raw)


def parse_ethernet_frame(data: bytes) -> EthernetFrame:
    if len(data) < 14:
        raise ValueError("ethernet frame too short")
    dst, src, ethertype = struct.unpack("!6s6sH", data[:14])
    return EthernetFrame(_mac(dst), _mac(src), ethertype, data[14:])


def parse_ipv4_packet(data: bytes) -> IPv4Packet:
    if len(data) < 20:
        raise ValueError("ipv4 packet too short")
    first, _, total_length, _, _, ttl, protocol, _, src, dst = struct.unpack("!BBHHHBBH4s4s", data[:20])
    version = first >> 4
    ihl = (first & 0x0F) * 4
    if version != 4:
        raise ValueError(f"not ipv4: version={version}")
    if len(data) < total_length:
        raise ValueError("ipv4 packet truncated")
    return IPv4Packet(str(ipaddress.IPv4Address(src)), str(ipaddress.IPv4Address(dst)), protocol, ttl, data[ihl:total_length])


def parse_tcp_segment(data: bytes) -> TCPSegment:
    if len(data) < 20:
        raise ValueError("tcp segment too short")
    src_port, dst_port, seq, ack, offset_flags = struct.unpack("!HHIIH", data[:14])
    data_offset = (offset_flags >> 12) * 4
    flags = offset_flags & 0x01FF
    return TCPSegment(src_port, dst_port, seq, ack, flags, data[data_offset:])


def parse_udp_datagram(data: bytes) -> UDPDatagram:
    if len(data) < 8:
        raise ValueError("udp datagram too short")
    src_port, dst_port, length, _checksum = struct.unpack("!HHHH", data[:8])
    if len(data) < length:
        raise ValueError("udp datagram truncated")
    return UDPDatagram(src_port, dst_port, length, data[8:length])
