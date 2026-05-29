# Week00 Notes - Orientation, Layering, and Tools

## 0. 本周定位

Week00 不是在学习某一个具体协议，而是在建立整个 network tutorial 的总心智模型。

这一周最重要的问题是：

> 当一次服务访问失败时，不要笼统地说“网络不通”，而要判断它失败在通信路径上的哪一层。

本教程后面所有内容，都围绕这条主线展开：

```text
application intent
-> DNS
-> route
-> socket
-> TCP/UDP
-> TLS
-> HTTP
-> proxy/gateway
-> upstream
```

这条链路不是单个 packet 的发送过程，而是一次应用通信的排障依赖链。

---

## 1. 当前实验环境

Week00 运行过的命令：

```powershell
python -m pip install -e .
python -m netlab doctor
python -m netlab path tutorial
python -m netlab capture status
```

本机环境检查结果：

```text
OS: Windows 11
Python: 3.12.9
TShark: available
TShark/Wireshark version: 4.6.6
Docker: available
```

---

## 2. Week00 的核心思想

“网络问题”不是一类问题，而是一条通信路径上不同层次的失败。

一次服务访问失败时，应该按层次拆开看：

```text
1. 应用想访问谁？（application intent）
2. 域名是否解析成功？（DNS，判断请求有没有解析出目标 IP）
3. 系统是否选择了正确路径？（route，判断系统有没有选出正确路径）
4. 端口是否能连上？（socket）
5. TCP/UDP 是否正常？（TCP/UDP，判断 TCP/UDP 是否到达）
6. TLS 是否握手成功？（TLS，判断 TLS 是否握手成功）
7. HTTP 是否有协议级响应？（HTTP，判断 HTTP 是否有协议级响应）
8. proxy/gateway 是否正常转发？（proxy/gateway）
9. upstream/application 是否收到并处理？（upstream，看 proxy/gateway/upstream/application 的业务行为）
```

---

## 3. Layer Map 的逐层理解

### 3.1 application intent

application intent 是应用最开始的访问意图。

例如：

```text
我要访问 https://example.com/api/chat
```

里面实际包含：

```text
scheme = https
host = example.com
port = 443
path = /api/chat
method = GET/POST
headers/body/timeout 等配置
```

这一步还没有真正开始网络传输，只是应用准备发起通信。

---

### 3.2 DNS

DNS 负责把域名解析成 IP。

例如：

```text
example.com -> 93.184.216.34
```

关键点：

```text
DNS 成功，只说明拿到了目标 IP。
DNS 成功，不说明 TCP/TLS/HTTP 一定成功。
```

常见情况：

```text
DNS 失败：
不知道应该连接哪个 IP。

DNS 成功但 TCP 失败：
知道 IP，但连接不上目标端口。

DNS 成功、TCP 成功但 TLS 失败：
端口能连，但 HTTPS 握手失败。

DNS 成功、TCP 成功、TLS 成功但 HTTP 500：
底层网络大概率已经通了，问题在 HTTP/application 层。
```

---

### 3.3 route

route 决定去某个目标 IP 时：

```text
从哪块网卡出去？
下一跳是谁？
走默认网关、VPN、专线，还是容器网络？
```

代码通常只指定目标地址，不直接控制具体路径。

例如代码里写：

```python
requests.get("https://example.com")
```

但代码没有直接说明：

```text
从 Wi-Fi 网卡出去
走 192.168.1.1 网关
访问 10.0.0.0/8 时走 VPN
```

这些由 OS 的路由表和当前网络环境决定。

重要规则：

```text
最长前缀匹配优先。
```

例如：

```text
0.0.0.0/0        -> 默认网关
10.0.0.0/8       -> VPN
10.20.30.0/24    -> 某条更具体的路由
```

访问 `10.20.30.40` 时，系统优先选择 `/24`，因为它比 `/8` 和 `/0` 更具体。

---

### 3.4 socket

socket 是应用进入网络世界的 OS API。

例如 Python 中：

