# Week 07 - TLS

Focus: Python `ssl`, certificate validation, SNI, ALPN/cipher observation.

Run:

```powershell
$env:PYTHONPATH="src"
python -m netlab client https --host example.com --port 443 --path /
```

Optional local certificate generation:

```powershell
openssl req -x509 -newkey rsa:2048 -nodes -keyout localhost.key -out localhost.crt -days 7 -subj "/CN=localhost"
```

Questions:

- 证书校验失败和 TCP 连接失败有什么区别？
- SNI 为什么对多域名 HTTPS 服务重要？
- TLS 保护了什么，没保护什么？

Wireshark task:

- Capture `tcp port 443` while calling `example.com`.
- Use display filter `tls`.
- Identify ClientHello, SNI, ServerHello, certificate, and encrypted application data.

## Systematic Template

- Concept Model: Secure Transport. TLS protects bytes after TCP connects and before HTTP is readable.
- Code Lab: Run HTTPS client and inspect cipher/body.
- Failure Lab: Use an invalid certificate endpoint when available; classify with `python -m netlab fault classify tls-verify-failed`.
- Wireshark Lab: Use `tls` and find ClientHello, SNI, and encrypted application data.
- Work Mapping: Cloud APIs, private gateways, and model endpoints commonly fail at certificate/SNI boundaries.
