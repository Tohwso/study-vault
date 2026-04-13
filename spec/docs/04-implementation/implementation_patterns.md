# Padrões de Implementação — Study Vault

> **Artefato RUP:** Implementation Patterns (Implementação)
> **Proprietário:** [RUP] Desenvolvedor
> **Status:** Complete
> **Última atualização:** 2026-07-21

---

## 1. Visão Geral

Este documento cataloga os padrões recorrentes aplicados na implementação do Study Vault. Cada padrão inclui: onde é usado, como funciona, e um exemplo de código.

---

## 2. Frontmatter Parsing via Regex (sem PyYAML)

### Onde

`scripts/validate.py`, `scripts/backfill.py`

### Motivação

O frontmatter do Study Vault é **flat** (sem aninhamento, sem listas, sem multi-line values). Usar PyYAML adicionaria uma dependência externa que quebraria o princípio de fail-fast no CI (validação roda antes do `pip install`). ADR-005 documenta essa decisão.

### Como funciona

1. Regex extrai o bloco entre `---` delimitadores:
   ```python
   FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
   ```
2. Cada linha é parseada como `key: value` via `str.find(":")`:
   - Aspas circundantes (simples ou duplas) são removidas
   - Linhas vazias e comentários (`#`) são ignoradas
3. Resultado é um `dict[str, str]` — todos os valores são strings

### Limitações

- Não suporta YAML aninhado (dicts dentro de dicts)
- Não suporta listas YAML (`- item`)
- Não suporta multi-line strings (pipe `|` ou fold `>`)
- Valores com `:` no meio são parseados corretamente (split no primeiro `:`)

### Risco

Se o frontmatter do projeto evoluir para incluir campos aninhados (ex: `tags: [tag1, tag2]`), o parser regex quebrará. Nesse cenário, migrar para PyYAML e ajustar a ordem dos steps no CI (instalar pip antes de validar). AS-11 documenta essa premissa.

---

## 3. Validação por Severidade (ERRO vs. AVISO)

### Onde

`scripts/validate.py`

### Motivação

Nem toda violação deve bloquear o pipeline. Erros estruturais (frontmatter ausente, seções faltando) indicam problemas graves. Word count fora da faixa ou rodapé ausente são desejáveis mas não impeditivos.

### Como funciona

```python
class Severity:
    ERROR = "ERRO"
    WARNING = "AVISO"
```

- **ERRO**: incrementa `total_errors`, resulta em `sys.exit(1)` se > 0
- **AVISO**: reportado no output mas não afeta exit code

### Mapeamento

| Verificação | Severidade | Bloqueia CI? |
|-------------|------------|--------------|
| Frontmatter ausente/inválido | ERRO | Sim |
| Campos obrigatórios faltando | ERRO | Sim |
| Título fora do formato | ERRO | Sim |
| Status inválido | ERRO | Sim |
| Seções Conexões/Top 5 ausentes | ERRO | Sim |
| Metadata blockquote ausente | ERRO | Sim |
| Admonition ausente | ERRO | Sim |
| Word count fora da faixa | AVISO | Não |
| data_geracao formato inválido | AVISO | Não |
| Rodapé ausente | AVISO | Não |

### Rastreabilidade

O mapeamento segue a tabela em `ci_cd_pipeline.md` seção 3.1 e `architecture.md` seção 5.1.

---

## 4. Backfill Safe Mode (Dry-Run por Default)

### Onde

`scripts/backfill.py`

### Motivação

O backfill modifica 80+ arquivos. Modificações em massa de conteúdo existente têm alto risco de corrupção (especialmente com fórmulas LaTeX e admonitions). Dry-run por default é uma guardrail contra execução acidental.

### Como funciona

1. **Separação compute/write**: `compute_changes()` calcula o novo conteúdo e a lista de mudanças sem tocar no disco
2. **Dry-run** (default): apenas imprime o diff semântico (quais campos adicionados, como o título mudaria)
3. **--apply**: efetivamente escreve os arquivos

### Garantias de segurança