```python
sock.connect(("93.184.216.34", 443))
```

socket 不是 TCP 本身，而是应用使用 TCP/UDP 等网络能力的接口。

常见 socket 操作：

```text
bind
listen
accept
connect
send
recv
```

理解重点：

```text
socket 是应用代码可见的；
TCP/UDP 的很多细节由 OS 协议栈处理。
```

---

### 3.5 TCP/UDP

TCP 是可靠、有序的字节流。

多数 HTTP、HTTPS、API、RPC、代理、模型服务都跑在 TCP 上。

关键理解：

```text
TCP 连接成功，只说明传输层通了。
TCP 成功，不代表 TLS 成功。
TCP 成功，也不代表 HTTP 成功。
```

常见现象：

```text
connection refused:
目标主机有回应，但目标端口没有服务监听，或服务主动拒绝。

timeout:
没有收到有效回应。可能是路径不通、防火墙静默丢包、目标不可达、网络设备丢弃等。

connected:
TCP 连接建立成功，但后面的 TLS/HTTP/application 仍可能失败。
```

UDP 是无连接 datagram，不做 TCP 那种连接建立、可靠传输和顺序保证。DNS 常见使用 UDP。

---

### 3.6 TLS

HTTPS = HTTP over TLS。

TLS 位于 TCP 之后、HTTP 之前。

大致顺序：

```text
TCP handshake 成功
-> TLS handshake
-> HTTP request/response
```

TLS 常见失败原因：

```text
证书不被信任
证书域名不匹配
证书过期
SNI 不对
TLS 版本不兼容
加密套件不兼容
```

重要区分：

```text
SNI 在 TLS 层。
Host header 在 HTTP 层。
```

如果 TLS 握手失败，HTTP 请求通常还没有真正发出去。

所以：

```text
TLS certificate error != HTTP 500
TLS handshake failure != application server 处理失败
```

---

### 3.7 HTTP

HTTP 是应用层协议。

如果已经看到：

```text
HTTP 200
HTTP 400
HTTP 404
HTTP 429
HTTP 500
```

说明底层至少已经走到了 HTTP 层。

关键点：

```text
HTTP 500 不是 TCP 失败。
HTTP 429 不是网络不通。
HTTP 404 不是端口没开。
```

HTTP status 是协议/应用层结果，不是底层网络连通性的直接证据。

---

### 3.8 proxy/gateway

proxy/gateway 是中间层，典型路径：

```text
client -> gateway -> upstream
```

它经常把通信拆成两段：

```text
连接 A：client <-> gateway
连接 B：gateway <-> upstream
```

gateway 会：

```text
接收 downstream request
根据规则转发
作为新的 client 请求 upstream
返回 upstream 的结果或自己的错误
```

所以：

```text
HTTP 502/504 可能说明 client 到 gateway 成功，
但 gateway 到 upstream 失败或超时。
```

不能简单把 502/504 理解成“客户端网络不通”。

---

### 3.9 upstream

upstream 是真正处理请求的后端服务。

例如：

```text
RAG API
模型推理服务
数据库服务
内部 RPC 服务
业务应用 server
```

如果 upstream 日志完全没有请求，可能说明失败发生在 upstream 之前。

但如果中间有 gateway，还要进一步区分：

```text
client -> gateway 是否成功
gateway -> upstream 是否成功
```

---

## 4. 代码可见 vs OS/网络环境决定

这里的区别不是“代码里有没有写死”，而是：

```text
代码可见：
应用代码能主动指定、调用、配置、捕获错误，或从响应中直接观察。

OS/网络环境决定：
应用代码通常不直接控制，需要通过 OS 配置、路由表、DNS 配置、防火墙、网络设备、代理配置等决定。
```

大致分类：

```text
强可见：
application intent
socket
TLS
HTTP

半可见：
DNS
TCP/UDP
proxy/gateway
upstream

弱可见 / 主要由环境决定：
route
ARP
NAT
firewall
security group
```

具体理解：

