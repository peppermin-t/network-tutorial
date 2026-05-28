# Concepts

This file is a lightweight field guide for the labs. Read the relevant section before running a lab, then verify the idea with logs, HTTP output, and packets.

## Host / Port

### Mental model
A host names a machine or interface; a port names one listening application endpoint on that host.

### Why it matters here
Week01 starts every network experiment by choosing a host and port. Week09 adds container hostnames and port mapping.

### What to observe
Run a server on `127.0.0.1:9001`, connect a client to the same pair, then try the wrong port. In packet capture, the port numbers identify the conversation.

### Common confusion
`localhost` is not "the whole network"; it means the current network namespace. Inside a container, it usually means the container itself.

### AI/LLM engineering mapping
Local model servers, vector databases, gateways, and agents all reduce to "which host and port am I really calling?"

### Related labs
Week01, Week09, Week10.

## Socket

### Mental model
A socket is the process API for sending and receiving bytes or datagrams through the OS network stack.

### Why it matters here
The repository intentionally starts with Python sockets so HTTP, DNS, proxy, and model-like streaming do not feel magical later.

### What to observe
Look at `bind`, `listen`, `accept`, `connect`, `sendall`, `recv`, and `recvfrom` in Week01 and Week02.

### Common confusion
`recv(4096)` means "up to 4096 bytes", not "one complete application message".

### AI/LLM engineering mapping
Even high-level SDK calls eventually become socket reads and writes with timeout behavior.

### Related labs
Week01, Week02, Week05, Week06, Week10.

## TCP

### Mental model
TCP gives applications a reliable ordered byte stream between two endpoints.

### Why it matters here
Week01 uses TCP echo; Week02 shows why a byte stream still needs application framing.

### What to observe
Capture `tcp port 9001`: handshake, payload, acknowledgments, and connection teardown. Notice that payload boundaries may not match application messages.

### Common confusion
TCP is reliable transport, not a message protocol. It does not know where JSON, HTTP, or model tokens start and end.

### AI/LLM engineering mapping
Slow model responses and gateway read timeouts usually happen after TCP is already connected.

### Related labs
Week01, Week02, Week05, Week06, Week10.

## UDP

### Mental model
UDP sends independent datagrams without connection setup, delivery guarantee, or stream semantics.

### Why it matters here
Week01 compares UDP echo with TCP echo. Week04 DNS uses UDP for normal queries.

### What to observe
There is no `listen`/`accept` connection lifecycle. A DNS query is one datagram out and, ideally, one response datagram back.

### Common confusion
UDP is not "bad TCP"; it is a different contract where the application handles loss and retry.

### AI/LLM engineering mapping
DNS failures often show up before HTTP or TLS exists, and they may be UDP timeout problems.

### Related labs
Week01, Week04.

## TCP Handshake

### Mental model
Before TCP carries data, client and server agree on a connection with SYN, SYN/ACK, and ACK.

### Why it matters here
Week01 packet capture makes the connection lifecycle visible.

### What to observe
In Wireshark, use `tcp.flags.syn == 1` or `tcp.port == 9001`. A refused connection usually shows a reset instead of an accepted handshake.

### Common confusion
An HTTP 500 or 429 means the TCP handshake already succeeded; those are higher-layer outcomes.

### AI/LLM engineering mapping
When a local model endpoint says connection refused, the process may not be listening or the port mapping is wrong. That is different from a slow generation.

### Related labs
Week01, Week06, Week09, Week10.

## Connection Lifecycle

### Mental model
A TCP connection moves from connect, data transfer, and close through OS state; UDP does not have this connection lifecycle.

### Why it matters here
Week01 asks what the server sees when the client exits. Week05 and Week10 use `Connection: close` to simplify response reading.

### What to observe
Capture FIN/RST packets and compare graceful close with early close in Week06 fault server mode.

### Common confusion
A closed application connection is not the same thing as a failed DNS lookup or a failed TLS certificate check.

### AI/LLM engineering mapping
Dropped streaming responses often look like an incomplete HTTP body on top of a connection close.

### Related labs
Week01, Week05, Week06, Week10.

## Bind / Listen / Accept / Connect

### Mental model
Servers bind and listen; clients connect; servers accept each established TCP client connection.

### Why it matters here
Week01 is the smallest place to see server and client roles without HTTP in the way.

### What to observe
Start two servers on the same host/port and observe the bind failure. Connect to a closed port and classify it as TCP.

### Common confusion
UDP uses `bind` and `recvfrom`, but not TCP-style `listen` and `accept`.

### AI/LLM engineering mapping
Port conflicts and wrong listener addresses are common in local inference stacks and Docker Compose projects.

