from __future__ import annotations

import csv
import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "metadata" / "archive_manifest.csv"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024 * 8), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not MANIFEST.exists():
        print(f"Missing manifest: {MANIFEST}")
        return 1

    errors: list[str] = []
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            archive_path = REPO_ROOT / "archives" / row["archive"]
            if not archive_path.exists():
                errors.append(f"missing {archive_path}")
                continue
            size = archive_path.stat().st_size
            expected_size = int(row["archive_bytes"])
            if size != expected_size:
                errors.append(f"{row['archive']}: size {size} != {expected_size}")
            actual_hash = sha256_file(archive_path)
            if actual_hash != row["sha256"]:
                errors.append(f"{row['archive']}: sha256 mismatch")

    if errors:
        print("FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK: all archives match metadata/archive_manifest.csv.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