- DNS：代码知道要解析哪个域名，也可能捕获 DNS 错误；但使用哪个 DNS server 常由系统/网络配置决定。
- route：代码通常只给目标 IP，具体走哪块网卡、哪个网关由 OS 路由表决定。
- TCP：代码能看到 connect/refused/timeout/reset，但三次握手、重传、拥塞控制主要由 OS 协议栈处理。
- TLS/HTTP：应用或库能直接看到握手错误、HTTP status、headers、body。

---

## 5. Layer Map、Packet、Connection、Request 的关系

这是 Week00 最容易混淆、但最关键的一部分。

### 5.1 Layer map 不是一个 packet 的结构

Layer map 是排障依赖链：

```text
application intent
-> DNS
-> route
-> socket
-> TCP/UDP
-> TLS
-> HTTP
-> proxy/gateway
-> upstream
```

它回答的是：

```text
如果一次服务访问失败，可能失败在哪一层？
```

它不是严格描述单个 packet 的发送过程。

---

### 5.2 一次应用请求通常包含多个协议动作

一次 HTTPS 请求大致会经历：

```text
DNS 查询
-> route/ARP 选择路径和下一跳
-> TCP 三次握手
-> TLS 握手
-> HTTP request
-> HTTP response
-> TCP 连接复用或关闭
```

所以一次“请求”不是一个单向动作，而是一组网络交互。

---

### 5.3 时间线 vs 封装结构

时间线描述先后顺序：

```text
DNS Query
-> DNS Answer
-> TCP SYN
-> TCP SYN-ACK
-> TCP ACK
-> TLS ClientHello
-> TLS ServerHello/Certificate
-> HTTP Request
-> HTTP Response
```

封装结构描述每一次真实发包时 packet 里有什么：

```text
DNS Query                    DNS -> UDP -> IP -> Ethernet
DNS Answer                   DNS -> UDP -> IP -> Ethernet
TCP SYN                      TCP -> IP -> Ethernet
TCP SYN-ACK                  TCP -> IP -> Ethernet
TCP ACK                      TCP -> IP -> Ethernet
TLS ClientHello              TLS -> TCP -> IP -> Ethernet
TLS ServerHello/Certificate  TLS -> TCP -> IP -> Ethernet
HTTP Request over HTTPS      HTTP -> TLS -> TCP -> IP -> Ethernet
HTTP Response over HTTPS     HTTP -> TLS -> TCP -> IP -> Ethernet
```

关键点：

```text
不是所有包都有 HTTP/TLS。
包里有什么层，取决于这个包正在完成什么协议动作。
```

---

### 5.4 发送端封装，接收端解封装

发送 HTTPS request 时：

```text
HTTP request
-> TLS 加密
-> TCP 分段
-> IP 加目标地址
-> Ethernet/Wi-Fi 加下一跳 MAC
-> 发出
```

接收端反向处理：

```text
Ethernet/Wi-Fi
-> IP
-> TCP
-> TLS 解密
-> HTTP 解析
-> 交给应用代码
```

业务代码通常只看到 HTTP 层之后的内容，不会直接处理 Ethernet/IP/TCP header。

---

### 5.5 HTTP request、TCP connection、packet、业务请求不是一回事

```text
业务请求：
用户想完成的一件事，例如问模型一个问题。

HTTP 请求：
一次 POST /v1/chat/completions。

TCP 连接：
client_ip:port <-> server_ip:443 的可靠有序字节流通道。

packet：
网络中实际传输的单个封装单位。
```

它们不是一一对应关系：

```text
一个 HTTP request 可能被拆成多个 TCP segment / packet。
一个 TCP connection 可以承载多个 HTTP request。
一个业务请求可能触发多个 HTTP/RPC 调用。
一个 gateway 请求后面可能转发成新的 upstream 请求。
```

最重要的一句话：

```text
HTTP request 不是 packet。
TCP connection 不是 request。
packet 是每一次实际传输的封装单位。
```

---

## 6. 后端应用没有日志时，可能失败在哪里？

