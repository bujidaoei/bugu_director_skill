"""Check planning structure and local references; does not validate production."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def validate(root: Path) -> dict:
    root = root.resolve(strict=True)
    feature = root / "specs/001-director-runtime"
    errors: list[str] = []
    required = ["spec.md", "plan.md", "research.md", "data-model.md", "quickstart.md", "tasks.md",
                "contracts/cli.md", "contracts/lifecycle.md", "contracts/production.md",
                "contracts/review.md", "contracts/delivery.md", "research/source-context.md",
                "research/core-suite.md", "research/supporting-suites.md", "research/upstream-integration.md"]
    for name in required:
        if not (feature / name).is_file():
            errors.append(f"Missing document: {name}")
    spec = (feature / "spec.md").read_text(encoding="utf-8")
    tasks = (feature / "tasks.md").read_text(encoding="utf-8")
    requirements = re.findall(r"\*\*((?:FR|SC)-\d{3})\*\*:", spec)
    if len(requirements) != len(set(requirements)):
        errors.append("Duplicate requirement IDs")
    task_rows = [line for line in tasks.splitlines() if re.match(r"^- \[[ xX]\] T", line)]
    task_ids = []
    referenced_requirements: set[str] = set()
    for line in task_rows:
        match = re.match(r"^- \[([ xX])\] (T\d{3})(?: \[P\])?(?: \[US[1-6]\])? (.+)$", line)
        if not match:
            errors.append("Malformed task row")
            continue
        task_ids.append(match[2])
        mapped = set(re.findall(r"\b(?:FR|SC)-\d{3}\b", line))
        referenced_requirements.update(mapped)
        if not mapped:
            errors.append(f"Task lacks explicit requirement mapping: {match[2]}")
        if not re.search(r"(?:src|tests|skills|specs|tools|deploy|workflows|docs|licenses|\.github|\.specify)/|pyproject\.toml|uv\.lock|README\.md|THIRD_PARTY_NOTICES\.md", line):
            errors.append(f"Task lacks target path: {match[2]}")
    if task_ids != [f"T{index:03d}" for index in range(1, len(task_ids) + 1)]:
        errors.append("Task IDs must be sequential and unique")
    missing = sorted(set(requirements) - referenced_requirements)
    unknown = sorted(referenced_requirements - set(requirements))
    if missing:
        errors.append("Unmapped requirements: " + ", ".join(missing))
    if unknown:
        errors.append("Unknown requirement references: " + ", ".join(unknown))
    documents = [root / "README.md", root / "THIRD_PARTY_NOTICES.md", root / "docs/enterprise-plan.md"]
    documents += sorted(feature.rglob("*.md"))
    checked_links = 0
    hashes = {}
    for document in documents:
        content = document.read_text(encoding="utf-8")
        hashes[document.relative_to(root).as_posix()] = hashlib.sha256(document.read_bytes()).hexdigest()
        if re.search(r"\[NEEDS CLARIFICATION|\[FEATURE NAME\]|\[Brief Title\]|\[DATE\]", content):
            errors.append(f"Unresolved scaffold: {document.relative_to(root)}")
        for target in re.findall(r"(?<!!)\[[^\]\n]*\]\(([^\n)]+)\)", content):
            target = target.strip().strip("<>")
            if not target or target.startswith("#") or urlsplit(target).scheme:
                continue
            path = unquote(target.split("#", 1)[0])
            checked_links += 1
            if not (document.parent / path).resolve().exists():
                errors.append(f"Broken local link in {document.relative_to(root)}: {target}")
    json_count = 0
    for document in sorted((feature / "evidence").glob("*.json")):
        json.loads(document.read_text(encoding="utf-8"))
        json_count += 1
    return {"schema_version": 1, "observed_at_utc": datetime.now(timezone.utc).isoformat(),
            "scope": "Planning structure, explicit task coverage, JSON parsing and local file links only",
            "production_acceptance": "not-run", "formal_release_eligible": False,
            "requirements": len(requirements), "tasks": len(task_ids),
            "completed_task_ids": [re.search(r"T\d{3}", row)[0] for row in task_rows if row.startswith(("- [x]", "- [X]"))],
            "unmapped_requirements": missing, "unknown_requirement_references": unknown,
            "checked_local_links": checked_links, "json_files_parsed": json_count,
            "document_hashes": hashes, "errors": errors, "result": "pass" if not errors else "fail"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in result.items() if key != "document_hashes"}, ensure_ascii=False))
    raise SystemExit(0 if result["result"] == "pass" else 1)


if __name__ == "__main__":
    main()