### Related labs
Week01, Week09.

## Connection Refused

### Mental model
The target machine was reachable enough to reject the TCP connection because no process accepted that port.

### Why it matters here
Week01 and Week06 use this to separate TCP reachability from application errors.

### What to observe
Call a closed local port and run `python -m netlab fault classify connection-refused`. In capture, look for TCP reset.

### Common confusion
Connection refused is not a timeout. It is usually fast and explicit.

### AI/LLM engineering mapping
If a model gateway returns refused, debug listener, host, port, container mapping, or process startup before prompt logic.

### Related labs
Week01, Week06, Week09.

## Timeout

### Mental model
A timeout is a local decision to stop waiting after a deadline.

### Why it matters here
Week02, Week06, and Week10 use timeouts to distinguish no connection, slow read, slow upstream, and overload.

### What to observe
Compare connect timeout, read timeout, gateway timeout, and upstream slow responses. The packet trace may show a connection with no response bytes.

### Common confusion
"Timeout" is not one failure. Ask which operation timed out and which layer owned that wait.

### AI/LLM engineering mapping
Long model generations need explicit budgets: connect timeout, first-token timeout, total timeout, and retry policy.

### Related labs
Week02, Week06, Week10.

## Localhost / 127.0.0.1 / Loopback

### Mental model
Loopback routes traffic back to the same network namespace without leaving the machine.

### Why it matters here
Most labs use loopback for safe local experiments. Week09 shows why container loopback is separate.

### What to observe
Use `127.0.0.1` for local labs, then compare Docker host port mapping with service names.

### Common confusion
Inside a container, `127.0.0.1` is the container, not your laptop host and not another service container.

### AI/LLM engineering mapping
Many "container cannot reach model server" bugs are loopback scope bugs.

### Related labs
Week01, Week09, Week10.

## DNS Query

### Mental model
A DNS query asks a resolver to map a name to records such as A, AAAA, or CNAME before the application connects.

### Why it matters here
Week04 builds and sends DNS messages so name resolution is observable.

### What to observe
Capture `udp port 53` and inspect transaction id, question, answer, TTL, and response code.

### Common confusion
DNS success only gives an address. It does not prove TCP, TLS, or HTTP will succeed.

### AI/LLM engineering mapping
Private model endpoints and internal gateways often fail first at name resolution.

### Related labs
Week04, Week09, Week11.

## A / AAAA / CNAME

### Mental model
`A` maps a name to IPv4, `AAAA` maps to IPv6, and `CNAME` aliases one name to another.

### Why it matters here
Week04 supports these query types directly.

### What to observe
Query the same name with different types and compare answers. In Wireshark, inspect answer sections.

### Common confusion
A CNAME is not the final IP address; another lookup may be needed.

### AI/LLM engineering mapping
IPv6-only or IPv4-only environments can make an endpoint resolve but still be unreachable from a client.

### Related labs
Week04.

## TTL

### Mental model
TTL tells caches how long a DNS answer may be reused before asking again.

### Why it matters here
Week04 has a caching resolver experiment.

### What to observe
Run repeated queries and compare cache hit behavior before and after TTL expiry.

### Common confusion
Changing DNS records does not mean every client sees the change immediately.

### AI/LLM engineering mapping
Service migration, blue/green deployment, and private endpoint changes can look random while caches expire.

### Related labs
Week04, Week09, Week11.

## DNS Cache

### Mental model
A DNS cache saves recent answers to reduce latency and resolver load.

### Why it matters here
Week04 demonstrates why repeated queries can avoid network traffic.

### What to observe
Compare resolver logs and packet capture on first query versus cached query.

### Common confusion
A cache can preserve both useful answers and stale answers.

### AI/LLM engineering mapping
Agent workers may keep using old endpoint IPs after DNS or VPN policy changes.

### Related labs
Week04, Week11.

## DNS Timeout vs NXDOMAIN

### Mental model
Timeout means no useful answer arrived before the deadline; NXDOMAIN means the resolver answered that the name does not exist.

### Why it matters here
Week04 failure classification separates these symptoms.

### What to observe
Use `python -m netlab fault classify dns-timeout` and `dns-nxdomain`; compare whether packets show no response or an error response.

### Common confusion
Both may appear as "name resolution failed" in high-level tools, but fixes differ.

### AI/LLM engineering mapping
Internal model names behind VPN often fail as timeout or NXDOMAIN depending on DNS policy.

### Related labs
Week04, Week11.

## Docker Compose Service Name DNS

### Mental model
Compose gives containers on the same network DNS names based on service names.