如果最终 application server / upstream server 完全没有这次请求日志，可能失败在：

```text
application intent 配错
DNS 失败
route 选错或无路由
ARP/本地链路失败
NAT/firewall/security group 丢包
socket connect 失败
TCP 握手失败
TLS 握手失败
proxy/gateway 到 upstream 失败
```

注意：

如果客户端收到了：

```text
HTTP 502
HTTP 504
```

这可能是 gateway 返回的，最终 upstream application server 仍然可能完全没收到请求。

但如果客户端收到的是 upstream 自己返回的：

```text
HTTP 200
HTTP 400
HTTP 500
```

那说明请求至少到达了某个 HTTP 应用处理层。

---

## 7. 四类证据

排障不能只靠一种证据。不同证据能证明的东西不同。

### 7.1 logs

logs 是组件内部记录的事件。

适合证明：

```text
某个组件是否收到请求
某个组件内部做了什么判断
错误是在谁那里被记录的
请求有没有 trace id
```

例子：

```text
received request /v1/chat
upstream timeout
TLS handshake failed
connection refused
```

局限：

```text
没打日志的事情看不到。
应用没日志不代表包一定没到，也可能是日志级别、日志采集、trace id 断了。
```

---

### 7.2 metrics

metrics 是一段时间内的统计和趋势。

适合证明：

```text
是否整体变慢
是否错误率升高
是否容量不足
是否 p95/p99 latency 恶化
是否 429/5xx/timeout 增多
```

例子：

```text
QPS
error rate
p95 latency
connection count
timeout count
queue depth
CPU/GPU usage
HTTP 429 count
```

局限：

```text
metrics 通常不能解释单个请求到底发生了什么。
```

例如 p95 latency 上升，只能说明慢了，不能直接说明是 DNS 慢、TCP 慢、TLS 慢，还是 upstream 推理慢。

---

### 7.3 command output

command output 是当前机器/当前时刻的状态快照或即时探测结果。

适合证明：

```text
当前 IP 是什么
DNS server 是什么
默认网关是什么
路由表怎么选路
端口是否监听
域名当前解析到哪里
ping/traceroute 当前表现如何
```

例子：

```powershell
ipconfig /all
route print
nslookup example.com
ping 8.8.8.8
tracert example.com
netstat -ano
```

局限：

```text
它通常只是某一时刻的快照。
现在正常，不代表故障发生时也正常。
```

---

### 7.4 packet capture

packet capture 是包级真实交互证据。

适合证明：

```text
包到底有没有发出机器
对方到底有没有回应
有没有 DNS query / answer
有没有 TCP SYN / SYN-ACK
有没有 TLS ClientHello
有没有 HTTP request
有没有 reset / retransmission / FIN
失败卡在哪一层
```

局限：

```text
HTTPS payload 加密后看不到明文 body。
抓错网卡会误判。
信息量很大，需要理解协议结构。
```

---

### 7.5 证据类型总结

```text
logs:
证明组件内部看到和记录了什么。

metrics:
证明一段时间内系统状态和趋势。

command output:
证明当前机器/网络配置和即时探测结果。

packet capture:
证明线上真实包级交互，尤其适合判断请求是否发出、是否收到回应、卡在哪一层。
```

重要原则：

```text
一个信号通常不能证明所有层。
排障时要组合 logs、metrics、command output、packet capture。
```

---

## 8. 本周修正过的关键误区

### 8.1 误区：把“网络问题”当成一类问题

修正：

```text
“网络问题”不是一类问题，而是一条通信路径上不同层次的失败。
```

要问：

```text
DNS 是否成功？
route 是否选对？
TCP 是否连上？
TLS 是否握手成功？
HTTP 是否有响应？
gateway 是否正常转发？
upstream 是否收到并处理？
```

---

### 8.2 误区：把 layer map 理解成一个 packet 的发送过程

修正：

```text
Layer map 是排障依赖链，不是单个 packet 的结构。
```

每个协议动作最终都会变成一个或多个 packet，但不同动作的 packet 结构不同。

