# Systematic Knowledge Path

The project is organized around one request path, not around disconnected scenarios.

## 1. Application Intent

An application decides to call another component. This intent becomes a hostname, port, protocol, timeout, retry policy, payload, and expected response.

## 2. Name Resolution

DNS maps names to addresses. Important failure modes: timeout, NXDOMAIN, stale cache, wrong internal record.

## 3. Connection

TCP creates a byte stream; UDP sends datagrams. Important failure modes: refused connection, reset, timeout, half-open connection.

## 4. Secure Transport

TLS wraps the connection. Important failure modes: certificate validation, SNI mismatch, protocol or cipher mismatch.

## 5. Application Protocol

HTTP, RPC, and WebSocket define message structure above transport. Important failure modes: malformed headers, wrong status, broken framing, long-lived connection drops.

## 6. Proxy/Gateway

A gateway creates a second network path to upstream. Important failure modes: upstream slow, gateway timeout, header loss, retry amplification.

## 7. Concurrency and Backpressure

Many requests compete for the same capacity. Important failure modes: queue buildup, 429, timeout, retry storm, p95 latency growth.

## 8. Observability

Logs, metrics, and trace ids connect application behavior to network behavior.

## 9. Packet-Level Verification

Wireshark validates whether the mental model matches what crossed the network boundary.
