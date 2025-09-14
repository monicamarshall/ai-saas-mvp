import hashlib
from pathlib import Path
BASE = Path("storage")
BASE.mkdir(exist_ok=True)
def put_bytes(key:str, b:bytes) -> tuple[str,str]:
    path = BASE / key
    path.parent.mkdir(parents=True, exist_ok=True)
    checksum = hashlib.sha256(b).hexdigest()
    path.write_bytes(b)
    return str(path), checksum
def get_bytes(key:str) -> bytes:
    path = BASE / key
    return path.read_bytes()
