# Especificação de Contratos — Study Vault

> **Artefato RUP:** Especificação de Contratos (Análise & Design)
> **Proprietário:** [RUP] Arquiteto
> **Status:** Complete
> **Última atualização:** 2026-07-19
>
> ⚠️ Este artefato substitui o tradicional "API Spec". No Study Vault não há APIs REST — os contratos são: formato do frontmatter YAML, estrutura do markdown, prompt template como contrato de geração, e geração automática do nav.

---

## 1. Schema do Frontmatter YAML

O frontmatter é o **contrato máquina-máquina** de cada resumo. Ele fica no topo do arquivo markdown, delimitado por `---`.

### 1.1 Campos Obrigatórios

| Campo | Tipo | Formato | Exemplo | RF |
|-------|------|---------|---------|-----|
| `title` | string | `"<ano> - <concurso> - <matéria> - <tema>"` | `"2026 - CACD - História Mundial - Crise de 1929 e New Deal"` | RF-03 |
| `edital_ref` | string | Número do edital (livre) | `"1.5"` | RF-02 |
| `capitulo` | string | `"<N>. <Nome do capítulo>"` | `"1. Estruturas e Ideias Econômicas"` | RF-02 |
| `materia` | string | Nome por extenso da matéria | `"História Mundial"` | RF-02 |
| `concurso` | string | Sigla do concurso | `"CACD"` | RF-02 |
| `status` | enum | `completo` \| `em_revisao` \| `pendente` | `"completo"` | RF-04 |
| `data_geracao` | date | ISO 8601 (`YYYY-MM-DD`) | `"2026-04-01"` | RF-05 |
| `modelo_llm` | string | Identificador do modelo LLM | `"gpt-4o"` | RF-06 |

### 1.2 Regras de Validação

| Regra | Descrição | Severidade |
|-------|-----------|------------|
| FRONT-01 | Bloco `---` delimitado corretamente (abertura e fechamento) | ERRO |
| FRONT-02 | YAML parseável (sem erros de sintaxe) | ERRO |
| FRONT-03 | Todos os 8 campos obrigatórios presentes | ERRO |
| FRONT-04 | `title` segue o formato `"<ano> - <concurso> - <matéria> - <tema>"` | ERRO |
| FRONT-05 | `status` é um dos 3 valores válidos | ERRO |
| FRONT-06 | `data_geracao` é data válida no formato YYYY-MM-DD | AVISO |
| FRONT-07 | `modelo_llm` não está vazio | AVISO |
| FRONT-08 | `materia` e `concurso` são consistentes com o diretório pai e o `mkdocs.yml` | AVISO |

### 1.3 Exemplo Completo — História Mundial

```yaml
---
title: "2026 - CACD - História Mundial - As crises e os mecanismos anticrise: a Crise de 1929 e o New Deal"
edital_ref: "1.5"
capitulo: "1. Estruturas e Ideias Econômicas"
materia: "História Mundial"
concurso: "CACD"
status: completo
data_geracao: "2026-04-01"
modelo_llm: "gpt-4o"
---
```

### 1.4 Exemplo Completo — Economia (pós-padronização)

```yaml
---
title: "2026 - CACD - Economia - Demanda do Consumidor"
edital_ref: "1.1"
capitulo: "1. Microeconomia"
materia: "Economia"
concurso: "CACD"
status: completo
data_geracao: "2026-04-01"
modelo_llm: "desconhecido"
---
```

### 1.5 Estado Atual vs. Estado Desejado (Delta de Backfill)

| Aspecto | HM (60 resumos) | Economia (24 resumos) | Ação |
|---------|------------------|-----------------------|------|
| `title` | ✅ Formato padronizado | ❌ Descritivo sem prefixo | RF-38: migrar |
| `edital_ref` | ✅ Presente | ✅ Presente | — |
| `capitulo` | ✅ Presente | ✅ Presente | — |
| `materia` | ❌ Ausente | ❌ Ausente | RF-02: adicionar |
| `concurso` | ❌ Ausente | ❌ Ausente | RF-02: adicionar |
| `status` | ✅ Presente | ✅ Presente | — |
| `data_geracao` | ❌ Ausente | ❌ Ausente | RF-40: adicionar |
| `modelo_llm` | ❌ Ausente | ❌ Ausente | RF-40: adicionar |