### Why it matters here
Week09 uses service names instead of hard-coded container IPs.

### What to observe
Inside Compose, `gateway` or `upstream` can resolve; from the host, those names usually do not.

### Common confusion
Published host ports and container service DNS solve different problems.

### AI/LLM engineering mapping
A gateway container should call `upstream:8090`, while the host may call `127.0.0.1:18080`.

### Related labs
Week09, Week10.

## DNS Leak

### Mental model
A DNS leak means data traffic may use one path while DNS queries use another resolver/path.

### Why it matters here
Week11 uses it only as a diagnostic concept for VPN routing and DNS policy.

### What to observe
Compare DNS server settings before and after VPN connection with read-only commands.

### Common confusion
This tutorial does not teach bypass, anonymity, or commercial VPN setup. It only asks whether DNS and routes match the intended engineering path.

### AI/LLM engineering mapping
If internal model names fail after VPN connects, check whether DNS policy changed with routes.

### Related labs
Week04, Week11.

## Request Line

### Mental model
The HTTP request line says method, target path, and protocol version.

### Why it matters here
Week05 parses it directly.

### What to observe
Capture `GET /hello HTTP/1.1` and compare with parsed request fields.

### Common confusion
The request line is application protocol data inside TCP, not part of TCP itself.

### AI/LLM engineering mapping
Wrong paths such as `/stream` versus `/generate` are HTTP/application bugs after connectivity already worked.

### Related labs
Week05, Week10.

## Status Line

### Mental model
The HTTP status line reports protocol version, numeric status, and reason phrase.

### Why it matters here
Week05 and Week10 use status codes to separate application and capacity failures.

### What to observe
Compare `200 OK`, `429 Too Many Requests`, and `500 Injected Error`.

### Common confusion
HTTP error status does not mean TCP failed.

### AI/LLM engineering mapping
429 from a model gateway means capacity/backpressure, not DNS or TLS.

### Related labs
Week05, Week06, Week10.

## Headers

### Mental model
Headers are key-value metadata that control or describe the HTTP message.

### Why it matters here
Week05 parses headers; Week10 uses `X-Trace-Id` and `Transfer-Encoding`.

### What to observe
Inspect `Host`, `Content-Length`, `Connection`, `Transfer-Encoding`, and `X-Trace-Id`.

### Common confusion
Proxies may add, remove, or preserve headers; trace propagation depends on this.

### AI/LLM engineering mapping
Gateways commonly use headers for auth, routing, trace ids, model choice, and streaming behavior.

### Related labs
Week05, Week06, Week10.

## Body

### Mental model
The HTTP body is the payload after headers.

### Why it matters here
Week05 shows fixed-length bodies; Week10 streams body chunks over time.

### What to observe
Compare `Content-Length` responses with chunked responses.

### Common confusion
The body is not always available all at once.

### AI/LLM engineering mapping
Token streaming is an HTTP body delivered progressively.

### Related labs
Week05, Week10.

## Content-Length

### Mental model
`Content-Length` tells the receiver exactly how many body bytes to read.

### Why it matters here
Week05 uses it for simple complete responses.

### What to observe
Check that parsed body length matches the header.

### Common confusion
`Content-Length` and `Transfer-Encoding: chunked` are different ways to delimit a body.

### AI/LLM engineering mapping
Batch inference responses often use fixed content length; streaming responses usually do not know final length up front.

### Related labs
Week05.

## Connection: close

### Mental model
`Connection: close` tells the peer the connection will close after the response, making message end easier to detect.

### Why it matters here
The tutorial uses it to keep socket examples small.

### What to observe
After response bytes, the server closes the TCP connection.

### Common confusion
This is simpler than production keep-alive behavior.

### AI/LLM engineering mapping
Long-lived streaming and connection pools require more careful timeout and lifecycle handling.

### Related labs
Week05, Week10.

## Keep-Alive

### Mental model
Keep-alive reuses a TCP connection for multiple HTTP requests.

### Why it matters here
Week05 mentions it as a parser/server design pressure.

### What to observe
Compare one request per connection with a connection that remains open.

### Common confusion
Keeping TCP open does not keep an application request active forever; timeouts still apply.

### AI/LLM engineering mapping
SDKs and gateways use connection pooling to reduce handshake cost, but bad pools can hide stale connections.

### Related labs
Week05, Week06.

## Chunked Transfer Encoding

### Mental model
Chunked encoding sends an HTTP body as length-prefixed chunks when total size is not known at the start.

### Why it matters here
Week10 model-like server streams generated tokens using HTTP chunks.

