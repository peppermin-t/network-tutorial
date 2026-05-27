from netlab.dns.messages import build_query, parse_message


def main() -> None:
    query = build_query("example.com", "A", transaction_id=7)
    print("query bytes:", query.hex())
    print("This lab's parser is covered by tests/test_dns_messages.py.")
    print("Use `python -m netlab dns query example.com --type A` for a real UDP query.")


if __name__ == "__main__":
    main()
