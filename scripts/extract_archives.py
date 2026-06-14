from __future__ import annotations

import tarfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DIR = REPO_ROOT / "archives"
ARCHIVES = [
    "healthy.tar",
    "minor.tar",
    "serious.tar",
    "loss.tar",
    "fishnet.tar",
    "plastic.tar",
    "3mm.tar",
]


def is_safe_member(member: tarfile.TarInfo, destination: Path) -> bool:
    target = (destination / member.name).resolve()
    return str(target).startswith(str(destination.resolve()))


def main() -> int:
    for archive_name in ARCHIVES:
        archive_path = ARCHIVE_DIR / archive_name
        if not archive_path.exists():
            print(f"Missing archive: {archive_path}")
            return 1

        print(f"Extracting {archive_name}...")
        with tarfile.open(archive_path, mode="r") as tar:
            members = tar.getmembers()
            unsafe = [m.name for m in members if not is_safe_member(m, REPO_ROOT)]
            if unsafe:
                print(f"Refusing unsafe paths in {archive_name}: {unsafe[:5]}")
                return 1
            tar.extractall(REPO_ROOT, members=members)

    print("Done. Dataset restored under gcm_t_input_dataset_with_rpm_info/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
