#!/usr/bin/env python3
"""Validate Study Vault summaries for conformity against SDD specification.

Checks frontmatter fields, markdown structure, word count, and naming
conventions. Uses only Python stdlib (no pyyaml dependency).

Exit codes:
    0 — all checks passed (warnings may exist)
    1 — at least one ERROR found
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = [
    "title",
    "edital_ref",
    "capitulo",
    "status",
    "materia",
    "concurso",
    "data_geracao",
    "modelo_llm",
]

VALID_STATUSES = {"completo", "em_revisao", "pendente"}

# title format: "<ano> - <concurso> - <matéria> - <tema>"
TITLE_PATTERN = re.compile(r"^\d{4}\s*-\s*.+\s*-\s*.+\s*-\s*.+$")

FILENAME_PATTERN = re.compile(r"^\d{2}(-\d{2})?-.+\.md$")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

DATE_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

WORD_COUNT_MIN = 1500
WORD_COUNT_MAX = 5000

# ---------------------------------------------------------------------------
# Severity helpers
# ---------------------------------------------------------------------------

class Severity:
    ERROR = "ERRO"
    WARNING = "AVISO"


class Finding:
    """A single validation finding."""

    __slots__ = ("file", "severity", "message")

    def __init__(self, file: str, severity: str, message: str):
        self.file = file
        self.severity = severity
        self.message = message

    def __str__(self):
        return f"  [{self.severity}] {self.message}"


# ---------------------------------------------------------------------------
# Frontmatter parser (regex-based, no pyyaml)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str):
    """Parse YAML frontmatter from markdown text.

    Returns (dict, error_message). If parsing fails, dict is None.
    Only handles flat key: value pairs (no nesting) which is sufficient
    for Study Vault frontmatter.
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "Frontmatter YAML ausente ou mal delimitado (esperado --- no início)"

    raw = match.group(1)
    fields = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        colon_idx = line.find(":")
        if colon_idx == -1:
            continue
        key = line[:colon_idx].strip()
        value = line[colon_idx + 1:].strip()
        # Strip surrounding quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        fields[key] = value

    return fields, None


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_frontmatter(filepath: str, text: str, fields: dict) -> list:
    """Check frontmatter fields for completeness and validity."""
    findings = []

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in fields or not fields[field]:
            findings.append(Finding(filepath, Severity.ERROR,
                f"Campo obrigatório ausente no frontmatter: '{field}'"))

    # status value
    status_val = fields.get("status", "")
    if status_val and status_val not in VALID_STATUSES:
        findings.append(Finding(filepath, Severity.ERROR,
            f"Campo 'status' com valor inválido: '{status_val}' "
            f"(esperado: {', '.join(sorted(VALID_STATUSES))})"))

    # title format
    title_val = fields.get("title", "")
    if title_val and not TITLE_PATTERN.match(title_val):
        findings.append(Finding(filepath, Severity.ERROR,
            f"Campo 'title' não segue formato '<ano> - <concurso> - <matéria> - <tema>': "
            f"'{title_val}'"))

    # data_geracao format
    data_val = fields.get("data_geracao", "")
    if data_val and not DATE_ISO_RE.match(data_val):
        findings.append(Finding(filepath, Severity.WARNING,
            f"Campo 'data_geracao' não é ISO 8601 (YYYY-MM-DD): '{data_val}'"))

    return findings


def check_structure(filepath: str, text: str) -> list:
    """Check for required markdown structural elements."""
    findings = []
    lines = text.split("\n")

    # Metadata blockquote (line starting with > after H1)
    has_blockquote = False
    past_frontmatter = False
    past_h1 = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            past_frontmatter = True
            continue
        if past_frontmatter and stripped.startswith("# ") and not stripped.startswith("## "):
            past_h1 = True
            continue
        if past_h1 and stripped.startswith(">"):
            has_blockquote = True
            break

    if not has_blockquote:
        findings.append(Finding(filepath, Severity.ERROR,
            "Metadata blockquote ausente (linhas com '>' após H1)"))

    # Admonition temas irmãos
    if not any(line.strip().startswith('!!! info') for line in lines):
        findings.append(Finding(filepath, Severity.ERROR,
            "Admonition de temas irmãos ausente ('!!! info')"))

    # Required final sections: Conexões + Top 5
    has_conexoes = False
    has_top5 = False
    for line in lines:
        stripped = line.strip()
        if re.match(r"^##\s+.*[Cc]onex", stripped):
            has_conexoes = True
        if re.match(r"^##\s+.*[Tt]op\s*5", stripped):
            has_top5 = True

    if not has_conexoes:
        findings.append(Finding(filepath, Severity.ERROR,
            "Seção obrigatória ausente: 'Conexões com Outros Temas'"))

    if not has_top5:
        findings.append(Finding(filepath, Severity.ERROR,
            "Seção obrigatória ausente: 'Top 5'"))

    return findings


