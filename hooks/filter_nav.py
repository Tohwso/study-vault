"""MkDocs hook: filtra disciplinas inativas do nav e do build.

Lê disciplines.yml na raiz do projeto e remove do nav (e exclui do
build) qualquer disciplina com status != 'ativo'.

Também reescreve a tabela de matérias no index.md em tempo de build,
para que apenas disciplinas ativas apareçam na Home.
"""

import logging
import os
import re
import yaml

log = logging.getLogger("mkdocs.hooks.filter_nav")

_inactive_dirs: set[str] = set()


def _load_config() -> dict:
    """Carrega disciplines.yml relativo ao diretório do mkdocs.yml."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "disciplines.yml")
    config_path = os.path.normpath(config_path)
    if not os.path.exists(config_path):
        log.warning("disciplines.yml não encontrado em %s", config_path)
        return {}
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def on_config(config):
    """Identifica disciplinas inativas e popula _inactive_dirs."""
    global _inactive_dirs
    data = _load_config()
    _inactive_dirs = set()

    for d in data.get("disciplinas", []):
        if d.get("status", "ativo") != "ativo":
            _inactive_dirs.add(d["dir"])
            log.info("Disciplina inativa: %s", d["dir"])

    if not _inactive_dirs:
        return config

    # Filtra o nav removendo seções de disciplinas inativas
    if config.get("nav"):
        config["nav"] = _filter_nav(config["nav"])

    return config


def _filter_nav(nav_items: list) -> list:
    """Remove itens do nav cujos paths começam com dirs inativos."""
    filtered = []
    for item in nav_items:
        if isinstance(item, dict):
            keep = True
            new_item = {}
            for key, value in item.items():
                if isinstance(value, str):
                    # Leaf: "Title: path/to/file.md"
                    if _is_inactive_path(value):
                        keep = False
                elif isinstance(value, list):
                    # Section: "Title: [children]"
                    children = _filter_nav(value)
                    if not children:
                        keep = False
                    else:
                        value = children
                new_item[key] = value
            if keep:
                filtered.append(new_item)
        elif isinstance(item, str):
            if not _is_inactive_path(item):
                filtered.append(item)
    return filtered


def _is_inactive_path(path: str) -> bool:
    """Verifica se um path pertence a uma disciplina inativa."""
    for d in _inactive_dirs:
        if path.startswith(d + "/") or path == d:
            return True
    return False


def on_files(files, config):
    """Remove arquivos de disciplinas inativas do build."""
    if not _inactive_dirs:
        return files

    files._files = [
        f for f in files._files
        if not _is_inactive_path(f.src_path)
    ]
    return files


def on_page_markdown(markdown, page, config, files):
    """Remove linhas de disciplinas inativas da tabela do index.md."""
    if page.file.src_path != "index.md" or not _inactive_dirs:
        return markdown

    lines = markdown.split("\n")
    filtered = []
    for line in lines:
        # Detecta linhas da tabela tipo "| [Disciplina](dir/index.md) |"
        skip = False
        for d in _inactive_dirs:
            if f"]({d}/" in line or f"]({d})" in line:
                skip = True
                break
        if not skip:
            filtered.append(line)

    return "\n".join(filtered)
