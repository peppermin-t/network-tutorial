# Python Network Lab Tutorial Project

`python-network-lab` 是一个代码驱动的计算机网络学习项目。它用 Python 从 socket 开始，逐步搭建 TCP/UDP、协议解析、DNS、HTTP、代理、TLS、RPC、WebSocket、Docker 网络、并发/背压、故障注入和可观测通信系统。

目标不是只读概念，而是每周都有可运行代码、实验命令、测试和复盘问题。

统一主线：

```text
Application Intent
-> Name Resolution
-> Connection
-> Secure Transport
-> Application Protocol
-> Proxy/Gateway
-> Concurrency & Backpressure
-> Failure Handling
-> Observability
-> Packet-Level Verification
```

云服务、分布式系统、本地模型服务部署都是验证场景；目录主线仍然是这条分层通信链路。

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
python -m unittest discover -s tests -p "test_*.py"
python -m netlab --help
```

不安装包也可以直接运行：

```powershell
$env:PYTHONPATH="src"
python -m netlab --help
```

## CLI Examples

启动 TCP echo server：

```powershell
python -m netlab server tcp-echo --host 127.0.0.1 --port 9001
```

另开一个终端调用：

```powershell
python -m netlab client tcp-echo --host 127.0.0.1 --port 9001 --message "hello tcp"
```

DNS 查询：

```powershell
python -m netlab dns query example.com --type A --server 8.8.8.8
```

HTTP server/client：

```powershell
python -m netlab server http --host 127.0.0.1 --port 8080
python -m netlab client http --host 127.0.0.1 --port 8080 --path /
```

WebSocket echo：

```powershell
python -m netlab server websocket --host 127.0.0.1 --port 8765
python -m netlab client websocket --host 127.0.0.1 --port 8765 --message "ping"
```

故障归层：

```powershell
python -m netlab fault classify read-timeout
python -m netlab fault classify retry-storm
```

并发压测：

```powershell
python -m netlab client load-http --host 127.0.0.1 --port 8080 --requests 20 --concurrency 5
```

Model-like upstream：

```powershell
python -m netlab server model --host 127.0.0.1 --port 8090 --max-concurrency 2 --tokens 8 --token-delay 0.1
python -m netlab client http --host 127.0.0.1 --port 8090 --path /stream?prompt=local+model
```

Wireshark/TShark optional helpers:

```powershell
python -m netlab capture status
python -m netlab capture command --interface "Adapter for loopback traffic capture" --output captures/week05-http.pcapng --filter "tcp port 8080" --packets 20
```

See [docs/wireshark.md](docs/wireshark.md) for the capture workflow and [docs/capture-first-day.md](docs/capture-first-day.md) for a first-day route.

## 10-Week Path

1. `labs/week01-sockets`: TCP/UDP echo、端口、连接生命周期。
2. `labs/week02-tcp-udp`: 长度前缀、分包/粘包、心跳、超时。
3. `labs/week03-packet-thinking`: 用字节数组模拟协议头和 payload。
4. `labs/week04-dns`: DNS message、查询、TTL cache。
5. `labs/week05-http`: HTTP/1.1 parser、client、server、keep-alive。
6. `labs/week06-proxy-timeout-retry`: forward/reverse proxy、timeout、retry。
7. `labs/week07-tls`: Python `ssl`、本地证书、SNI/ALPN 观察。
8. `labs/week08-rpc-websocket`: JSON-RPC over HTTP、WebSocket。
9. `labs/week09-container-networking`: Docker Compose、服务名解析、bridge network。
10. `labs/week10-capstone`: client -> gateway -> model-like upstream 的可观测通信系统。

每个 lab 都包含 `README.md`、`experiment.py`、`notes.md`。先跑实验，再读源码，最后写观察结论。

## Tooling Notes

- 主线只依赖 Python 标准库。
- 单元测试使用 `unittest`，也兼容 `pytest` 发现。
- Docker 用于第 9 周和第 10 周增强实验。
- Wireshark/tshark 是强烈推荐的增强层，不是必需条件。没有它也能完成全部代码实验；装好后可以把每周实验和真实报文对应起来。
- 并发、背压、故障注入和 model-like upstream 用来验证同一套底层网络知识，不是额外拼接的独立主题。
