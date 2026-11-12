#!/usr/bin/env python3
"""Refresh this repo from the skills' source folder and rebuild the downloads.

    python3 tools/build.py <path-to-source-external-folder>

1. Copies every skill folder (a folder with SKILL.md) from the source into
   plugins/inro-agency-skills/skills/, replacing what is there.
2. Checks each SKILL.md: frontmatter keys claude.ai accepts, name matches the folder.
3. Writes downloads/<name>.zip (the folder at the zip root, ready to upload in claude.ai)
   and downloads/inro-agency-skills-all.zip.
4. Rewrites the skills table in README.md between the SKILLS markers.
"""
import pathlib
import re
import shutil
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = ROOT / "plugins" / "inro-agency-skills" / "skills"
DOWN = ROOT / "downloads"
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKIP = {".DS_Store", "__pycache__", "accounts", "evals", ".git"}
# Order and grouping of the skills in the README table.
GROUPS = [
    ("Set up a client", ["client-account-setup", "partner-client-onboarding", "instagram-ai-agent-setup"]),
    ("Audit and plan", ["instagram-account-audit", "dm-funnel-planner"]),
    ("Build", ["dm-flow-builder", "inbound-dm-playbook"]),
    ("Run and report", ["monthly-client-report", "multi-client-health-check", "partner-bulk-rollout"]),
    ("Content", ["client-post-scheduler", "short-form-content-principles"]),
]


def frontmatter(md):
    m = re.match(r"---\n(.*?)\n---\n", md.read_text(), re.S)
    if not m:
        sys.exit(f"{md}: no frontmatter")
    fm = {}
    for line in m.group(1).split("\n"):
        km = re.match(r"^([A-Za-z][\w-]*):\s?(.*)$", line)
        if km:
            fm[km.group(1)] = km.group(2).strip().strip("'\"")
    return fm


def first_sentence(text):
    return re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]


def main(src):
    src = pathlib.Path(src).resolve()
    skills = sorted(p.parent for p in src.glob("*/SKILL.md"))
    if not skills:
        sys.exit(f"no skills in {src}")
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    DOWN.mkdir(exist_ok=True)
    for old in DOWN.glob("*.zip"):
        old.unlink()
    info = {}
    for s in skills:
        fm = frontmatter(s / "SKILL.md")
        extra = set(fm) - ALLOWED
        if extra:
            sys.exit(f"{s.name}: frontmatter keys claude.ai rejects: {sorted(extra)}")
        if fm.get("name") != s.name:
            sys.exit(f"{s.name}: name in SKILL.md is {fm.get('name')!r}")
        shutil.copytree(s, DEST / s.name, ignore=shutil.ignore_patterns(*SKIP))
        info[s.name] = fm.get("description", "")
    every = zipfile.ZipFile(DOWN / "inro-agency-skills-all.zip", "w", zipfile.ZIP_DEFLATED)
    for name in sorted(info):
        with zipfile.ZipFile(DOWN / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted((DEST / name).rglob("*")):
                if f.is_file():
                    arc = f.relative_to(DEST)
                    z.write(f, arc)
                    every.write(f, arc)
    every.close()
    listed = [n for _, names in GROUPS for n in names]
    missing = sorted(set(info) - set(listed))
    rows = ["| Skill | What it does | Download for claude.ai |", "|---|---|---|"]
    for group, names in GROUPS + ([("Other", missing)] if missing else []):
        present = [n for n in names if n in info]
        if not present:
            continue
        rows.append(f"| **{group}** | | |")
        for n in present:
            rows.append(f"| [`{n}`](plugins/inro-agency-skills/skills/{n}/SKILL.md) | {first_sentence(info[n])} | [{n}.zip](downloads/{n}.zip) |")
    readme = ROOT / "README.md"
    text = readme.read_text()
    new, n = re.subn(r"(<!-- SKILLS:START -->\n).*?(<!-- SKILLS:END -->)", lambda m: m.group(1) + "\n".join(rows) + "\n" + m.group(2), text, flags=re.S)
    if n != 1:
        sys.exit("README.md: SKILLS markers not found")
    readme.write_text(new)
    print(f"{len(info)} skills copied, {len(info) + 1} zips written, README table updated")
    for n in sorted(set(listed) - set(info)):
        print("not in source:", n)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
