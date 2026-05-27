def main() -> None:
    print("Run: docker compose -f docker/docker-compose.yml up --build")
    print("Then call: python -m netlab client http --host 127.0.0.1 --port 18080 --path /from-host")


if __name__ == "__main__":
    main()
