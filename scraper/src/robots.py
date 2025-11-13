# import urllib.robotparser
#
# def can_fetch(url, user_agent="*"):
#     rp = urllib.robotparser.RobotFileParser()
#     domain = "/".join(url.split("/")[:3])
#     rp.set_url(f"{domain}/robots.txt")
#     rp.read()
#     return rp.can_fetch(user_agent, url)
# src/robots.py

import urllib.robotparser
import threading
from datetime import datetime

_rp_cache = {}
_cache_lock = threading.Lock()

def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

def can_fetch(url, user_agent="*"):
    domain = "/".join(url.split("/")[:3])

    with _cache_lock:
        if domain in _rp_cache:
            rp = _rp_cache[domain]
        else:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{domain}/robots.txt")
            try:
                rp.read()
            except Exception as e:
                log(f"[robots.txt] Failed to read {domain}/robots.txt: {e}")
            _rp_cache[domain] = rp

    allowed = rp.can_fetch(user_agent, url)

    status = "ALLOWED" if allowed else "BLOCKED"
    log(f"[{status}] {url}")

    return allowed


