"""Scaffold a new Architecture Decision Record (ADR).

Usage:
    python scripts/new-adr.py "Title of the decision"

Creates docs/collaboration/adrs/NNNN-title-of-the-decision.md using the ADR
template, and prints the path of the new file.
"""

import re
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_ADR_DIR = _REPO_ROOT / "docs" / "collaboration" / "adrs"
_TEMPLATE = _REPO_ROOT / "docs" / "collaboration" / "templates" / "adr-template.md"


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "untitled-decision"


def next_number() -> int:
    existing = list(_ADR_DIR.glob("*.md")) if _ADR_DIR.is_dir() else []
    numbers = []
    for path in existing:
        match = re.match(r"(\d{4})-", path.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)

    title = " ".join(sys.argv[1:])
    _ADR_DIR.mkdir(parents=True, exist_ok=True)

    number = next_number()
    filename = f"{number:04d}-{slugify(title)}.md"
    target = _ADR_DIR / filename

    template = _TEMPLATE.read_text(encoding="utf-8") if _TEMPLATE.is_file() else ""
    content = template.replace("ADR-NNNN: Title of the decision", f"ADR-{number:04d}: {title}")

    target.write_text(content, encoding="utf-8")
    print(f"Created {target.relative_to(_REPO_ROOT)}")


if __name__ == "__main__":
    main()
