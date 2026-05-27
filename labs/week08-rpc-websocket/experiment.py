from netlab.rpc.jsonrpc import encode_request, handle_request
from netlab.rpc.websocket import decode_frame, encode_frame


def main() -> None:
    response = handle_request(encode_request("echo", "hello", 1), {"echo": lambda params: params})
    print(response.decode())
    opcode, payload, _ = decode_frame(encode_frame(b"hello websocket"))
    print("frame:", opcode, payload)


if __name__ == "__main__":
    main()
