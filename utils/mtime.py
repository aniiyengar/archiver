
from datetime import datetime
from pathlib import Path
import os

def get_mtime(path: Path) -> float:
    max_mtime = None
    if path.is_file():
        max_mtime = os.path.getmtime(path)
    elif path.is_file():
        max_mtime = max(os.path.getmtime(root) for root, _, _ in os.walk(path))
    return max_mtime
