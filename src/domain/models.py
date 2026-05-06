import ipaddress
import socket
from dataclasses import dataclass
from typing import List

class AnalyzeRequestUrl:
    def __init__(self, url: str):
        self.url = url
        self._validate_ssrf()

    def _validate_ssrf(self):
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        host = parsed.hostname
        if not host:
            raise ValueError("Invalid URL: missing hostname")
        
        # Check explicit localhost
        if host.lower() in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            raise ValueError("SSRF Check Failed: Localhost is not allowed.")
            
        # Try to resolve IP to prevent DNS rebinding to local IPs
        try:
            ip_addr = socket.gethostbyname(host)
            ip = ipaddress.ip_address(ip_addr)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                raise ValueError("SSRF Check Failed: Private/Local IP ranges are not allowed.")
        except socket.gaierror:
            # If DNS resolution fails, let it pass here and let httpx fail, 
            # or we could block it. Letting it pass to httpx is standard.
            pass

@dataclass
class CategorizationResult:
    title: str
    summary: str
    categories: List[str]
