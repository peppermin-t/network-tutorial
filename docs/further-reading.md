# Further Reading

Keep this list small and official. Use it when a lab raises a concept you want to verify from primary documentation.

## Python Socket / SSL

- Python `socket`: https://docs.python.org/3/library/socket.html
- Python `ssl`: https://docs.python.org/3/library/ssl.html
- Python `http.server`, for comparison with this repo's tiny HTTP code: https://docs.python.org/3/library/http.server.html

## DNS

- Cloudflare Learning Center, DNS: https://www.cloudflare.com/learning/dns/what-is-dns/
- Cloudflare Learning Center, DNS records: https://www.cloudflare.com/learning/dns/dns-records/
- RFC 1035, DNS implementation details: https://www.rfc-editor.org/rfc/rfc1035

## HTTP

- MDN HTTP overview: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview
- MDN HTTP messages: https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
- MDN `Transfer-Encoding`: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding
- MDN 429 status: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429

## TLS

- Cloudflare Learning Center, TLS: https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/
- MDN Transport Layer Security: https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security
- RFC 8446, TLS 1.3: https://www.rfc-editor.org/rfc/rfc8446

## Docker Networking

- Docker networking overview: https://docs.docker.com/network/
- Docker Compose networking: https://docs.docker.com/compose/how-tos/networking/
- Docker bridge driver: https://docs.docker.com/engine/network/drivers/bridge/

## Wireshark / TShark

- Wireshark User's Guide: https://www.wireshark.org/docs/wsug_html_chunked/
- Wireshark display filters: https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html
- TShark manual page: https://www.wireshark.org/docs/man-pages/tshark.html

## Proxy / Gateway

- MDN proxy servers and tunneling: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Proxy_servers_and_tunneling
- Cloudflare reverse proxy overview: https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/
- NGINX reverse proxy admin guide, as production contrast: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/

## Timeout / Retry / Backpressure

- Google SRE Book, Handling Overload: https://sre.google/sre-book/handling-overload/
- Google SRE Book, Addressing Cascading Failures: https://sre.google/sre-book/addressing-cascading-failures/
- Microsoft retry pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/retry

## VPN Mental Model

- Microsoft Always On VPN routing options: https://learn.microsoft.com/en-us/windows-server/remote/remote-access/vpn/always-on-vpn/
- Microsoft VPN split tunneling: https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/vpn/vpn-routing
- Red Hat networking guide, MTU overview: https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_networking/

## Model Serving / Streaming APIs

- OpenAI streaming API docs, for network behavior comparison: https://platform.openai.com/docs/api-reference/streaming
- MDN Server-Sent Events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- Kubernetes service networking, for production service-name contrast: https://kubernetes.io/docs/concepts/services-networking/service/
