# Glossary

| Term | 中文解释 | Mental Model | Related Lab |
| ---- | ---- | ---- | ---- |
| Host | 主机名或地址 | The machine/interface you intend to reach. | Week01, Week09 |
| Port | 端口 | The application endpoint on a host. | Week01 |
| Socket | 套接字 | The process API for network I/O. | Week01, Week02 |
| TCP | 传输控制协议 | Reliable ordered byte stream. | Week01, Week02 |
| UDP | 用户数据报协议 | Independent datagrams without connection setup. | Week01, Week04 |
| Handshake | 握手 | TCP setup before application bytes. | Week01 |
| Timeout | 超时 | Local deadline for waiting. | Week02, Week06 |
| DNS | 域名系统 | Name to record/address lookup. | Week04 |
| A / AAAA | IPv4 / IPv6 记录 | Address records for a name. | Week04 |
| CNAME | 别名记录 | One name points to another name. | Week04 |
| TTL | 生存时间 | How long DNS cache may reuse an answer. | Week04 |
| NXDOMAIN | 域名不存在 | Resolver says the name does not exist. | Week04 |
| HTTP Request Line | HTTP 请求行 | Method, target, version. | Week05 |
| HTTP Status | HTTP 状态 | Application result code. | Week05, Week10 |
| Header | HTTP 头 | Metadata key-value fields. | Week05, Week10 |
| Content-Length | 内容长度 | Fixed body byte count. | Week05 |
| Chunked | 分块传输 | Body sent as size-prefixed chunks. | Week05, Week10 |
| Streaming | 流式响应 | Body arrives progressively. | Week10 |
| Proxy | 代理 | A hop that forwards traffic. | Week06 |
| Gateway | 网关 | Controlled reverse proxy/service entry. | Week06, Week10 |
| Upstream | 上游 | Dependency called by a gateway. | Week06, Week10 |
| Retry | 重试 | Repeat after likely transient failure. | Week06 |
| Retry Storm | 重试风暴 | Retries multiply overload. | Week06, Week10 |
| TLS | 安全传输层 | Encrypted/authenticated transport above TCP. | Week07 |
| SNI | TLS 服务名指示 | Hostname sent during TLS handshake. | Week07 |
| ALPN | 应用层协议协商 | TLS negotiation of HTTP protocol. | Week07 |
| Backpressure | 背压 | Refuse/slow callers when capacity is full. | Week10 |
| HTTP 429 | 请求过多 | Capacity or rate-limit rejection. | Week10 |
| p50 / p95 | 延迟分位数 | Median and tail latency signals. | Week10 |
| Container Namespace | 容器网络命名空间 | A container's own network view. | Week09 |
| Bridge Network | 桥接网络 | Virtual network connecting containers. | Week09 |
| Service Name | 服务名 | Compose DNS name for a service. | Week09 |
| Port Mapping | 端口映射 | Host port forwarded to container port. | Week09 |
| VPN Tunnel | VPN 隧道 | Selected traffic carried through encrypted path. | Week11 |
| Route Table | 路由表 | Destination-to-interface/next-hop rules. | Week11 |
| Full Tunnel | 全隧道 | Most traffic goes through VPN. | Week11 |
| Split Tunnel | 分流隧道 | Only selected routes go through VPN. | Week11 |
| DNS Leak | DNS 泄漏 | DNS uses an unexpected resolver/path. | Week11 |
| Trace ID | 追踪 ID | Correlation id across components. | Week10 |
| Metrics | 指标 | Aggregated counters/timings. | Week10 |
| Packet Capture | 抓包 | Interface-level evidence of traffic. | All |
