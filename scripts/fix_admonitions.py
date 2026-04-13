#!/usr/bin/env python3
"""Inject missing '!!! info' admonitions listing sibling topics.

Reads the chapter structure from existing files and injects the admonition
block after the H1 title and metadata blockquote, before the first H2.

Uses only Python stdlib. Runs in DRY-RUN mode by default.
"""

import argparse
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
FILENAME_PREFIX_RE = re.compile(r"^(\d{2})-(\d{2})-(.+)\.md$")


def parse_frontmatter_field(text: str, field: str) -> str:
    """Extract a single field value from frontmatter text."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return ""
    for line in match.group(1).splitlines():
        stripped = line.strip()
        colon_idx = stripped.find(":")
        if colon_idx == -1:
            continue
        key = stripped[:colon_idx].strip()
        if key == field:
            value = stripped[colon_idx + 1:].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            return value
    return ""


def get_h1_title(text: str) -> str:
    """Extract the first H1 title from content (after frontmatter)."""
    match = FRONTMATTER_RE.match(text)
    start = match.end() if match else 0
    for line in text[start:].splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            return stripped[2:].strip()
    return ""


def build_chapter_map(docs_path: Path) -> dict:
    """Build map: materia_dir -> chapter_num -> [(CC.TT, tema_display)]"""
    chapter_map = {}
    for materia_dir in sorted(docs_path.iterdir()):
        if not materia_dir.is_dir() or materia_dir.name.startswith("."):
            continue
        chapters = {}
        for md_file in sorted(materia_dir.glob("*.md")):
            if md_file.name == "index.md":
                continue
            prefix_match = FILENAME_PREFIX_RE.match(md_file.name)
            if not prefix_match:
                continue
            chap = prefix_match.group(1)
            tema = prefix_match.group(2)
            # Get display name from the file's H1 or title field
            text = md_file.read_text(encoding="utf-8")
            display = get_h1_title(text)
            if not display:
                title_field = parse_frontmatter_field(text, "title")
                # Extract tema part from standardized title
                parts = title_field.split(" - ")
                display = " - ".join(parts[3:]) if len(parts) >= 4 else title_field
            if not display:
                display = md_file.stem.replace("-", " ").title()

            ref = f"{chap}.{tema}"
            chapters.setdefault(chap, []).append((ref, display))

        chapter_map[materia_dir.name] = chapters
    return chapter_map


def build_admonition(siblings: list) -> str:
    """Build the admonition block text."""
    lines = ['!!! info "Temas do mesmo capítulo"']
    for ref, display in siblings:
        lines.append(f"    {ref} {display}")
    return "\n".join(lines)


def has_admonition(text: str) -> bool:
    """Check if the file already has the info admonition."""
    return '!!! info' in text


def inject_admonition(text: str, admonition: str) -> str:
    """Inject admonition after the metadata blockquote, before the first H2.
    
    Structure expected:
      ---frontmatter---
      # H1 Title
      > metadata blockquote (one or more lines)
      [blank line]
      !!! info   <-- inject here
      [blank line]
      ---
      [blank line]
      ## First H2
    """
    match = FRONTMATTER_RE.match(text)
    start = match.end() if match else 0
    content_after_fm = text[start:]

    # Find the end of the metadata blockquote block
    lines = content_after_fm.split("\n")
    insert_idx = None
    in_blockquote = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(">"):
            in_blockquote = True
        elif in_blockquote and not stripped.startswith(">"):
            # We're past the blockquote
            insert_idx = i
            break

    if insert_idx is None:
        # No blockquote found — insert before first H2
        for i, line in enumerate(lines):
            if line.strip().startswith("## "):
                insert_idx = i
                break

    if insert_idx is None:
        # Fallback: insert after H1
        for i, line in enumerate(lines):
            if line.strip().startswith("# "):
                insert_idx = i + 1
                break

    if insert_idx is None:
        return text  # Can't find insertion point

    # Insert admonition block
    new_lines = lines[:insert_idx] + ["", admonition, ""] + lines[insert_idx:]
    return text[:start] + "\n".join(new_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Injeta admonitions de temas irmãos nos resumos que não os têm."
    )
    parser.add_argument("--path", default="docs/", help="Caminho para docs/")
    parser.add_argument("--apply", action="store_true", help="Aplicar alterações")
    args = parser.parse_args()

    docs_path = Path(args.path)
    if not docs_path.is_dir():
        print(f"Erro: '{args.path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    is_dry_run = not args.apply
    if is_dry_run:
        print("═" * 60)
        print("  MODO DRY-RUN — nenhum arquivo será alterado")
        print("═" * 60)
        print()

    chapter_map = build_chapter_map(docs_path)

    files_changed = 0
    total_files = 0

    for materia_dir in sorted(docs_path.iterdir()):
        if not materia_dir.is_dir() or materia_dir.name.startswith("."):
            continue
        chapters = chapter_map.get(materia_dir.name, {})

        for md_file in sorted(materia_dir.glob("*.md")):
            if md_file.name == "index.md":
                continue

            prefix_match = FILENAME_PREFIX_RE.match(md_file.name)
            if not prefix_match:
                continue

            total_files += 1
            chap = prefix_match.group(1)
            text = md_file.read_text(encoding="utf-8")

            if has_admonition(text):
                continue

            siblings = chapters.get(chap, [])
            if not siblings:
                continue

            admonition = build_admonition(siblings)
            new_text = inject_admonition(text, admonition)

            if new_text == text:
                print(f"⚠ {md_file} — não foi possível encontrar ponto de inserção")
                continue

            files_changed += 1
            print(f"─── {md_file}")
            print(f"  + admonition com {len(siblings)} temas irmãos")

            if not is_dry_run:
                md_file.write_text(new_text, encoding="utf-8")
                print("  ✓ Arquivo atualizado")
            print()

    print("═" * 60)
    action = "alterados" if not is_dry_run else "a alterar"
    print(f"Total: {total_files} arquivos analisados")
    print(f"  {files_changed} arquivo(s) {action}")
    if is_dry_run and files_changed > 0:
        print(f"\n  Para aplicar: python3 scripts/fix_admonitions.py --apply")
    print("═" * 60)


if __name__ == "__main__":
    main()