### What to observe
Capture `/stream` and look for `Transfer-Encoding: chunked`, chunk sizes, chunk payloads, and the final zero-size chunk.

### Common confusion
Chunked HTTP is still HTTP over TCP; it is not WebSocket.

### AI/LLM engineering mapping
LLM token streaming often relies on chunked HTTP or Server-Sent Events. A proxy that buffers chunks destroys the user-perceived streaming.

### Related labs
Week05, Week10.

## HTTP Streaming

### Mental model
HTTP streaming means the response body arrives incrementally while the request is still active.

### Why it matters here
Week10 contrasts direct upstream stream with gateway stream.

### What to observe
Measure first byte/token latency separately from total latency. Watch whether chunks arrive one by one or only at the end.

### Common confusion
Fast total response and fast first token are different properties.

### AI/LLM engineering mapping
Interactive chat quality depends heavily on first-token latency and whether the gateway flushes upstream chunks promptly.

### Related labs
Week05, Week10.

## First Byte Latency vs Total Latency

### Mental model
First byte latency measures when any response starts; total latency measures when the whole response completes.

### Why it matters here
Week10 is the first lab where these can diverge naturally.

### What to observe
Stream tokens with a delay and compare direct upstream with gateway path.

### Common confusion
A system can have acceptable total latency but poor first-token latency if a proxy buffers.

### AI/LLM engineering mapping
Users notice delayed first token before they notice final completion time.

### Related labs
Week10.

## Forward Proxy vs Reverse Proxy

### Mental model
A forward proxy represents the client; a reverse proxy or gateway represents the service side.

### Why it matters here
Week06 and Week10 use a reverse proxy shape.

### What to observe
The client connects to the proxy, and the proxy opens a separate upstream TCP connection.

### Common confusion
Both are "proxies", but ownership, routing, headers, and failure responsibility differ.

### AI/LLM engineering mapping
Model gateways, API gateways, and ingress proxies are usually reverse proxies.

### Related labs
Week06, Week10.

## Gateway

### Mental model
A gateway is a controlled hop that accepts downstream requests and makes upstream requests on their behalf.

### Why it matters here
Week10 uses gateway behavior to connect trace ids, streaming, capacity, retries, and metrics.

### What to observe
Compare client -> gateway logs with gateway -> upstream logs and packet flows.

### Common confusion
The gateway may fail even when upstream works directly.

### AI/LLM engineering mapping
LLM gateways centralize routing, auth, observability, timeout, retry, and backpressure policy.

### Related labs
Week06, Week10.

## Upstream

### Mental model
Upstream is the dependency a proxy or gateway calls to satisfy a downstream request.

### Why it matters here
Week06 fault server and Week10 model-like server are upstreams.

### What to observe
When upstream is slow or returns 500/429, classify whether the gateway changed the symptom.

### Common confusion
An upstream timeout might be reported to the client as a gateway timeout.

### AI/LLM engineering mapping
The upstream might be a model worker, vector database, embedding service, or remote tool.

### Related labs
Week06, Week10.

## Proxy Buffering

### Mental model
Proxy buffering means the proxy reads a response into memory before forwarding some or all of it downstream.

### Why it matters here
Week10 verifies that the teaching proxy forwards streaming chunks instead of waiting for the whole body.

### What to observe
Compare first byte timing through gateway. If all tokens arrive at once, buffering is likely happening.

### Common confusion
Buffering can be useful for small responses but harmful for interactive streaming.

### AI/LLM engineering mapping
Buffered gateways make LLM streaming look broken even when the model server streams correctly.

### Related labs
Week06, Week10.

## Gateway Timeout

### Mental model
A gateway timeout means the gateway gave up waiting for upstream or could not complete upstream work in budget.

### Why it matters here
Week06 maps upstream slow behavior to gateway symptoms.

### What to observe
Run a slow fault server and compare client timeout, proxy log, and upstream log.

### Common confusion
Gateway timeout is not the same as client connect timeout.

### AI/LLM engineering mapping
Model serving gateways need separate budgets for queue wait, first token, and total generation.

### Related labs
Week06, Week10.

## Upstream Timeout

### Mental model
An upstream timeout is the proxy or gateway timing out while calling its dependency.

### Why it matters here
Week06 asks where timeout is enforced.

### What to observe
Point the proxy at a slow upstream and compare whether downstream receives a response, a close, or a local timeout.

### Common confusion
The client may only see "gateway failed" while the root wait happened upstream.

### AI/LLM engineering mapping
Retrying a slow model worker can amplify load if the original request keeps running.

### Related labs
Week06, Week10.

## Retry

