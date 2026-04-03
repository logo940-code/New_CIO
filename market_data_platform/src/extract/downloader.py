from pathlib import Path
from datetime import datetime
from src.core.http import fetch_bytes
from src.core.hashing import sha256_bytes


def download_to_raw(url: str, raw_dir: Path) -> tuple[Path, str, bytes]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    content = fetch_bytes(url)
    digest = sha256_bytes(content)
    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{digest[:12]}"
    path = raw_dir / filename
    path.write_bytes(content)
    return path, digest, content
