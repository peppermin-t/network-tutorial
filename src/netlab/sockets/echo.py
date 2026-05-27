from __future__ import annotations

import socket
import threading
from contextlib import closing

from netlab.common.logging import EventLogger


def run_tcp_echo_server(host: str, port: int, stop_after_one: bool = False) -> None:
    logger = EventLogger("tcp-echo-server")
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        logger.event("listening", host=host, port=port)
        while True:
            conn, addr = server.accept()
            logger.event("accepted", remote=f"{addr[0]}:{addr[1]}")
            thread = threading.Thread(target=_handle_tcp_client, args=(conn, addr, logger), daemon=True)
            thread.start()
            if stop_after_one:
                thread.join()
                return


def _handle_tcp_client(conn: socket.socket, addr: tuple[str, int], logger: EventLogger) -> None:
    remote = f"{addr[0]}:{addr[1]}"
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                logger.event("closed", remote=remote)
                return
            logger.event("received", remote=remote, bytes=len(data))
            conn.sendall(data)


def tcp_echo_client(host: str, port: int, message: bytes, timeout: float = 3.0) -> bytes:
    with closing(socket.create_connection((host, port), timeout=timeout)) as sock:
        sock.settimeout(timeout)
        sock.sendall(message)
        return sock.recv(4096)


def run_udp_echo_server(host: str, port: int, stop_after_one: bool = False) -> None:
    logger = EventLogger("udp-echo-server")
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as server:
        server.bind((host, port))
        logger.event("listening", host=host, port=port)
        while True:
            data, addr = server.recvfrom(65535)
            logger.event("received", remote=f"{addr[0]}:{addr[1]}", bytes=len(data))
            server.sendto(data, addr)
            if stop_after_one:
                return


def udp_echo_client(host: str, port: int, message: bytes, timeout: float = 3.0) -> bytes:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
        sock.settimeout(timeout)
        sock.sendto(message, (host, port))
        data, _ = sock.recvfrom(65535)
        return data
