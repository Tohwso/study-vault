# Guia de Configuração — Study Vault

> **Artefato RUP:** Configuration Guide (Implementação)
> **Proprietário:** [RUP] Desenvolvedor
> **Status:** Complete
> **Última atualização:** 2026-07-21

---

## 1. mkdocs.yml — Configuração do Site

### 1.1 Localização

`/mkdocs.yml` (raiz do repositório)

### 1.2 Seções Principais

| Seção | Propósito | Frequência de alteração |
|-------|-----------|------------------------|
| `site_name`, `site_description`, `site_author` | Metadados do site | Raramente |
| `theme` | Tema Material (paleta, features, ícones) | Raramente |
| `plugins` | Busca em português | Nunca |
| `markdown_extensions` | Extensões habilitadas (admonition, MathJax, Mermaid, etc.) | Apenas ao habilitar nova extensão |
| `extra_javascript` | MathJax CDN | Nunca |
| `nav` | Hierarquia de navegação | **A cada novo resumo** |

### 1.3 Manutenção do `nav`

A cada novo resumo adicionado ao projeto, sua entrada deve ser incluída no `nav` seguindo:

1. Posição: dentro da matéria e capítulo corretos
2. Ordem: pela numeração `CC-TT` do edital
3. Formato: `<slug-materia>/<CC-TT-slug>.md` (path relativo a `docs/`)

Exemplo:
```yaml
- 2. Macroeconomia:
  - economia/02-01-contabilidade-nacional.md
  - economia/02-02-contas-externas.md  # ← novo resumo
```

### 1.4 Extensões Configuráveis

| Extensão | Parâmetro | Valor | Motivo |
|----------|-----------|-------|--------|
| `pymdownx.superfences` | `custom_fences.mermaid` | `fence_code_format` | Diagramas Mermaid |
| `pymdownx.tabbed` | `alternate_style` | `true` | Estilo de abas moderno |
| `pymdownx.highlight` | `anchor_linenums` | `true` | Links para linhas de código |
| `pymdownx.arithmatex` | `generic` | `true` | Compatibilidade MathJax 3 |
| `toc` | `permalink` | `true` | Links permanentes para seções |

---

## 2. Prompt Template — Configuração de Geração

### 2.1 Localização

- Template base: `scripts/prompts/summary.md`
- Variantes por matéria: `scripts/prompts/summary-<materia>.md` (quando necessário)

### 2.2 Variáveis

| Variável | Fonte | Obrigatória | Exemplo |
|----------|-------|-------------|---------|
| `{concurso}` | Constante do projeto | Sim | `CACD 2026` |
| `{materia}` | Nome da matéria | Sim | `História Mundial` |
| `{capitulo}` | Número + nome do capítulo | Sim | `1. Estruturas e Ideias Econômicas` |
| `{tema}` | Título do tema no edital | Sim | `1.5 Crise de 1929 e New Deal` |
| `{subtemas_irmaos}` | Demais temas do capítulo | Sim | `1.1 Rev. Industrial, 1.2 Fases...` |
| `{bibliografia}` | Bibliografia do edital | Sim | `HOBSBAWM, Eric. A Era dos Extremos...` |

### 2.3 Preenchimento

Atualmente manual — o Autor substitui as variáveis antes de submeter à LLM. O preenchimento automático via `data/<materia>.yml` é proposta futura (ADR-004).

---

## 3. Scripts de Automação — Configuração

### 3.1 `scripts/validate.py`

| Parâmetro | Default | Descrição |
|-----------|---------|-----------|
| `--path` | `docs/` | Diretório raiz dos resumos |
| `--verbose` | `false` | Exibir arquivo-a-arquivo (incluindo os sem erro) |

**Constantes configuráveis** (no código fonte):

| Constante | Valor | Descrição |
|-----------|-------|-----------|
| `REQUIRED_FIELDS` | 8 campos | Lista de campos obrigatórios no frontmatter |
| `VALID_STATUSES` | `completo, em_revisao, pendente` | Valores válidos para `status` |
| `WORD_COUNT_MIN` | `1500` | Contagem mínima de palavras |
| `WORD_COUNT_MAX` | `5000` | Contagem máxima de palavras |

> **Nota sobre word count**: a especificação (RF-22) define faixa de 2.000–4.000. O script usa 1.500–5.000 com margem intencional, pois: (a) a contagem `split()` inclui código LaTeX/markdown que infla artificialmente, e (b) resumos próximos do limite não devem bloquear o CI. A severidade é AVISO, não ERRO.

### 3.2 `scripts/backfill.py`

| Parâmetro | Default | Descrição |
|-----------|---------|-----------|
| `--path` | `docs/` | Diretório raiz dos resumos |
| `--apply` | `false` | Executa alterações (sem flag = dry-run) |

**Constantes de backfill** (no código fonte):

| Constante | Valor | Descrição |
|-----------|-------|-----------|
| `CONCURSO` | `CACD` | Valor padrão para campo `concurso` |
| `ANO` | `2026` | Ano do concurso |
| `BACKFILL_DATA_GERACAO` | `2026-04-01` | Data aproximada para resumos pré-existentes |
| `BACKFILL_MODELO_LLM` | `desconhecido` | Modelo desconhecido para resumos pré-existentes |
| `MATERIA_MAP` | 7 entradas | Mapeamento diretório → nome da matéria |

---

## 4. CI/CD — Configuração

### 4.1 Localização

`.github/workflows/deploy.yml`

### 4.2 Parâmetros

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| Python version | `3.12` | Versão estável usada localmente |
| `cache: pip` | habilitado | Economia de ~30s por build |
| `cancel-in-progress` | `true` | Evita builds redundantes em pushes rápidos |
| `--strict` no mkdocs build | habilitado | Warnings viram erros (links quebrados, nav inconsistente) |

### 4.3 Dependências

Gerenciadas via `requirements.txt`:

```
mkdocs-material==9.6.14
```

**Procedimento de atualização:**
1. `pip install --upgrade mkdocs-material`
2. Testar: `mkdocs build --strict && mkdocs serve`
3. Atualizar versão no `requirements.txt`
4. Commit + push

---

## 5. Ambiente Local

### 5.1 Setup Inicial

```bash
git clone <repo-url>
cd study-vault
pip install -r requirements.txt
```

### 5.2 Comandos do Dia a Dia

| Operação | Comando |
|----------|---------|
| Preview local | `mkdocs serve` |
| Build de teste | `mkdocs build --strict` |
| Validar resumos | `python3 scripts/validate.py` |
| Validar com detalhes | `python3 scripts/validate.py --verbose` |
| Backfill dry-run | `python3 scripts/backfill.py` |
| Backfill executar | `python3 scripts/backfill.py --apply` |

### 5.3 Pré-requisitos

- Python 3.12+
- Git 2.x+
- pip (qualquer versão recente)
- Sem Docker, sem Node.js, sem ferramentas adicionais
