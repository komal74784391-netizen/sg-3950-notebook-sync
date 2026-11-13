import hashlib
import shutil
from pathlib import Path


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sync_folder(source: str, target: str) -> list:
    source_dir = Path(source)
    target_dir = Path(target)
    target_dir.mkdir(parents=True, exist_ok=True)
    changed = []
    for item in source_dir.rglob("*"):
        if not item.is_file():
            continue
        destination = target_dir / item.relative_to(source_dir)
        if not destination.exists() or file_digest(item) != file_digest(destination):
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)
            changed.append(str(destination))
    return changed