---

### 8.3 误区：认为每个 packet 都是 HTTP -> TLS -> TCP -> IP -> Ethernet

修正：

```text
DNS 包可能是 DNS -> UDP -> IP -> Ethernet。
TCP 握手包是 TCP -> IP -> Ethernet。
TLS 握手包是 TLS -> TCP -> IP -> Ethernet。
HTTPS 请求包才是 HTTP -> TLS -> TCP -> IP -> Ethernet。
```

---

### 8.4 误区：把 HTTP request、TCP connection、packet 混在一起

修正：

```text
HTTP request 是应用层语义。
TCP connection 是传输层字节流通道。
packet 是网络中实际传输的封装单位。
```

它们不是一一对应关系。

---

### 8.5 误区：后端应用没日志，就以为是应用自己的问题

修正：

```text
后端应用没日志，说明请求可能根本没到应用层。
```

可能失败在：

```text
DNS
route
ARP
NAT/firewall
TCP
TLS
gateway -> upstream
```

---

### 8.6 误区：看到 HTTP 502/504 就以为客户端到服务不通

修正：

```text
502/504 往往说明 client 到 gateway 已经成功，
但 gateway 到 upstream 失败、超时，或 gateway 内部策略/容量出问题。
```

---

## 9. Week00 自测问题与答案

### Q1：哪些层是代码可见的？哪些由 OS/网络环境决定？

代码强可见：

```text
application intent
socket
TLS
HTTP
```

半可见：

```text
DNS
TCP/UDP
proxy/gateway
upstream
```

主要由 OS/网络环境决定：

```text
route
ARP
NAT
firewall/security group
```

核心理解：

```text
代码通常指定“我要访问谁”，但不直接编排“从哪块网卡出去、走哪个网关、经过哪些路由器”。
```

---

### Q2：哪些层可以在 application server 收到请求前失败？

可能失败在：

```text
application intent 配错
DNS 失败
route 失败
ARP/本地链路失败
firewall/NAT/security group 丢包
socket connect 失败
TCP 握手失败
TLS 握手失败
proxy/gateway 到 upstream 失败
```

如果有 gateway，要区分：

```text
client -> gateway
gateway -> upstream
```

---

### Q3：logs、metrics、command output、packet capture 的区别？

```text
logs:
组件内部事件，证明某个组件看到并记录了什么。

metrics:
趋势和统计，证明系统整体状态、容量、延迟、错误率变化。

command output:
当前状态快照，证明当前 IP、DNS、route、端口、即时探测结果。

packet capture:
包级事实，证明真实流量有没有发出、有没有回应、卡在哪一层。
```

---

### Q4：每次 lab 的 notes.md 应该记什么？

以后每个 week 的 notes 尽量固定包含：

```text
本周核心问题
自己的概念定义
跑过的命令
关键输出摘要
观察到的现象
修正过的误区
以后可复用的排查 checklist
```

目标不是写学习感想，而是形成以后可以复用的排障模板。

---

## 10. Week00 最核心总结

### 10.1 一句话版本

```text
Layer map 是排障视角下的通信依赖链；
协议栈是每次发包时的封装/解封装结构；
一次请求是应用层语义，可能跨多个 packet、复用一个 TCP 连接，并经过多个中间组件。
```

### 10.2 工程排障版本

```text
先看 application intent 是否正确；
再看 DNS 是否解析成功；
再看 route 是否选对路径；
再看 socket/TCP/UDP 是否连通；
再看 TLS 是否握手成功；
再看 HTTP 是否有响应；
再看 proxy/gateway 是否正确转发；
最后看 upstream/application 是否收到并处理。
```

### 10.3 最重要的边界

```text
DNS 成功 != TCP 成功
TCP 成功 != TLS 成功
TLS 成功 != HTTP 成功
HTTP 500/429 != 底层网络不通
HTTP 502/504 可能是 gateway 到 upstream 的问题
后端无日志 != 一定是后端应用代码问题
```