- O script **nunca** modifica o corpo do markdown (entre frontmatter e rodapé)
- O frontmatter é reconstruído preservando a **ordem original** dos campos
- Novos campos são adicionados **após** os campos existentes
- O rodapé é adicionado apenas se ausente, **sempre ao final** do arquivo
- Fórmulas LaTeX (`$$...$$`) e admonitions (`!!!`) não são tocados

### Extração de tema do título

Para padronizar o título de economia de `"Demanda do Consumidor: Preferências..."` para `"2026 - CACD - Economia - Demanda do Consumidor"`, o script usa heurística:

```python
def extract_tema_from_title(title: str) -> str:
    # Já no formato padrão? Pega o último segmento
    parts = title.split(" - ")
    if len(parts) >= 4:
        return " - ".join(parts[3:])
    # Título descritivo — parte antes do ':'
    if ":" in title:
        return title.split(":")[0].strip()
    return title
```

---

## 5. Mapeamento Diretório → Matéria

### Onde

`scripts/backfill.py`

### Motivação

O campo `materia` no frontmatter deve conter o nome por extenso com acentos (`"História Mundial"`), mas o diretório usa slug kebab-case sem acentos (`historia-mundial/`). O mapeamento é necessário para o backfill e potencialmente para validação futura.

### Como funciona

```python
MATERIA_MAP = {
    "historia-mundial": "História Mundial",
    "economia": "Economia",
    "historia-do-brasil": "História do Brasil",
    "portugues": "Português",
    "geografia": "Geografia",
    "politica-internacional": "Política Internacional",
    "direito": "Direito",
}
```

Fallback para diretórios não mapeados: `slug.replace("-", " ").title()`.

### Extensibilidade

Ao adicionar nova matéria, incluir entrada no `MATERIA_MAP`. Se não incluir, o fallback gera um nome razoável (ex: `historia-do-brasil` → `Historia Do Brasil`), mas sem acentos corretos.

---

## 6. Coleta de Arquivos com Exclusão de Especiais

### Onde

`scripts/validate.py`, `scripts/backfill.py`

### Motivação

O diretório `docs/` contém subdiretórios que não são matérias: `javascripts/`, `stylesheets/`, etc. Além disso, `index.md` de cada matéria não é um resumo — é o dashboard de progresso.

### Como funciona

```python
def collect_files(docs_path: Path) -> list:
    skip_dirs = {"javascripts", "stylesheets", "assets", "images"}
    for materia_dir in sorted(docs_path.iterdir()):
        if materia_dir.name in skip_dirs or materia_dir.name.startswith("."):
            continue
        for md_file in sorted(materia_dir.glob("*.md")):
            if md_file.name == "index.md":
                continue
            # ...
```

### Decisão: UQ-008

A questão "validate.py deve tratar index.md diferentemente?" (UQ-008) foi resolvida na implementação: `index.md` é simplesmente ignorado pela coleta de arquivos, pois não é um resumo e não segue o schema de frontmatter dos resumos.

---

## 7. Detecção de Seções via Regex Flexível

### Onde

`scripts/validate.py`

### Motivação

A especificação permite flexibilidade nas seções internas para matérias analíticas (RF-10), mas exige "Conexões" e "Top 5" como invariantes. A detecção precisa ser flexível o suficiente para aceitar variações como `## Conexões com Outros Temas do Edital` e `## 🎯 Top 5 — O que mais cai no CACD`.

### Como funciona

```python
# Match variações de "Conexões"
if re.match(r"^##\s+.*[Cc]onex", stripped):
    has_conexoes = True

# Match variações de "Top 5"
if re.match(r"^##\s+.*[Tt]op\s*5", stripped):
    has_top5 = True
```

A regex busca H2 (`##`) seguido de qualquer texto que contenha "Conex" ou "Top 5", case-insensitive parcial. Isso acomoda:
- `## Conexões com Outros Temas do Edital`
- `## Conexões com Outros Temas`
- `## 🎯 Top 5 — O que mais cai no CACD`
- `## Top 5 — O que mais cai no CACD sobre Política Monetária`
