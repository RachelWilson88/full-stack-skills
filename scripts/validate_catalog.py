#!/usr/bin/env python3
"""Validate README package inventory and headline counts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_RE = re.compile(
    r"^\| \[([^]]+)\]\(https://github\.com/full-stack-skills/([^)]+)\) \| ([0-9]+) \|",
    re.MULTILINE,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def read_inventory() -> list[str]:
    return [
        line.strip()
        for line in (ROOT / "scripts/repositories.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def validate_readme(path: Path, expected: set[str]) -> int:
    text = path.read_text(encoding="utf-8")
    rows = REPOSITORY_RE.findall(text)
    repositories = [repository for label, repository, _ in rows if label == repository]
    counts = [int(count) for label, repository, count in rows if label == repository]
    errors = 0

    duplicates = sorted({name for name in repositories if repositories.count(name) > 1})
    missing = sorted(expected - set(repositories))
    unexpected = sorted(set(repositories) - expected)
    for label, values in (("duplicate", duplicates), ("missing", missing), ("unexpected", unexpected)):
        if values:
            fail(f"{path.name}: {label} repositories: {', '.join(values)}")
            errors += 1

    headline = re.search(
        r"\*\*([0-9]+)(?: 个)? Agent Skills[。.]\s*([0-9]+)(?: 个技能包| Skill Packages)",
        text,
    )
    if not headline:
        fail(f"{path.name}: headline counts not found")
        return errors + 1
    declared_skills, declared_packages = map(int, headline.groups())
    if declared_packages != len(expected):
        fail(f"{path.name}: declares {declared_packages} packages, expected {len(expected)}")
        errors += 1
    if declared_skills != sum(counts):
        fail(f"{path.name}: declares {declared_skills} skills, table sums to {sum(counts)}")
        errors += 1

    snapshot = json.loads((ROOT / "docs/catalog-inventory.json").read_text(encoding="utf-8"))
    recorded = {row["repository"].split("/")[1]: row["skills"] for row in snapshot["packages"]}
    documented = {repository: int(count) for label, repository, count in rows if label == repository}
    if recorded != documented:
        fail(f"{path.name}: package counts differ from the source snapshot")
        errors += 1

    # 分类小计及汇总表必须与该分类实际收录的包一致，社区推荐不参与求和。
    for heading, body in re.findall(r"^### (.+)\n([\s\S]*?)(?=^### |^## |\Z)", text, re.MULTILINE):
        subtotal = re.search(r"[（(]([0-9]+) (?:个技能|skills)[）)]", heading)
        package_rows = [(label, int(count)) for label, repository, count in REPOSITORY_RE.findall(body) if label == repository]
        if not subtotal or not package_rows:
            continue
        actual = sum(count for _, count in package_rows)
        if int(subtotal.group(1)) != actual:
            fail(f"{path.name}: category {heading} sums to {actual}")
            errors += 1
        label = heading[:subtotal.start()].strip()
        summary = f"| {label} | {len(package_rows)} | {actual} |"
        if summary not in text:
            fail(f"{path.name}: category summary missing or inconsistent: {label}")
            errors += 1

    print(f"{path.name}: {len(repositories)} packages, {sum(counts)} skills")
    return errors


def main() -> int:
    inventory = read_inventory()
    if inventory != sorted(set(inventory)):
        fail("scripts/repositories.txt must be sorted and unique")
        return 1
    expected = set(inventory)
    errors = sum(validate_readme(ROOT / name, expected) for name in ("README.md", "README.en.md"))
    index = (ROOT / "SKILLS_INDEX.md").read_text(encoding="utf-8")
    index_rows = re.findall(r"^## ([^\s]+)（([0-9]+) 个技能）\n\n([^\n]+)", index, re.MULTILINE)
    indexed = {package: int(count) for package, count, _ in index_rows}
    snapshot = json.loads((ROOT / "docs/catalog-inventory.json").read_text(encoding="utf-8"))
    recorded = {row["repository"].split("/")[1]: row["skills"] for row in snapshot["packages"]}
    if len(recorded) != len(snapshot["packages"]) or set(recorded) != expected or indexed != recorded:
        fail("index, source snapshot and repository inventory differ")
        errors += 1
    for package, count, names in index_rows:
        if len(re.findall(r"`[^`]+`", names)) != int(count):
            fail(f"index: {package} skill names do not match its count")
            errors += 1
    for row in snapshot["packages"]:
        if not re.fullmatch(r"[0-9a-f]{40}", row["commit"]):
            fail(f"snapshot: invalid commit for {row['repository']}")
            errors += 1
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
