#!/usr/bin/env python3
"""Build per-skill ZIPs for a marketplace slug and rewrite source attribution."""
import argparse
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def build(slug):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", slug):
        raise ValueError("slug must use lowercase letters, digits, and hyphens")
    output = ROOT / "dist" / slug
    output.mkdir(parents=True, exist_ok=True)
    for folder in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
        archive = output / f"{folder.name}.zip"
        with ZipFile(archive, "w", ZIP_DEFLATED) as z:
            for path in sorted(folder.rglob("*")):
                if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                    continue
                data = path.read_bytes()
                if path.suffix.lower() in {".md", ".py", ".json", ".toml"}:
                    data = data.replace(b"utm_source=github", f"utm_source={slug}".encode())
                z.writestr(f"{folder.name}/{path.relative_to(folder).as_posix()}", data)
        print(archive.relative_to(ROOT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="marketplace source slug, such as skillsmp")
    build(parser.parse_args().slug)
