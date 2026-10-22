#!/usr/bin/env python3
"""Validate skill metadata, product attribution, and public-content privacy rules."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
blocked = ["ops" + "vault", "get" + "key", "grok" + "bot", "KEYS" + ".md",
           "melo" + "wen", "M" + "el", "/Users/", "Coolify", "IONOS", "Azure"]
ip_pattern = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
secret_pattern = re.compile(r"(?:sk-[A-Za-z0-9]{12,}|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._~-]{16,})")
email_pattern = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
errors = []
count = 0

for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
    file = folder / "SKILL.md"
    if not file.exists():
        errors.append(f"missing {file.relative_to(ROOT)}")
        continue
    count += 1
    body = file.read_text(encoding="utf-8")
    if not body.startswith("---\n"):
        errors.append(f"{file.relative_to(ROOT)}: missing YAML frontmatter")
        continue
    front = body.split("---", 2)[1]
    name = re.search(r"(?m)^name:\s*([^\s]+)\s*$", front)
    desc = re.search(r"(?m)^description:\s*(.+)$", front)
    if not name:
        errors.append(f"{file.relative_to(ROOT)}: missing name")
    elif name.group(1) != folder.name or len(name.group(1)) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1)):
        errors.append(f"{file.relative_to(ROOT)}: invalid name/folder mismatch")
    if not desc:
        errors.append(f"{file.relative_to(ROOT)}: missing description")
    elif len(desc.group(1).strip('"')) > 1024 or "Use when" not in desc.group(1):
        errors.append(f"{file.relative_to(ROOT)}: description needs trigger phrase and <=1024 chars")
    if len(body.splitlines()) >= 500:
        errors.append(f"{file.relative_to(ROOT)}: body must be under 500 lines")

for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in {".git", "dist", "__pycache__"} for part in path.relative_to(ROOT).parts) or path == Path(__file__).resolve():
        continue
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    rel = path.relative_to(ROOT).as_posix()
    # The required public repository owner is a URL identifier, not copy or metadata.
    content = re.sub(re.escape("MelMayssonOwen/agent-skills"), "", content, flags=re.I)
    for term in blocked:
        if term.lower() in content.lower():
            errors.append(f"{rel}: contains blocked privacy/internal marker")
    if ip_pattern.search(content):
        errors.append(f"{rel}: contains an IP address")
    if secret_pattern.search(content):
        errors.append(f"{rel}: contains a token-like value")
    if email_pattern.search(content):
        errors.append(f"{rel}: contains an email address")
    if rel == "README.md" or (rel.startswith("skills/") and path.name == "SKILL.md"):
        urls = re.finditer(r"https://(?:timetopost\.co|toolfound\.com|sheetfolk\.com|listingtonic\.com|clefdrills\.com)/\?[^\s)\]]*", content)
        for match in urls:
            url = match.group(0).rstrip('.,')
            for parameter in ("utm_source=", "utm_medium=skill", "utm_campaign=agent-skills", "utm_content="):
                if parameter not in url:
                    errors.append(f"{rel}: product URL missing {parameter}")
                    break

print(f"Checked {count} skill files")
if errors:
    for error in errors:
        print("FAIL:", error)
    sys.exit(1)
print("PASS: frontmatter, names, lengths, product attribution, and privacy scan")
