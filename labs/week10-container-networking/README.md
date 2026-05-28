# Week 10 - Docker and Container Networking

## Goal
Understand Docker network namespaces, bridge networks, Compose service-name DNS, host port versus container port, and why localhost changes meaning.

## Why this matters
Containerized model services, vector DBs, web UIs, gateways, and agents often fail because the caller uses the wrong name, namespace, or port.

## Where this fits
Week05 DNS and Week06 HTTP become concrete in Docker. Week11 applies similar path changes to VPN.

## Before You Run: Concepts
Read [Docker Networking](../../docs/concepts.md#docker-networking), [DNS](../../docs/concepts.md#dns), [Gateway](../../docs/concepts.md#gateway), and [HTTP](../../docs/concepts.md#http).

## Run
Docker is optional for the tutorial core. If available:

```powershell
docker compose -f docker/docker-compose.yml up --build
python -m netlab client http --host 127.0.0.1 --port 18080 --path /from-host
```

Without Docker:

```powershell
python labs/week10-container-networking/experiment.py
```

## Observe
- `gateway` can reach `upstream` by Compose service name.
- Host reaches gateway through published port `18080`.
- `18080:8081` means host port 18080 -> container port 8081.
- `localhost` inside a container is that container, not the host.
- Which services are internal-only and which ports are published.

## Questions
1. Why is container `localhost` not the host machine?
2. Why can Compose service names resolve?
3. In `18080:8081`, what does each side mean?
4. Which ports should be published?
5. Which ports should stay internal-only?

## Notes Checklist
- Draw host -> gateway container -> upstream container.
- List service names and ports.
- Mark published versus internal-only ports.
- Write one wrong-localhost example.

## Work Mapping
This maps to Dockerized AI stacks, local RAG services, reverse proxies, internal databases, container-to-container calls, and development deployments.

## Next Week
Week11 uses the same path thinking for VPN and remote access.

