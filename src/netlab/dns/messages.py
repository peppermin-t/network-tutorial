from __future__ import annotations

import random
import socket
import struct
from dataclasses import dataclass


QTYPE = {"A": 1, "CNAME": 5, "AAAA": 28}
QTYPE_NAME = {value: key for key, value in QTYPE.items()}


@dataclass(frozen=True)
class DNSQuestion:
    name: str
    qtype: str
    qclass: int = 1


@dataclass(frozen=True)
class DNSAnswer:
    name: str
    rtype: str
    ttl: int
    value: str


@dataclass(frozen=True)
class DNSMessage:
    transaction_id: int
    questions: list[DNSQuestion]
    answers: list[DNSAnswer]
    rcode: int


def encode_name(name: str) -> bytes:
    parts = name.rstrip(".").split(".")
    encoded = bytearray()
    for part in parts:
        raw = part.encode("ascii")
        if len(raw) > 63:
            raise ValueError("dns label too long")
        encoded.append(len(raw))
        encoded.extend(raw)
    encoded.append(0)
    return bytes(encoded)


def decode_name(data: bytes, offset: int) -> tuple[str, int]:
    labels: list[str] = []
    jumped = False
    next_offset = offset
    seen: set[int] = set()
    while True:
        if offset >= len(data):
            raise ValueError("dns name out of range")
        length = data[offset]
        if length & 0xC0 == 0xC0:
            if offset + 1 >= len(data):
                raise ValueError("dns compression pointer truncated")
            pointer = ((length & 0x3F) << 8) | data[offset + 1]
            if pointer in seen:
                raise ValueError("dns compression pointer loop")
            seen.add(pointer)
            if not jumped:
                next_offset = offset + 2
                jumped = True
            offset = pointer
            continue
        if length == 0:
            offset += 1
            if not jumped:
                next_offset = offset
            break
        offset += 1
        labels.append(data[offset : offset + length].decode("ascii"))
        offset += length
    return ".".join(labels), next_offset


def build_query(name: str, qtype: str = "A", transaction_id: int | None = None) -> bytes:
    qtype = qtype.upper()
    if qtype not in QTYPE:
        raise ValueError(f"unsupported qtype: {qtype}")
    txid = random.randint(0, 0xFFFF) if transaction_id is None else transaction_id
    header = struct.pack("!HHHHHH", txid, 0x0100, 1, 0, 0, 0)
    question = encode_name(name) + struct.pack("!HH", QTYPE[qtype], 1)
    return header + question


def parse_message(data: bytes) -> DNSMessage:
    if len(data) < 12:
        raise ValueError("dns message too short")
    txid, flags, qdcount, ancount, _nscount, _arcount = struct.unpack("!HHHHHH", data[:12])
    offset = 12
    questions: list[DNSQuestion] = []
    answers: list[DNSAnswer] = []
    for _ in range(qdcount):
        name, offset = decode_name(data, offset)
        qtype, qclass = struct.unpack("!HH", data[offset : offset + 4])
        offset += 4
        questions.append(DNSQuestion(name, QTYPE_NAME.get(qtype, str(qtype)), qclass))
    for _ in range(ancount):
        name, offset = decode_name(data, offset)
        rtype, _rclass, ttl, rdlength = struct.unpack("!HHIH", data[offset : offset + 10])
        offset += 10
        rdata = data[offset : offset + rdlength]
        offset += rdlength
        answers.append(DNSAnswer(name, QTYPE_NAME.get(rtype, str(rtype)), ttl, _decode_rdata(data, rtype, rdata, offset - rdlength)))
    return DNSMessage(txid, questions, answers, flags & 0x000F)


def _decode_rdata(message: bytes, rtype: int, rdata: bytes, rdata_offset: int) -> str:
    if rtype == QTYPE["A"] and len(rdata) == 4:
        return socket.inet_ntop(socket.AF_INET, rdata)
    if rtype == QTYPE["AAAA"] and len(rdata) == 16:
        return socket.inet_ntop(socket.AF_INET6, rdata)
    if rtype == QTYPE["CNAME"]:
        name, _ = decode_name(message, rdata_offset)
        return name
    return rdata.hex()
