# Estratégia de Testes — Study Vault

> **Artefato RUP:** Estratégia de Testes (Qualidade)
> **Proprietário:** [RUP] Analista de Qualidade
> **Status:** Complete
> **Última atualização:** 2026-07-21

---

## 1. Natureza do Projeto e Implicações para Testes

O Study Vault **não é software convencional** — é um pipeline de geração de conteúdo estático. Não há APIs, banco de dados, serviços em execução ou lógica de negócio em runtime. O "sistema" é composto de:

- Resumos markdown com frontmatter estruturado
- Scripts Python de validação/normalização
- Pipeline CI/CD (GitHub Actions)
- Site estático (MkDocs Material → GitHub Pages)

Isso muda fundamentalmente a estratégia de testes: **não há testes unitários no sentido clássico**. O ato de "testar" aqui é **verificar conformidade** de conteúdo contra a especificação.

---

## 2. Pirâmide de Testes Adaptada

```
          ╔═══════════════════════╗
          ║  Revisão Humana (RF)  ║  ← Validação factual, pluralidade,
          ║     Não automatizável ║     qualidade argumentativa
          ╚══════════╤════════════╝
         ╔═══════════╧════════════════╗
         ║  Build Gate (mkdocs build) ║  ← Links, YAML, renderização
         ║        --strict            ║
         ╚═══════════╤════════════════╝
    ╔════════════════╧═════════════════════╗
    ║  Validação Automatizada (validate.py)║  ← Frontmatter, seções,
    ║       11 checks × 80+ arquivos      ║     word count, naming
    ╚══════════════════════════════════════╝
```

| Camada | Ferramenta | Cobertura | Execução |
|--------|-----------|-----------|----------|
| **Base: Validação automatizada** | `scripts/validate.py` | Conformidade estrutural (frontmatter, seções, word count, naming, rodapé) | Local + CI (pré-build) |
| **Meio: Build gate** | `mkdocs build --strict` | Integridade do site (links, YAML, markdown válido, nav consistente) | Local + CI (pós-validação) |
| **Topo: Revisão humana** | Leitura do Autor | Qualidade factual, precisão de datas, autores citados, pluralidade interpretativa | Manual, pós-geração |

### 2.1 O que NÃO é testável automaticamente

| Requisito | Por que não é automatizável | Mitigação |
|-----------|----------------------------|-----------|
| RF-13 (datas precisas) | Exige conhecimento factual do domínio | Revisão humana + bibliografia no prompt |
| RF-14 (autores citados com teses) | Exige avaliação semântica | Revisão humana |
| RF-15 (pluralidade interpretativa) | Exige julgamento acadêmico | Revisão humana |
| RF-23 (baseado na bibliografia) | Verificação factual cruzada impossível | Disclaimer público (RF-32, NFR-15) |
| NFR-08 (consistência terminológica) | Requer NLP cross-documento | Fora do escopo atual |

---

## 3. Ferramentas e Frameworks

| Ferramenta | Papel | Dependência |
|-----------|-------|-------------|
| `scripts/validate.py` | Test suite principal — validação de conformidade | Python 3.12 stdlib only |
| `scripts/backfill.py` | Normalização pré-teste (dry-run → apply) | Python 3.12 stdlib only |
| `mkdocs build --strict` | Build gate — integridade do site | mkdocs-material==9.6.14 |
| `python3 validate.py` (CI step) | Quality gate pré-build no GitHub Actions | Integrado no deploy.yml |

### 3.1 Ausência Intencional de Frameworks

- **pytest**: volume de "código testável" não justifica framework. Os scripts são simples e seu output é diretamente verificável
- **markdownlint**: verifica formatação genérica, não semântica do projeto (ADR-005)
- **JSON Schema**: parcial — só cobriria frontmatter. O validate.py cobre tudo

---

## 4. Perfis de Validação

### 4.1 Validação Completa (pré-deploy)

```bash
python3 scripts/validate.py --path docs/ --verbose
```

Executada: a cada push no CI + localmente antes de commits de conteúdo.

### 4.2 Validação por Matéria

Não implementada como flag, mas viável via:
```bash
python3 scripts/validate.py --path docs/economia/
```
Nota: a interface `--path` aceita qualquer subdiretório.

### 4.3 Validação Pré/Pós-Backfill

```bash
# 1. Estado atual (diagnóstico)
python3 scripts/validate.py --path docs/ > pre-backfill.txt

# 2. Dry-run do backfill
python3 scripts/backfill.py --path docs/

# 3. Aplicar backfill
python3 scripts/backfill.py --path docs/ --apply

# 4. Estado pós-backfill
python3 scripts/validate.py --path docs/ > post-backfill.txt

# 5. Comparar
diff pre-backfill.txt post-backfill.txt
```

---

## 5. Estratégia de Mocking

Não aplicável. Não há dependências externas, APIs, bancos ou serviços para mockar. Os scripts operam diretamente sobre arquivos markdown no filesystem.

---

## 6. Gestão de Dados de Teste

Os "dados de teste" são os próprios 80 resumos existentes em `docs/`. Não há necessidade de massa de teste sintética — o conteúdo real é o alvo da validação.

Para validação do backfill, o procedimento é:
1. Capturar estado pré-backfill (output do validate.py)
2. Executar backfill em dry-run
3. Aplicar backfill
4. Comparar estado pós-backfill

---

## 7. Metas de Cobertura e Gaps Atuais

### 7.1 Metas

| Alvo | Meta | Atual |
|------|------|-------|
| RFs verificáveis automaticamente | 100% cobertos por validate.py | 14/41 RFs cobertos (34%) |
| RFs verificáveis por build gate | 100% cobertos por mkdocs build | ~5 RFs adicionais |
| Arquivos sem ERRO no validate.py | 100% pós-backfill | 0/80 (0%) — pré-backfill |
| Arquivos sem AVISO | ≥ 90% pós-backfill | 11/80 (14%) — pré-backfill |

### 7.2 Gaps Identificados

| Gap | Impacto | RF/NFR | Resolução |
|-----|---------|--------|-----------|
| validate.py não verifica FRONT-08 (materia vs diretório) | Baixo — backfill garante consistência | RF-02 | TD-005 |
| validate.py não verifica RF-16 (disclaimer dentro do Top 5) | Médio — transparência ao leitor | RF-16, NFR-18 | TD-006 |
| validate.py não verifica kebab-case/acentos no slug | Baixo — todos os 80 arquivos conformes | RF-17 | Risco baixo, não bloqueia |
| 25 arquivos sem seção "Conexões" (20 Economia + 5 HM) | Alto — backfill.py não resolve (requer conteúdo) | RF-09, RF-39 | TD-002 |
| 5 arquivos HM sem seção "Top 5" | Alto — mesmo caso | RF-09 | TD-002 |
| 48 arquivos sem admonition `!!! info` | Alto — mas backfill.py não cobre | RF-08 | TD-007 |

---

## 8. Integração com CI/CD

O validate.py está integrado no pipeline como **primeiro step executável** (fail-fast):

```yaml
# .github/workflows/deploy.yml
- name: Validate content conformity
  run: python scripts/validate.py --path docs/
```

**Ordem de execução:**
1. Checkout
2. Setup Python 3.12 (com cache pip)
3. **validate.py** ← quality gate (exit 1 = pipeline para)
4. pip install
5. mkdocs build --strict ← build gate
6. Upload + deploy

**Consequência:** atualmente, com 502 ERROs, o deploy **falharia** se o validate.py estivesse no CI do estado corrente. O backfill é pré-condição para que o CI funcione.