---

## 2. Estrutura do Conteúdo Markdown

O corpo do arquivo segue uma estrutura rígida. A ordem dos elementos é invariante.

### 2.1 Estrutura Canônica

```markdown
---
(frontmatter YAML — ver Seção 1)
---

# <Título do tema>

> **Concurso:** <concurso> <ano> — <nome completo do concurso>
> **Matéria:** <matéria>
> **Capítulo:** <capítulo>
> **Referência no edital:** <edital_ref>
> **Status:** ✅ Completo | ⏳ Em revisão | 📝 Pendente

---

!!! info "Temas do mesmo capítulo"
    CC.TT <Tema 1>
    CC.TT <Tema 2> *(este resumo)*
    CC.TT <Tema 3>
    ...

---

## Contexto e Periodização
(conteúdo)

## Desenvolvimento
(conteúdo)

## Interpretações e Debates
(conteúdo)

## Conexões com Outros Temas do Edital
(conteúdo)

## 🎯 Top 5 — O que mais cai no <concurso>
(disclaimer + lista)

---

*Gerado por IA ({modelo_llm}). Sujeito a revisão.*
```

### 2.2 Elementos Obrigatórios

| # | Elemento | Regex/Padrão de Detecção | RF |
|---|----------|--------------------------|-----|
| 1 | Frontmatter YAML | `^---\n.*\n---` (multiline) | RF-02 |
| 2 | Título H1 | `^# .+` | — |
| 3 | Metadata blockquote | `^> \*\*Concurso:\*\*` | RF-07 |
| 4 | Admonition temas irmãos | `^!!! info` | RF-08 |
| 5 | Seção "Contexto e Periodização" | `^## Contexto` | RF-09 |
| 6 | Seção "Desenvolvimento" | `^## Desenvolvimento` | RF-09 |
| 7 | Seção "Interpretações e Debates" | `^## Interpretações` | RF-09 |
| 8 | Seção "Conexões" | `^## Conexões` | RF-09 |
| 9 | Seção "Top 5" | `^## .*Top 5` | RF-09 |
| 10 | Rodapé disclaimer | `^\*Gerado por IA` | RF-11 |

### 2.3 Flexibilidade para Matérias Analíticas (RF-10)

Para matérias como Economia e Direito, as seções **Contexto**, **Desenvolvimento** e **Interpretações** podem ser substituídas por **subseções temáticas numeradas** (ex: `## 1. Preferências do Consumidor`). As seções **Conexões** e **Top 5** permanecem obrigatórias como seções finais nomeadas.

**Detecção de conformidade para matérias analíticas:**
- As 3 primeiras seções (`Contexto`, `Desenvolvimento`, `Interpretações`) → presença **opcional** (podem ser substituídas por subseções temáticas)
- `Conexões` → presença **obrigatória**
- `Top 5` → presença **obrigatória**

### 2.4 Disclaimer na Seção Top 5 (RF-16)

A seção "Top 5" deve iniciar com um disclaimer explícito. Formato:

```markdown
## 🎯 Top 5 — O que mais cai no CACD

> ⚠️ Os tópicos abaixo são baseados na **percepção do modelo de IA** sobre o
> padrão histórico de cobrança do concurso. Não se trata de análise estatística
> factual de provas anteriores.

1. ...
2. ...
```

### 2.5 Formatação Markdown

