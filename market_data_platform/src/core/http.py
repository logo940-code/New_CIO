import httpx


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.content
