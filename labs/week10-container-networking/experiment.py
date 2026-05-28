def main() -> None:
    print("Run: docker compose -f docker/docker-compose.yml up --build")
    print("Then call from host: python -m netlab client http --host 127.0.0.1 --port 18080 --path /from-host")
    print("Inside Compose, client calls gateway:8081 and gateway calls upstream:8080 by service name.")
    print("Mental model: host port 18080 -> gateway container port 8081 -> upstream service name port 8080.")


if __name__ == "__main__":
    main()