### Mental model
A retry repeats an operation after a failure, hoping the failure was temporary.

### Why it matters here
Week06 shows retry value and risk with a tiny policy.

### What to observe
Run the retry experiment and count attempts. Classify retry-storm separately from the original failure.

### Common confusion
Retries are not free. They add load and can convert a small outage into overload.

### AI/LLM engineering mapping
Retrying expensive generation can burn GPU capacity and increase queue latency for everyone.

### Related labs
Week06, Week10.

## Retry Storm

### Mental model
A retry storm happens when many clients retry at once and multiply pressure on an already struggling dependency.

### Why it matters here
Week06 and Week10 classify it as capacity behavior.

### What to observe
Use load tests and watch p95 latency, 429s, and failure count rise.

### Common confusion
More retries can reduce individual transient failures but worsen systemic overload.

### AI/LLM engineering mapping
Agents that retry tool/model calls aggressively can saturate gateways and worker queues.

### Related labs
Week06, Week10.

## TLS

### Mental model
TLS encrypts and authenticates application bytes after TCP connects.

### Why it matters here
Week07 shows where HTTPS differs from plain HTTP.

### What to observe
Capture ClientHello, ServerHello, certificate, and encrypted application data.

### Common confusion
TLS does not hide IP addresses, TCP ports, timing, or usually the server name in classic SNI.

### AI/LLM engineering mapping
Private gateways often fail at certificate trust, SNI, or proxy TLS boundaries.

### Related labs
Week07, Week10, Week11.

## Certificate Validation

### Mental model
Certificate validation checks whether the server identity chains to a trusted authority and matches the hostname.

### Why it matters here
Week07 distinguishes certificate failure from TCP failure.

### What to observe
Call a known HTTPS endpoint and inspect whether the TLS handshake completes.

### Common confusion
Disabling verification hides the symptom instead of teaching the layer.

### AI/LLM engineering mapping
Internal model endpoints often use private CAs; clients must trust the right CA instead of ignoring validation.

### Related labs
Week07.

## SNI

### Mental model
SNI lets a client tell a TLS server which hostname it wants during the handshake.

### Why it matters here
Week07 includes SNI observation.

### What to observe
In ClientHello, look for the server name extension.

### Common confusion
SNI is not the HTTP `Host` header, though both carry hostname intent at different layers.

### AI/LLM engineering mapping
Gateways hosting many HTTPS names need correct SNI for certificate and routing.

### Related labs
Week07, Week10.

## ALPN

### Mental model
ALPN negotiates the application protocol, such as HTTP/1.1 or HTTP/2, inside TLS.

### Why it matters here
Week07 observes protocol negotiation without turning the project into an HTTP/2 tutorial.

### What to observe
Inspect TLS handshake details when available.

### Common confusion
TLS and HTTP version are related through ALPN but still separate layers.

### AI/LLM engineering mapping
Some APIs behave differently behind gateways depending on HTTP/1.1 versus HTTP/2 support.

### Related labs
Week07.

## Encrypted Application Data

### Mental model
After TLS handshake, packet capture sees encrypted records instead of raw HTTP headers and body.

### Why it matters here
Week07 contrasts visible TCP/TLS metadata with hidden application payload.

### What to observe
Use `tls` display filter and notice that HTTP path/body are not readable without decryption keys.

### Common confusion
TLS hides content but not all metadata.

### AI/LLM engineering mapping
You may still debug DNS, TCP, certificate, SNI, timing, and byte counts for HTTPS model APIs.

### Related labs
Week07.

## What TLS Hides and What It Does Not Hide

### Mental model
TLS hides application content, but network metadata still exists below it.

### Why it matters here
Week07 teaches observability limits with HTTPS.

### What to observe
Packet capture can show IPs, ports, handshake, record sizes, and timing, but not plain HTTP body.

### Common confusion
"Encrypted" does not mean "undebuggable"; it means the visible signals move down to metadata.

### AI/LLM engineering mapping
For HTTPS LLM APIs, use logs and trace ids for application data, packets for transport evidence.

### Related labs
Week07, Week10.

## Concurrency

### Mental model
Concurrency is how many operations are in progress at the same time.

### Why it matters here
Week10 model-like server uses a max concurrency gate.

### What to observe
Run load with concurrency higher than capacity and observe 429s.

### Common confusion
Concurrency is not the same as requests per second, though they influence each other.

### AI/LLM engineering mapping
GPU workers and model runtimes often have small true concurrency even when HTTP accepts many clients.

### Related labs
Week10.

## Queue

### Mental model
A queue holds work waiting for capacity.

