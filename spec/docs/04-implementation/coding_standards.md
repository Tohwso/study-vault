# Convenções de Código — Study Vault

> **Artefato RUP:** Coding Standards (Implementação)
> **Proprietário:** [RUP] Desenvolvedor
> **Status:** Complete
> **Última atualização:** 2026-07-21

---

## 1. Visão Geral

O Study Vault não é um sistema de software convencional — é um pipeline de conteúdo estático. O "código" do projeto resume-se a:

- **Scripts Python** (`scripts/`) — validação e normalização de conteúdo
- **Markdown** (`docs/`) — resumos publicáveis
- **YAML** (`mkdocs.yml`, frontmatter) — configuração e metadados
- **GitHub Actions workflow** (`.github/workflows/`) — CI/CD

As convenções abaixo refletem essa realidade.

---

## 2. Python (`scripts/`)

### 2.1 Estilo

- **PEP 8** como base, sem enforcement via linter (volume de código não justifica tooling)
- Indentação: 4 espaços
- Line length: 100 caracteres (soft limit)
- Strings: aspas duplas para strings de usuário, aspas simples são aceitáveis em regex/constantes
- Imports organizados: stdlib primeiro, depois locais (na prática, tudo é stdlib)

### 2.2 Dependências

- **APENAS stdlib Python** — `re`, `pathlib`, `argparse`, `sys`, `os`
- Nenhuma dependência externa. Isso é uma decisão de design (ADR-005), não economia
- Motivo: os scripts rodam ANTES do `pip install` no CI — dependência externa quebraria o fail-fast

### 2.3 Docstrings e Comentários

- Docstrings em **inglês** (convenção Python internacional)
- Module-level docstring obrigatória em todo script
- Function docstrings para funções com lógica não trivial
- Mensagens de output (print) em **português** (público-alvo é o Autor)
- Comentários inline apenas onde a lógica não é óbvia

### 2.4 Naming

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Arquivos | `snake_case.py` | `validate.py`, `backfill.py` |
| Funções | `snake_case` | `parse_frontmatter()`, `check_word_count()` |
| Classes | `PascalCase` | `Finding`, `Severity` |
| Constantes | `UPPER_SNAKE_CASE` | `REQUIRED_FIELDS`, `WORD_COUNT_MIN` |
| Variáveis locais | `snake_case` | `total_errors`, `fields` |

### 2.5 Tratamento de Erros

- Scripts nunca devem crashar com traceback em uso normal
- Erros de I/O (arquivo não encontrado, permissão) são capturados e reportados como finding
- Exit code 0 = sucesso (avisos são aceitáveis), 1 = falha (pelo menos um ERRO)

### 2.6 Output

- Formato de findings: `[ERRO] mensagem` ou `[AVISO] mensagem`
- Agrupamento por arquivo com separador visual (`───`)
- Resumo numérico no final com separador (`═══`)
- Sem cores ANSI (compatibilidade com CI logs que não suportam)

---

## 3. Markdown (`docs/`)

### 3.1 Estrutura de Arquivo

Todo resumo segue a estrutura canônica definida em `api_spec.md` seção 2.1:

```
frontmatter → H1 → blockquote metadata → HR → admonition → HR → seções → HR → rodapé
```

### 3.2 Headings

- `#` — apenas o título do tema (1 por arquivo)
- `##` — seções principais (Contexto, Desenvolvimento, Interpretações, Conexões, Top 5)
- `###` — subseções dentro de seções
- `####` — raramente usado, apenas para subsubseções densas

### 3.3 Formatação Inline

| Uso | Sintaxe | Quando |
|-----|---------|--------|
| Termos técnicos | `**negrito**` | Primeira menção de conceito importante |
| Nomes de autores | `**negrito**` | Sempre |
| Citações históricas | `> blockquote` | Documentos, tratados, discursos |
| Fórmulas LaTeX | `$$...$$` ou `$...$` | Economia, matemática |

### 3.4 Admonitions

| Tipo | Uso |
|------|-----|
| `!!! info` | Temas irmãos do capítulo (obrigatório) |
| `!!! note` | Observações complementares |
| `!!! warning` | Ressalvas importantes para a prova |
| `!!! tip` | Dicas de estudo |

---

## 4. YAML (frontmatter e mkdocs.yml)

### 4.1 Frontmatter

- Delimitado por `---` (abertura e fechamento)
- Campos flat (sem nesting) — decisão de design para viabilizar parse via regex
- Valores string com caracteres especiais: sempre entre aspas duplas
- Campo `title`: sempre entre aspas (contém hífens e acentos)
- Sem trailing spaces

### 4.2 mkdocs.yml

- Indentação: 2 espaços (padrão YAML)
- Seção `nav`: ordem espelha a do edital
- Sem comentários desnecessários (o YAML já é autodescritivo)

---

## 5. GitHub Actions Workflow

- Nomes de steps descritivos em inglês (padrão da plataforma)
- Actions pinadas por major version (`@v4`, `@v5`)
- Validação como primeiro step executável (fail-fast)
- `pip install` via `requirements.txt` (nunca inline sem versão)
- `--strict` no `mkdocs build` (warnings viram erros)

---

## 6. Naming de Arquivos e Diretórios

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Resumo | `CC-TT-slug-kebab-case.md` | `01-05-crise-de-1929-e-new-deal.md` |
| Diretório de matéria | `slug-kebab-case/` (sem acentos) | `historia-mundial/` |
| Índice de matéria | `index.md` | `docs/economia/index.md` |
| Script Python | `snake_case.py` | `validate.py` |
| Prompt template | `summary.md` ou `summary-<materia>.md` | `summary-economia.md` |
| Artefato spec | `kebab-case.md` | `coding_standards.md` |
