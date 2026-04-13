#!/usr/bin/env python3
"""Backfill missing frontmatter fields and footer in existing Study Vault summaries.

Normalizes the 84 existing summaries to match the SDD specification:
- Adds missing fields: materia, concurso, data_geracao, modelo_llm
- Standardizes title format to "<ano> - <concurso> - <matéria> - <tema>"
- Adds/updates AI disclaimer footer

Runs in DRY-RUN mode by default. Use --apply to write changes.
Uses only Python stdlib (no pyyaml dependency).

SAFETY: Preserves all content between frontmatter and footer. Does NOT
modify LaTeX formulas, admonitions, or body text.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

# Map directory name to materia display name
MATERIA_MAP = {
    "historia-mundial": "História Mundial",
    "economia": "Economia",
    "historia-do-brasil": "História do Brasil",
    "portugues": "Português",
    "geografia": "Geografia",
    "politica-internacional": "Política Internacional",
    "direito": "Direito",
}

CONCURSO = "CACD"
ANO = "2026"
BACKFILL_DATA_GERACAO = "2026-04-01"
BACKFILL_MODELO_LLM = "desconhecido"

# Map (materia_dir, chapter_number) to chapter display name
CAPITULO_MAP = {
    "historia-mundial": {
        "1": "1. Estruturas e Ideias Econômicas",
        "2": "2. Revoluções",
        "3": "3. Relações Internacionais",
        "4": "4. Colonialismo e Imperialismo",
        "5": "5. As Américas",
        "6": "6. Ideias Políticas",
        "7": "7. A Vida Cultural",
        "8": "8. Relações Internacionais no Século XXI",
    },
    "economia": {
        "1": "1. Microeconomia",
        "2": "2. Macroeconomia",
        "3": "3. Economia Internacional",
        "4": "4. História Econômica Brasileira",
        "5": "5. Temas Contemporâneos",
    },
}

# Regex to extract CC-TT prefix from filename (e.g. "03-17-slug.md" → ("03","17"))
FILENAME_PREFIX_RE = re.compile(r"^(\d{2})-(\d{2})-")

FOOTER_PATTERN = re.compile(r"^\*Gerado por IA.*$", re.MULTILINE)
EXPECTED_FOOTER = "*Gerado por IA (desconhecido). Sujeito a revisão.*"


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str):
    """Parse flat YAML frontmatter. Returns (dict, raw_block, match_object)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, None, None

    raw = match.group(1)
    fields = {}
    field_order = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        colon_idx = stripped.find(":")
        if colon_idx == -1:
            continue
        key = stripped[:colon_idx].strip()
        value = stripped[colon_idx + 1:].strip()
        # Strip surrounding quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        fields[key] = value
        field_order.append(key)

    return fields, field_order, match


def serialize_frontmatter(fields: dict, field_order: list) -> str:
    """Serialize frontmatter dict back to YAML string."""
    lines = ["---"]
    # Emit fields in order, then any new fields not in original order
    emitted = set()
    for key in field_order:
        if key in fields:
            lines.append(format_field(key, fields[key]))
            emitted.add(key)

    for key in fields:
        if key not in emitted:
            lines.append(format_field(key, fields[key]))

    lines.append("---")
    return "\n".join(lines)


def format_field(key: str, value: str) -> str:
    """Format a single frontmatter field line."""
    # Always quote title (it contains special chars)
    if key == "title":
        return f'{key}: "{value}"'
    # Quote values that contain colons, special chars, or start with quotes
    if ":" in value or value.startswith('"') or value.startswith("'"):
        return f'{key}: "{value}"'
    return f"{key}: {value}"


def extract_tema_from_title(title: str) -> str:
    """Try to extract the tema portion from an existing title.

    For already-formatted titles like "2026 - CACD - ... - Tema",
    returns the last segment. For descriptive titles like
    "Demanda do Consumidor: Preferências...", returns the part before
    the colon (or the full title if no colon).
    Strips leading numeric prefixes like "6.4 " from the tema.
    """
    # Already in standard format?
    parts = title.split(" - ")
    if len(parts) >= 4:
        return " - ".join(parts[3:])

    # Descriptive title — take part before colon if exists
    if ":" in title:
        tema = title.split(":")[0].strip()
    else:
        tema = title

    # Strip leading numeric prefix like "6.4 " or "3.17 "
    tema = re.sub(r"^\d+\.\d+\s+", "", tema)
    return tema


# ---------------------------------------------------------------------------
# Backfill logic
# ---------------------------------------------------------------------------