### Why it matters here
The tutorial uses a reject-fast gate instead of a large queue to make backpressure visible.

### What to observe
Compare immediate 429 with slow queueing behavior in real systems.

### Common confusion
A queue can smooth bursts but also hide overload until latency becomes unacceptable.

### AI/LLM engineering mapping
Model serving often has request queues in front of scarce GPU workers.

### Related labs
Week10.

## Backpressure

### Mental model
Backpressure tells callers to slow down or stop sending work when capacity is exhausted.

### Why it matters here
Week10 returns HTTP 429 when max concurrency is exceeded.

### What to observe
Run load tests and count success, timeout, and 429 responses.

### Common confusion
Backpressure is not a bug by itself; it is often the healthy alternative to unbounded queue growth.

### AI/LLM engineering mapping
Gateways use 429, rate limits, and queues to protect model workers.

### Related labs
Week06, Week10.

## HTTP 429

### Mental model
HTTP 429 means the server understood the request but rejected it due to rate or capacity policy.

### Why it matters here
Week10 uses 429 to make capacity visible.

### What to observe
Trigger concurrent load above `--max-concurrency` and inspect status codes.

### Common confusion
429 is not a TCP failure, DNS failure, or TLS failure.

### AI/LLM engineering mapping
429 often maps to GPU worker saturation, queue limits, token budget limits, or tenant rate limits.

### Related labs
Week10.

## p50 / p95 Latency

### Mental model
p50 is the median request latency; p95 shows tail latency for the slower 5 percent.

### Why it matters here
The load helper reports these values to show pressure beyond average latency.

### What to observe
Increase concurrency and compare p50 and p95.

### Common confusion
A healthy average can hide bad tail latency.

### AI/LLM engineering mapping
Agent workflows feel unreliable when p95 or p99 tool/model calls grow, even if median is fine.

### Related labs
Week10.

## Model Serving Capacity

### Mental model
Model serving capacity is the practical limit of concurrent work a model runtime can handle before latency or rejection grows.

### Why it matters here
Week10 simulates model generation delay and max concurrency.

### What to observe
Tune `--max-concurrency`, `--tokens`, and `--token-delay`; observe 429 and latency.

### Common confusion
The HTTP server can accept sockets faster than the model can generate tokens.

### AI/LLM engineering mapping
GPU memory, batching, context length, and worker count decide real serving capacity.

### Related labs
Week10.

## GPU Worker / Request Queue Mental Model

### Mental model
A gateway receives many HTTP requests, but a small number of workers do the expensive generation; overflow waits or gets rejected.

### Why it matters here
Week10 uses a small backpressure gate to model this shape without GPU dependencies.

### What to observe
When more requests arrive than workers, some return 429 while accepted ones stream tokens.

### Common confusion
Network reachability can be perfect while capacity is exhausted.

### AI/LLM engineering mapping
This is the common path for local model serving, internal inference platforms, and agent tool backends.

### Related labs
Week10.

## Container Network Namespace

### Mental model
A network namespace gives a container its own interfaces, routes, and loopback.

### Why it matters here
Week09 explains why container `localhost` differs from host `localhost`.

### What to observe
Compare host commands with commands run inside a container.

### Common confusion
Two processes on the same physical machine may not share the same network view.

### AI/LLM engineering mapping
Local multi-container AI stacks often fail because a service points to the wrong namespace.

### Related labs
Week09.

## Bridge Network

### Mental model
A bridge network is a virtual L2 network connecting containers and NAT/published ports to the host.

### Why it matters here
Week09 uses Docker Compose bridge networking.

### What to observe
Service-to-service traffic uses container network addresses; host-to-container traffic uses published ports.

### Common confusion
Bridge networking is not the same as host networking.

### AI/LLM engineering mapping
Gateway and model containers communicate across the bridge while your browser uses host port mapping.

### Related labs
Week09, Week10.

## Service Name

### Mental model
A service name is a stable DNS name Docker Compose assigns to a container service.

### Why it matters here
Week09 uses names rather than changing IP addresses.

### What to observe
Inside Compose, resolve and call the service name. From the host, use the published port instead.

### Common confusion
Service names are scoped to the Compose network.

### AI/LLM engineering mapping
Use `model:8090` inside Compose; use `localhost:18080` from the host when port is published.

### Related labs
Week09, Week10.

## Port Mapping

### Mental model
Port mapping forwards a host port to a container port.

### Why it matters here
Week09 exposes a container service to the host.

### What to observe
Call the host port and compare it with the container's internal listening port.

### Common confusion
Changing the host port does not change the port the application listens on inside the container.

