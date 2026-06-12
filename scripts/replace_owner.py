"""Replace YOUR_ORG placeholders before publishing the repository."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".toml", ".yml", ".yaml", ".cff", ".txt"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("owner", help="GitHub owner or organization name")
    args = parser.parse_args()
    changed = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES and ".git" not in path.parts:
            text = path.read_text(encoding="utf-8")
            new = text.replace("YOUR_ORG", args.owner)
            if new != text:
                path.write_text(new, encoding="utf-8")
                changed.append(path.relative_to(ROOT))
    for path in changed:
        print(path)
    print(f"Updated {len(changed)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