def check_word_count(filepath: str, text: str) -> list:
    """Check word count is within acceptable range."""
    findings = []

    # Strip frontmatter for counting
    body = FRONTMATTER_RE.sub("", text, count=1)
    words = len(body.split())

    if words < WORD_COUNT_MIN:
        findings.append(Finding(filepath, Severity.WARNING,
            f"Contagem de palavras abaixo do mínimo: {words} "
            f"(esperado >= {WORD_COUNT_MIN})"))
    elif words > WORD_COUNT_MAX:
        findings.append(Finding(filepath, Severity.WARNING,
            f"Contagem de palavras acima do máximo: {words} "
            f"(esperado <= {WORD_COUNT_MAX})"))

    return findings


def check_footer(filepath: str, text: str) -> list:
    """Check for AI disclaimer footer."""
    findings = []

    if not re.search(r"^\*Gerado por IA", text, re.MULTILINE):
        findings.append(Finding(filepath, Severity.WARNING,
            "Rodapé com disclaimer de IA ausente ('*Gerado por IA...')"))

    return findings


def check_filename(filepath: str) -> list:
    """Check filename follows CC-TT-slug.md or NN-slug.md convention."""
    findings = []
    name = Path(filepath).name

    if not FILENAME_PATTERN.match(name):
        findings.append(Finding(filepath, Severity.ERROR,
            f"Nome de arquivo não segue formato CC-TT-slug.md ou NN-slug.md: '{name}'"))

    return findings


# ---------------------------------------------------------------------------
# Main validation logic
# ---------------------------------------------------------------------------

def get_materia_dirs(docs_path: Path) -> list:
    """Return list of materia directories (directories inside docs/ that are
    not special directories like 'javascripts')."""
    skip = {"javascripts", "stylesheets", "assets", "images"}
    dirs = []
    for entry in sorted(docs_path.iterdir()):
        if entry.is_dir() and entry.name not in skip and not entry.name.startswith("."):
            dirs.append(entry)
    return dirs


def collect_files(docs_path: Path) -> list:
    """Collect all summary markdown files to validate."""
    files = []
    for materia_dir in get_materia_dirs(docs_path):
        for md_file in sorted(materia_dir.glob("*.md")):
            # Skip index files
            if md_file.name == "index.md":
                continue
            files.append(md_file)
    return files


def validate_file(filepath: Path, verbose: bool = False) -> list:
    """Run all checks on a single file. Returns list of Findings."""
    rel_path = str(filepath)
    findings = []

    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        findings.append(Finding(rel_path, Severity.ERROR,
            f"Não foi possível ler o arquivo: {e}"))
        return findings

    # Filename check
    findings.extend(check_filename(rel_path))

    # Frontmatter parse
    fields, parse_error = parse_frontmatter(text)
    if parse_error:
        findings.append(Finding(rel_path, Severity.ERROR, parse_error))
        # Can still check structure even without frontmatter
    else:
        findings.extend(check_frontmatter(rel_path, text, fields))

    # Structural checks
    findings.extend(check_structure(rel_path, text))

    # Word count
    findings.extend(check_word_count(rel_path, text))

    # Footer
    findings.extend(check_footer(rel_path, text))

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Valida conformidade dos resumos do Study Vault contra a especificação SDD."
    )
    parser.add_argument(
        "--path", default="docs/",
        help="Caminho para o diretório docs/ (default: docs/)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Exibir detalhes de cada arquivo validado"
    )
    args = parser.parse_args()

    docs_path = Path(args.path)
    if not docs_path.is_dir():
        print(f"Erro: diretório '{args.path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    files = collect_files(docs_path)
    if not files:
        print(f"Nenhum arquivo de resumo encontrado em '{args.path}'.")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0
    files_with_errors = 0
    files_with_warnings = 0
    all_findings = {}

    for filepath in files:
        findings = validate_file(filepath, args.verbose)
        if findings:
            all_findings[str(filepath)] = findings
            file_errors = sum(1 for f in findings if f.severity == Severity.ERROR)
            file_warnings = sum(1 for f in findings if f.severity == Severity.WARNING)
            total_errors += file_errors
            total_warnings += file_warnings
            if file_errors > 0:
                files_with_errors += 1
            if file_warnings > 0:
                files_with_warnings += 1
        elif args.verbose:
            print(f"✓ {filepath}")

    # Output findings grouped by file
    if all_findings:
        print()
        for filepath, findings in all_findings.items():
            print(f"─── {filepath}")
            for finding in findings:
                print(str(finding))
            print()

    # Summary
    print("═" * 60)
    print(f"Validação concluída: {len(files)} arquivos analisados")
    print(f"  {total_errors} erro(s) em {files_with_errors} arquivo(s)")
    print(f"  {total_warnings} aviso(s) em {files_with_warnings} arquivo(s)")
    print(f"  {len(files) - files_with_errors} arquivo(s) sem erros")
    print("═" * 60)

    if total_errors > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