### AI/LLM engineering mapping
Misreading `18080:8080` is a common reason local model gateways appear unreachable.

### Related labs
Week09.

## Host Port vs Container Port

### Mental model
The host port is what the host machine accepts; the container port is what the application accepts inside the container namespace.

### Why it matters here
Week09 asks you to separate the two.

### What to observe
Compare Docker Compose config with client commands from host and container.

### Common confusion
`127.0.0.1:8080` on the host is not automatically the same as `127.0.0.1:8080` in a container.

### AI/LLM engineering mapping
This affects Ollama-like local services, vector stores, gateways, and UI containers.

### Related labs
Week09.

## Why Localhost Inside a Container Is Not the Host

### Mental model
Loopback always points to the current namespace, and a container has its own namespace.

### Why it matters here
Week09 turns this into a practical debugging rule.

### What to observe
Inside a container, `localhost` reaches services in that same container only.

### Common confusion
Sharing a machine does not mean sharing loopback.

### AI/LLM engineering mapping
A containerized agent cannot call a host model server via plain `localhost` unless the network is configured for that path.

### Related labs
Week09, Week10.

## VPN Tunnel

### Mental model
A VPN tunnel carries selected traffic through an encrypted path to a VPN gateway.

### Why it matters here
Week11 uses VPN as a routing and DNS mental model, not as a setup guide.

### What to observe
Compare route table, DNS servers, and traceroute before and after connecting to a VPN you are already authorized to use.

### Common confusion
VPN is not a magic switch; it changes how DNS and routes choose paths.

### AI/LLM engineering mapping
Remote lab servers and internal model endpoints may only resolve or route correctly through the intended VPN policy.

### Related labs
Week04, Week07, Week09, Week11.

## Virtual Interface

### Mental model
A virtual interface is an OS network interface created by software instead of physical hardware.

### Why it matters here
Week11 checks whether a VPN adds or changes interfaces and routes.

### What to observe
Read interface and route output; do not modify settings.

### Common confusion
Seeing a virtual interface does not mean all traffic uses it.

### AI/LLM engineering mapping
Internal service traffic may follow the virtual interface while public traffic stays direct in split tunnel.

### Related labs
Week11.

## TUN vs TAP

### Mental model
TUN carries IP packets; TAP carries Ethernet frames. For this tutorial, the distinction is conceptual only.

### Why it matters here
Week11 mentions it so interface names make more sense in VPN tools.

### What to observe
No setup is required. Just note interface names and routes.

### Common confusion
You do not need to build a TUN/TAP device to learn the routing and DNS signals.

### AI/LLM engineering mapping
Most application debugging starts from route/DNS outcomes, not driver details.

### Related labs
Week11.

## Route Table

### Mental model
The route table decides which next hop/interface should carry packets for a destination IP.

### Why it matters here
Week11 makes routing visible with read-only commands.

### What to observe
Compare default route and more-specific internal routes before and after VPN.

### Common confusion
DNS gives an IP; routing decides where packets to that IP go.

### AI/LLM engineering mapping
An internal model IP may resolve correctly but still time out if no route points to it.

### Related labs
Week11.

## Default Route

### Mental model
The default route is the fallback path when no more-specific route matches.

### Why it matters here
Full tunnel VPNs often change the default route; split tunnel VPNs often add specific routes.

### What to observe
Use read-only route commands and compare the default route before/after VPN.

### Common confusion
A changed default route affects broad traffic behavior, not just one app.

### AI/LLM engineering mapping
Public API latency or reachability may change if VPN moves public traffic through a corporate gateway.

### Related labs
Week11.

## Full Tunnel

### Mental model
Full tunnel sends most or all traffic through the VPN path.

### Why it matters here
Week11 asks whether public DNS, routes, and traceroute changed after VPN.

### What to observe
Default route and DNS servers often change.

### Common confusion
Full tunnel can affect public APIs, package installs, and cloud dashboards, not only internal services.

### AI/LLM engineering mapping
External model APIs may get slower or fail under corporate egress policy.

### Related labs
Week11.

## Split Tunnel

### Mental model
Split tunnel sends only selected routes through VPN while other traffic stays direct.

### Why it matters here
Week11 treats it as a route table pattern.

### What to observe
Look for specific internal routes and unchanged default route.

### Common confusion
Split tunnel can still change DNS policy even if default route does not change.

### AI/LLM engineering mapping
Internal model endpoints might work while public APIs keep using normal internet routing.

### Related labs
Week11.

## DNS Policy

### Mental model
DNS policy decides which resolver answers which names, sometimes depending on VPN state or domain suffix.

### Why it matters here
Week11 compares DNS server and domain resolution before and after VPN.