def compute_changes(filepath: Path, text: str) -> tuple:
    """Compute needed changes for a file. Returns (new_text, changes_list).

    changes_list is a list of human-readable change descriptions.
    If no changes needed, returns (None, []).
    """
    changes = []

    fields, field_order, fm_match = parse_frontmatter(text)
    if fields is None:
        return None, ["Frontmatter ausente — não é possível fazer backfill"]

    # Detect materia from directory
    materia_dir = filepath.parent.name
    materia_name = MATERIA_MAP.get(materia_dir, materia_dir.replace("-", " ").title())

    original_fields = dict(fields)
    modified = False

    # Normalize legacy field names (accented → unaccented)
    legacy_renames = {
        "título": "title",
        "capítulo": "capitulo",
        "subcapítulo": "edital_ref",
        "última_revisão": None,  # drop — replaced by data_geracao
        "disciplina": None,       # drop — replaced by materia
    }
    for old_key, new_key in legacy_renames.items():
        if old_key in fields:
            if new_key and new_key not in fields:
                fields[new_key] = fields[old_key]
                changes.append(f"~ {old_key} → {new_key}: {fields[new_key]}")
            del fields[old_key]
            if old_key in field_order:
                if new_key:
                    idx = field_order.index(old_key)
                    field_order[idx] = new_key
                else:
                    field_order.remove(old_key)
            modified = True

    # Add missing fields
    if "materia" not in fields:
        fields["materia"] = materia_name
        changes.append(f"+ materia: {materia_name}")
        modified = True

    if "concurso" not in fields:
        fields["concurso"] = CONCURSO
        changes.append(f"+ concurso: {CONCURSO}")
        modified = True

    if "data_geracao" not in fields:
        fields["data_geracao"] = BACKFILL_DATA_GERACAO
        changes.append(f"+ data_geracao: {BACKFILL_DATA_GERACAO}")
        modified = True

    if "modelo_llm" not in fields:
        fields["modelo_llm"] = BACKFILL_MODELO_LLM
        changes.append(f"+ modelo_llm: {BACKFILL_MODELO_LLM}")
        modified = True

    # Infer capitulo and edital_ref from filename prefix (CC-TT)
    prefix_match = FILENAME_PREFIX_RE.match(filepath.name)
    if prefix_match:
        chap_num = prefix_match.group(1).lstrip("0") or "0"
        tema_num = prefix_match.group(2).lstrip("0") or "0"
        edital_ref_val = f"{chap_num}.{tema_num}"

        if "edital_ref" not in fields:
            fields["edital_ref"] = edital_ref_val
            changes.append(f"+ edital_ref: {edital_ref_val}")
            modified = True

        if "capitulo" not in fields:
            chap_names = CAPITULO_MAP.get(materia_dir, {})
            chap_name = chap_names.get(chap_num, f"{chap_num}. (capítulo desconhecido)")
            fields["capitulo"] = chap_name
            changes.append(f"+ capitulo: {chap_name}")
            modified = True

    # Standardize title format
    title_val = fields.get("title", "")
    title_re = re.compile(r"^\d{4}\s*-\s*.+\s*-\s*.+\s*-\s*.+$")
    if title_val and not title_re.match(title_val):
        tema = extract_tema_from_title(title_val)
        new_title = f"{ANO} - {CONCURSO} - {materia_name} - {tema}"
        fields["title"] = new_title
        changes.append(f"~ title: \"{title_val}\" → \"{new_title}\"")
        modified = True

    # Rebuild text if frontmatter changed
    if modified:
        new_fm = serialize_frontmatter(fields, field_order)
        new_text = new_fm + text[fm_match.end():]
    else:
        new_text = text

    # Footer check
    if not FOOTER_PATTERN.search(new_text):
        # Add footer at the end
        new_text = new_text.rstrip() + "\n\n---\n\n" + EXPECTED_FOOTER + "\n"
        changes.append(f"+ rodapé: {EXPECTED_FOOTER}")

    if not changes:
        return None, []

    return new_text, changes


def collect_files(docs_path: Path) -> list:
    """Collect all summary markdown files."""
    skip_dirs = {"javascripts", "stylesheets", "assets", "images"}
    files = []
    for materia_dir in sorted(docs_path.iterdir()):
        if not materia_dir.is_dir() or materia_dir.name in skip_dirs:
            continue
        if materia_dir.name.startswith("."):
            continue
        for md_file in sorted(materia_dir.glob("*.md")):
            if md_file.name == "index.md":
                continue
            files.append(md_file)
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Normaliza frontmatter e rodapé dos resumos existentes do Study Vault."
    )
    parser.add_argument(
        "--path", default="docs/",
        help="Caminho para o diretório docs/ (default: docs/)"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Aplicar as alterações (sem essa flag, roda em modo dry-run)"
    )
    args = parser.parse_args()

    docs_path = Path(args.path)
    if not docs_path.is_dir():
        print(f"Erro: diretório '{args.path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    is_dry_run = not args.apply

    if is_dry_run:
        print("═" * 60)
        print("  MODO DRY-RUN — nenhum arquivo será alterado")
        print("  Use --apply para executar as alterações")
        print("═" * 60)
        print()

    files = collect_files(docs_path)
    if not files:
        print("Nenhum arquivo de resumo encontrado.")
        sys.exit(0)

    total_files = len(files)
    files_changed = 0
    total_changes = 0

    for filepath in files:
        try:
            text = filepath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"⚠ Não foi possível ler {filepath}: {e}")
            continue

        new_text, changes = compute_changes(filepath, text)
        if not changes:
            continue

        files_changed += 1
        total_changes += len(changes)

        print(f"─── {filepath}")
        for change in changes:
            print(f"  {change}")

        if not is_dry_run:
            try:
                filepath.write_text(new_text, encoding="utf-8")
                print("  ✓ Arquivo atualizado")
            except Exception as e:
                print(f"  ✗ Erro ao escrever: {e}")

        print()

    # Summary
    print("═" * 60)
    action = "alterados" if not is_dry_run else "a alterar"
    print(f"Total: {total_files} arquivos analisados")
    print(f"  {files_changed} arquivo(s) {action}")
    print(f"  {total_changes} alteração(ões) total")
    if is_dry_run and files_changed > 0:
        print()
        print("  Para aplicar: python3 scripts/backfill.py --apply")
    print("═" * 60)


if __name__ == "__main__":
    main()
