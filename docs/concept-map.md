# Concept Map

## Full Tutorial Map
```text
Week00 map/tools
  -> Week01 IP/subnet/route
  -> Week02 ARP/ICMP/NAT/firewall
  -> Week03 sockets TCP/UDP
  -> Week04 framing and packets
  -> Week05 DNS
  -> Week06 HTTP
  -> Week07 TLS/HTTPS
  -> Week08 proxy/timeout/retry
  -> Week09 RPC/WebSocket/streaming
  -> Week10 Docker networking
  -> Week11 VPN remote access
  -> Week12 design + observable service path
```

## Local Network Path
```text
laptop app
  -> socket
  -> local IP/subnet decision
  -> ARP for local next hop
  -> gateway when remote
  -> NAT/firewall policy
  -> destination
```

## Application Request Path
```text
intent
  -> DNS lookup
  -> route lookup
  -> TCP connect
  -> TLS handshake when HTTPS
  -> HTTP/RPC request
  -> proxy/gateway
  -> upstream service
  -> logs/metrics/traces/packets
```

## Docker Path
```text
host client
  -> published host port
  -> container port
  -> Compose bridge network
  -> service-name DNS
  -> upstream container
```

## VPN Path
```text
client app
  -> DNS policy
  -> route table
  -> virtual VPN interface
  -> encrypted outer tunnel
  -> remote network
  -> internal service
```

## Capstone Service Path
```text
client
  -> gateway/reverse proxy
  -> model-like upstream
  -> X-Trace-Id
  -> streaming chunks
  -> metrics/backpressure
  -> packet/timing evidence
```