| Elemento | Sintaxe | RF |
|----------|---------|-----|
| Seções | `##` | RF-24 |
| Subseções | `###` | RF-24 |
| Citações históricas | `> texto` | RF-24 |
| Observações especiais | `!!! note` / `!!! warning` / `!!! tip` | RF-24 |
| Termos técnicos | `**termo**` (negrito) | RF-12 |
| Fórmulas matemáticas | `$$..$$` ou `$...$` (MathJax/LaTeX) | RF-25 |
| Diagramas | `` ```mermaid `` | RF-26 |

---

## 3. Prompt Template como Contrato de Geração

O prompt template é a **implementação executável** dos requisitos de conteúdo (ADR-003). Ele traduz os RFs em instruções para a LLM.

### 3.1 Variáveis do Template

| Variável | Fonte | Obrigatória | Exemplo |
|----------|-------|-------------|---------|
| `{concurso}` | Constante por projeto | Sim | `CACD 2026` |
| `{materia}` | Nome da matéria | Sim | `História Mundial` |
| `{capitulo}` | Número + nome | Sim | `1. Estruturas e Ideias Econômicas` |
| `{tema}` | Título do tema do edital | Sim | `1.5 Crise de 1929 e New Deal` |
| `{subtemas_irmaos}` | Lista dos outros temas do capítulo | Sim | `1.1 Rev. Industrial, 1.2 Fases do capitalismo, ...` |
| `{bibliografia}` | Bibliografia de referência do edital | Sim | `HOBSBAWM, Eric. A Era dos Extremos. ...` |

### 3.2 Rastreabilidade Template → Requisitos

| Instrução no Template | RFs que implementa |
|-----------------------|---------------------|
| "Seja DENSO — cada parágrafo..." | RF-22 (2.000-4.000 palavras) |
| "Destaque termos técnicos em **negrito**" | RF-12 |
| "Inclua datas e periodizações precisas" | RF-13 |
| "Cite autores de referência da área" | RF-14 |
| "Apresente as principais correntes interpretativas" | RF-15 |
| Estrutura de 5 seções | RF-09 |
| "Extensão alvo: 2.000-4.000 palavras" | RF-22 |
| "Use `##` para seções, `###` para subseções" | RF-24 |
| "Use `>` para citações de documentos" | RF-24 |
| "Use `!!! note`/`!!! warning`" | RF-24 |

### 3.3 Variantes por Matéria

| Matéria | Template | Diferenças em relação ao base |
|---------|----------|-------------------------------|
| História Mundial | `summary.md` (base) | — |
| Economia | `summary-economia.md` (proposta) | + instrução MathJax (`$$`), + subseções temáticas numeradas (RF-10) |
| Direito | `summary-direito.md` (futura) | + citação de artigos legais, + legislação com número e ano |
| Política Internacional | `summary.md` (base, provavelmente) | A avaliar — estrutura similar a HM |
| História do Brasil | `summary.md` (base, provavelmente) | A avaliar — mesma estrutura de HM |

### 3.4 Contrato de Output Esperado

Dado um prompt preenchido, a LLM deve produzir output que satisfaça **simultaneamente**:

| Critério | Verificável | Método |
|----------|-------------|--------|
| 5 seções obrigatórias (ou variante analítica) | Sim | Regex em headings H2 |
| 2.000–4.000 palavras | Sim | Word count |
| Termos em negrito | Parcialmente | Contagem de `**` |
| Datas precisas | Parcialmente | Heurística (regex `\d{4}`) |
| Autores citados | Parcialmente | Presença de nomes próprios em negrito |
| Pluralidade interpretativa | Não | Avaliação humana |
| Precisão factual | Não | Avaliação humana + bibliografia |

> **Nota:** Critérios não-verificáveis automaticamente (pluralidade, factualidade) dependem da avaliação do Autor no passo 6 do UC-01. Isso é uma limitação inerente — mitigada pelo disclaimer público (RF-32, NFR-15).

---

## 4. Especificação da Navegação (`mkdocs.yml` nav)

### 4.1 Estrutura Hierárquica

O `nav` do `mkdocs.yml` espelha a hierarquia do edital (RF-20):

