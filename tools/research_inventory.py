"""Create a read-only, reproducible source inventory for research evidence."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def snapshot(source: Path) -> dict:
    source = source.resolve(strict=True)
    if not source.is_dir():
        raise ValueError("Source must be a directory")
    files = []
    for path in sorted(source.rglob("*"), key=lambda value: value.as_posix()):
        if path.is_symlink():
            raise ValueError(f"Source contains a symlink: {path.relative_to(source)}")
        if not path.is_file():
            continue
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        files.append({"path": path.relative_to(source).as_posix(),
                      "size": path.stat().st_size, "sha256": digest.hexdigest()})
    canonical = json.dumps(files, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    return {
        "schema_version": 1,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_root": str(source),
        "scope": "All regular files including pre-existing caches; no source mutation",
        "file_count": len(files),
        "byte_count": sum(row["size"] for row in files),
        "skill_count": sum(row["path"].endswith("/SKILL.md") for row in files),
        "top_level_file_counts": dict(sorted(Counter(row["path"].split("/")[0] for row in files).items())),
        "manifest_sha256": hashlib.sha256(canonical).hexdigest(),
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = snapshot(args.source)
    output = args.output.resolve()
    if output == args.source.resolve() or args.source.resolve() in output.parents:
        raise ValueError("Output must not be inside the read-only reference tree")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in result.items() if key != "files"}, ensure_ascii=True))


if __name__ == "__main__":
    main()
