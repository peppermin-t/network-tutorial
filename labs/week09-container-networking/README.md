# Week 09 - Container Networking

Focus: Docker Compose, service name DNS, bridge network, port mapping, network isolation.

## Before You Run: Concepts

- `Container network namespace`: each container has its own network view. See `docs/concepts.md#container-network-namespace`.
- `Bridge network`: the virtual network connecting Compose services. See `docs/concepts.md#bridge-network`.
- `Service name`: Docker Compose DNS name. See `docs/concepts.md#service-name`.
- `Port mapping`: host port forwarded to container port. See `docs/concepts.md#port-mapping`.
- `Why localhost inside a container is not the host`: loopback is namespace-local. See `docs/concepts.md#why-localhost-inside-a-container-is-not-the-host`.

## If You Are Confused

- If host can connect but a container cannot, compare host port, container port, and service name.
- If `localhost` fails inside a container, read `container network namespace`.
- If service names work in Compose but not on the host, read `Docker Compose service name DNS`.

Run:

```powershell
docker compose -f docker/docker-compose.yml up --build
```

Then from host:

```powershell
$env:PYTHONPATH="src"
python -m netlab client http --host 127.0.0.1 --port 18080 --path /from-host
```

Questions:

- host 访问容器和容器访问容器分别用什么地址？
- Compose service name 为什么能解析？
- 端口映射和容器内部监听端口是什么关系？

Wireshark task:

- Capture host-side traffic on published port `18080`.
- Inside Docker, compare service names `gateway` and `upstream` with host address `127.0.0.1`.
- Record which packets are visible from the host and which require container/network namespace inspection.

## Systematic Template

- Concept Model: Name Resolution -> Connection in an isolated network.
- Code Lab: Run Docker Compose with client, gateway, and upstream.
- Failure Lab: Use the wrong host/port or service name; classify as DNS or TCP depending on the observed error.
- Wireshark Lab: Capture host-side `tcp port 18080` and compare with container logs.
- Work Mapping: Cloud networking and local multi-container model deployments both depend on naming, routing, and port mapping.