```yaml
nav:
  - Home: index.md
  - <Nome da Matéria>:
    - Visão Geral: <slug>/index.md
    - <N>. <Nome do Capítulo>:
      - <slug>/<CC-TT-slug>.md
      - <slug>/<CC-TT-slug>.md
      - ...
    - <N>. <Nome do Capítulo>:
      - ...
  - <Outra Matéria>:
    - ...
```

### 4.2 Regras de Geração

| Regra | Descrição | RF |
|-------|-----------|-----|
| NAV-01 | Toda matéria com pelo menos 1 resumo deve ter seção no nav | RF-20 |
| NAV-02 | Primeira entrada de cada matéria é `Visão Geral: <slug>/index.md` | RF-19 |
| NAV-03 | Capítulos agrupados sob a matéria, numerados conforme edital | RF-20 |
| NAV-04 | Todo arquivo `.md` em `docs/<materia>/` (exceto `index.md`) deve ter entrada no nav | RF-21 |
| NAV-05 | A ordem dos temas no nav segue a numeração `CC-TT` do edital | RF-20 |
| NAV-06 | Entradas do nav usam path relativo (sem `docs/` prefixo) | mkdocs.yml |

### 4.3 Geração Automática (proposta — ADR-004)

Quando `data/<materia>.yml` existir, o script `scripts/generate_nav.py` pode gerar a seção nav da matéria:

**Input** (`data/economia.yml`):
```yaml
materia: Economia
slug: economia
capitulos:
  - numero: 1
    nome: Microeconomia
    temas:
      - ref: "1.1"
        nome: Demanda do Consumidor
        slug: demanda-do-consumidor
      - ref: "1.2"
        nome: Oferta do Produtor
        slug: oferta-do-produtor
      # ...
```

**Output** (fragmento YAML para nav):
```yaml
- Economia:
    - Visão Geral: economia/index.md
    - 1. Microeconomia:
      - economia/01-01-demanda-do-consumidor.md
      - economia/01-02-oferta-do-produtor.md
```

---

## 5. Especificação do Metadado do Edital (`data/<materia>.yml`)

### 5.1 Schema (proposto — ADR-004)

```yaml
# data/<materia>.yml
materia: <Nome da Matéria>
slug: <kebab-case>
concurso: <sigla>
ano: <int>
prompt_variante: <filename ou null>
bibliografia:
  - "<referência bibliográfica 1>"
  - "<referência bibliográfica 2>"

capitulos:
  - numero: <int>
    nome: "<Nome do Capítulo>"
    temas:
      - ref: "<edital_ref>"
        nome: "<Nome do Tema>"
        slug: "<kebab-case>"
        status: pendente | completo | em_revisao
        data_geracao: <YYYY-MM-DD ou null>
        modelo_llm: <string ou null>
```

### 5.2 Usos do Metadado

| Uso | Script | Input | Output |
|-----|--------|-------|--------|
| Gerar `index.md` da matéria | `generate_index.py` | `data/<materia>.yml` | `docs/<materia>/index.md` |
| Gerar seção nav do `mkdocs.yml` | `generate_nav.py` | `data/<materia>.yml` | Fragmento YAML |
| Preencher variáveis do prompt | Manual (ou futuro script) | `data/<materia>.yml` | Prompt preenchido |
| Diagnosticar backfill | `validate.py --report` | `data/` + `docs/` | Relatório de gaps |

### 5.3 Prioridade de Implementação

| Uso | Quando | Justificativa |
|-----|--------|---------------|
| Gerar nav | Quando projeto ultrapassar 3 matérias | Nav manual é gerenciável até ~100 temas |
| Gerar index.md | Junto com nav | Mesmo benefício, mesmo gatilho |
| Diagnosticar backfill | Imediato (junto com `validate.py`) | Necessário para RF-38 a RF-41 |
| Preencher prompt | Quando houver > 5 matérias | Preenchimento manual é ok para volume atual |