### What to observe
Use `Resolve-DnsName`, `scutil --dns`, `resolvectl dns`, or `dig` where available.

### Common confusion
Correct routes do not fix names that resolve through the wrong DNS server.

### AI/LLM engineering mapping
Company-only model names need the correct resolver or search domain.

### Related labs
Week04, Week11.

## VPN Outer Traffic vs Inner Traffic

### Mental model
Inner traffic is the original packet; outer traffic is the encrypted tunnel packet seen on the physical network.

### Why it matters here
Week11 explains why packet capture on a physical NIC may not show plain internal HTTP/DNS.

### What to observe
On a physical interface, expect encrypted tunnel traffic. On virtual interfaces, tools may show inner traffic depending on OS and capture permissions.

### Common confusion
"I cannot see HTTP in Wireshark" may be correct when traffic is inside an encrypted tunnel.

### AI/LLM engineering mapping
Use application logs and trace ids for inner HTTP behavior; use packets for route/timing evidence.

### Related labs
Week07, Week11.

## MTU / MSS

### Mental model
MTU is maximum packet size on a link; MSS is maximum TCP payload size after headers.

### Why it matters here
Week11 mentions it only as a conceptual explanation for "ping works but HTTP stalls" cases.

### What to observe
No risky tuning is required. Note symptoms and route/VPN changes.

### Common confusion
MTU/MSS is a later hypothesis after DNS, TCP connect, TLS, and HTTP basics are checked.

### AI/LLM engineering mapping
Large uploads, long responses, or TLS records may expose path MTU issues across VPN.

### Related labs
Week11.

## Logs

### Mental model
Logs are timestamped application events that explain what code thought it was doing.

### Why it matters here
Every server in the tutorial prints small structured events.

### What to observe
Correlate logs with client status and packet capture.

### Common confusion
Logs can lie by omission; packets and metrics help validate them.

### AI/LLM engineering mapping
Gateway and model worker logs are the fastest way to separate application failure from network failure.

### Related labs
All labs.

## Trace ID

### Mental model
A trace id is a shared identifier carried across components so one request can be followed end to end.

### Why it matters here
Week10 propagates or generates `X-Trace-Id`.

### What to observe
Compare client response header, gateway log, and upstream log.

### Common confusion
A trace id is not security; it is correlation metadata.

### AI/LLM engineering mapping
Agent calls often cross client, gateway, retrieval service, model worker, and tool server. Trace ids connect the path.

### Related labs
Week10.

## Metrics

### Mental model
Metrics are aggregated counters and timings used to see system behavior across requests.

### Why it matters here
Week10 exposes a small metrics endpoint and load summary.

### What to observe
Compare accepted/rejected counts and p50/p95 latency under load.

### Common confusion
Metrics show trends, not individual root cause by themselves.

### AI/LLM engineering mapping
Request rate, 429 count, queue depth, token rate, and latency percentiles are core model-serving signals.

### Related labs
Week10.

## Packet Capture

### Mental model
Packet capture records what crossed a network interface.

### Why it matters here
The tutorial uses Wireshark/TShark to verify that code behavior matches network behavior.

### What to observe
Capture one lab at a time with narrow filters, then map packets back to code.

### Common confusion
Packets do not automatically reveal encrypted application content or container-internal traffic from the host.

### AI/LLM engineering mapping
Packets are useful when logs disagree about DNS, TCP, TLS, timeout, or proxy behavior.

### Related labs
All labs.

## Capture Filter vs Display Filter

### Mental model
A capture filter decides what to record; a display filter decides what to show from already recorded traffic.

### Why it matters here
The capture docs and lab tasks use both.

### What to observe
Use narrow capture filters like `tcp port 8080` and display filters like `http` or `dns`.

### Common confusion
If a capture filter excluded traffic, a display filter cannot bring it back.

### AI/LLM engineering mapping
When debugging gateways, capture both downstream and upstream ports if you need the full path.

### Related labs
Week05, Week06, Week10.

## Connecting Code Behavior, Logs, HTTP Status, and Packets

### Mental model
Good debugging connects what the code did, what logs say, what HTTP returned, and what packets prove.

### Why it matters here
This is the main learning loop for every lab.

### What to observe
For each failure, write the command, expected result, actual status/error, logs, packet evidence, and layer classification.

### Common confusion
No single signal is enough for every failure.

### AI/LLM engineering mapping
Real AI systems span SDKs, gateways, containers, model runtimes, VPN, DNS, and cloud services. Layered evidence prevents random fixes.

### Related labs
All labs, especially Week06, Week10, Week11.
