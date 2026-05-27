from netlab.http.messages import build_http_request, parse_http_request


def main() -> None:
    raw = build_http_request("POST", "/submit", "localhost", b"name=netlab")
    request = parse_http_request(raw)
    print(request)


if __name__ == "__main__":
    main()
