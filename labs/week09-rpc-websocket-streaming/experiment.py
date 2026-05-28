import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from netlab.rpc.jsonrpc import encode_request, handle_request
from netlab.rpc.websocket import decode_frame, encode_frame


def main() -> None:
    response = handle_request(encode_request("echo", "hello", 1), {"echo": lambda params: params})
    print(response.decode())
    opcode, payload, _ = decode_frame(encode_frame(b"hello websocket"))
    print("frame:", opcode, payload)
    print("Use `python -m netlab client stream-http ...` against a streaming endpoint to compare first_byte_ms and total_ms.")


if __name__ == "__main__":
    main()
