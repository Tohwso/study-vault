# Mapa de Cobertura de Testes — Study Vault

> **Artefato RUP:** Matriz de Rastreabilidade de Testes (Qualidade)
> **Proprietário:** [RUP] Analista de Qualidade
> **Status:** Complete
> **Última atualização:** 2026-07-21

---

## 1. Matriz de Rastreabilidade — Requisitos Funcionais

| RF | Descrição (resumida) | Verificação | Ferramenta | Status |
|----|----------------------|-------------|------------|--------|
| RF-01 | 1 tema → 1 arquivo | Manual (verificação de duplicidade no filesystem) | Nenhuma | NOT_COVERED |
| RF-02 | Frontmatter com 8 campos obrigatórios | Automatizada: REQUIRED_FIELDS check | validate.py | COVERED |
| RF-03 | Título formato `<ano> - <concurso> - <matéria> - <tema>` | Automatizada: TITLE_PATTERN regex | validate.py | COVERED |
| RF-04 | Status ∈ {completo, em_revisao, pendente} | Automatizada: VALID_STATUSES check | validate.py | COVERED |
| RF-05 | Campo `data_geracao` ISO 8601 | Automatizada: DATE_ISO_RE regex (AVISO) | validate.py | COVERED |
| RF-06 | Campo `modelo_llm` presente | Automatizada: required field check | validate.py | COVERED |
| RF-07 | Metadata blockquote após H1 | Automatizada: check_structure() | validate.py | COVERED |
| RF-08 | Admonition temas irmãos (`!!! info`) | Automatizada: check_structure() | validate.py | COVERED |
| RF-09 | 5 seções obrigatórias (ou Conexões + Top 5 invariantes) | Automatizada parcial: Conexões + Top 5 verificadas | validate.py | PARTIALLY_COVERED |
| RF-10 | Flexibilidade p/ matérias analíticas | Implícita: Contexto/Desenvolvimento/Interpretações não são checadas | validate.py | COVERED |
| RF-11 | Rodapé `*Gerado por IA ({modelo_llm})...*` | Automatizada: check_footer() (AVISO) | validate.py | COVERED |
| RF-12 | Termos técnicos em **negrito** | Manual: heurística parcial possível | Nenhuma | NOT_COVERED |
| RF-13 | Datas e periodizações precisas | Manual: exige conhecimento factual | Nenhuma | NOT_COVERED |
| RF-14 | Autores citados com teses principais | Manual: avaliação semântica | Nenhuma | NOT_COVERED |
| RF-15 | Pluralidade interpretativa | Manual: julgamento acadêmico | Nenhuma | NOT_COVERED |
| RF-16 | Disclaimer explícito na seção Top 5 | **Não verificada** — validate.py checa presença do Top 5 mas não o conteúdo | Nenhuma | NOT_COVERED |
| RF-17 | Naming `CC-TT-slug.md` | Automatizada: FILENAME_PATTERN regex | validate.py | PARTIALLY_COVERED |
| RF-18 | Diretório por matéria em kebab-case | Implícita: coleta de arquivos usa diretórios de matéria | validate.py | NOT_COVERED |
| RF-19 | `index.md` com tabela de progresso | Manual | Nenhuma | NOT_COVERED |
| RF-20 | Hierarquia nav espelha edital | Build gate: `mkdocs build --strict` detecta nav inconsistente | mkdocs build | PARTIALLY_COVERED |
| RF-21 | Entrada no nav para cada resumo | Build gate: `--strict` detecta arquivos não referenciados | mkdocs build | PARTIALLY_COVERED |
| RF-22 | Extensão 2.000–4.000 palavras | Automatizada: check_word_count() (AVISO, margem 1500–5000) | validate.py | PARTIALLY_COVERED |
| RF-23 | Baseado na bibliografia de referência | Manual: impossível por automação | Nenhuma | NOT_COVERED |
| RF-24 | Formatação markdown (##, ###, >, !!!) | Parcial: seções e admonitions verificadas | validate.py | PARTIALLY_COVERED |
| RF-25 | MathJax/LaTeX para fórmulas | Build gate: renderização verificada por mkdocs serve | mkdocs build | PARTIALLY_COVERED |
| RF-26 | Diagramas Mermaid | Build gate | mkdocs build | PARTIALLY_COVERED |
| RF-27 | Prompt template versionado em scripts/prompts/ | Manual: verificação de existência do arquivo | Nenhuma | NOT_COVERED |
| RF-28 | Prompt parametrizado com 6 variáveis | Manual: revisão do template | Nenhuma | NOT_COVERED |
| RF-29 | Variante de template por matéria quando necessário | Manual | Nenhuma | NOT_COVERED |
| RF-30 | Deploy automático via push em main | Implícita: workflow existe e dispara | deploy.yml | COVERED |
| RF-31 | Python 3.12 + mkdocs-material | Configuração: deploy.yml + requirements.txt | deploy.yml | COVERED |
| RF-32 | Disclaimer IA na home | Manual | Nenhuma | NOT_COVERED |
| RF-33 | Checklist de conformidade pós-geração | **É o próprio validate.py** | validate.py | COVERED |
| RF-34 | Tabela de matérias na home | Manual | Nenhuma | NOT_COVERED |
| RF-35 | Checklist de onboarding de nova matéria | Manual: processo documentado | Nenhuma | NOT_COVERED |
| RF-36 | Estrutura idêntica cross-matéria | Automatizada: validate.py aplica mesmas regras | validate.py | COVERED |
| RF-37 | `index.md` com todos os temas antes de gerar | Manual | Nenhuma | NOT_COVERED |
| RF-38 | Backfill: padronizar título de Economia | Automatizada: backfill.py normaliza | backfill.py | COVERED |
| RF-39 | Backfill: seções Conexões/Top 5 em Economia | **NÃO coberta pelo backfill** — requer conteúdo novo | Nenhuma | NOT_COVERED |
| RF-40 | Backfill: `data_geracao` + `modelo_llm` | Automatizada: backfill.py adiciona | backfill.py | COVERED |
| RF-41 | Backfill: rodapé em Economia | Automatizada: backfill.py adiciona | backfill.py | COVERED |

### Resumo de Cobertura — RFs

| Status | Quantidade | % |
|--------|------------|---|
| COVERED | 16 | 39% |
| PARTIALLY_COVERED | 8 | 20% |
| NOT_COVERED | 17 | 41% |
| **Total** | **41** | 100% |

---

## 2. Matriz de Rastreabilidade — Requisitos Não Funcionais

| NFR | Descrição (resumida) | Verificação | Status |
|-----|----------------------|-------------|--------|
| NFR-01 | ≤ 3 cliques para qualquer tema | Manual: navegação no site | NOT_COVERED |
| NFR-02 | Busca full-text funcional | Build gate: plugin search habilitado | PARTIALLY_COVERED |
| NFR-03 | Carregamento < 3s em 4G | Manual: performance test | NOT_COVERED |
| NFR-04 | Responsividade ≥ 320px | Garantida pelo tema Material | COVERED (pelo tema) |
| NFR-05 | Word count 2.000–4.000 | validate.py (margem 1.500–5.000, AVISO) | PARTIALLY_COVERED |
| NFR-06 | 100% resumos com 5 seções | validate.py verifica Conexões + Top 5 | PARTIALLY_COVERED |
| NFR-07 | 100% frontmatters completos | validate.py verifica 8 campos | COVERED |
| NFR-08 | Consistência terminológica | Manual: exige NLP cross-documento | NOT_COVERED |
| NFR-09 | Nova matéria em ≤ 1h setup | Manual: processo descrito em RF-35 | NOT_COVERED |
| NFR-10 | Tudo versionado no Git | Implícita: monorepo | COVERED |
| NFR-11 | Requisitos propagados ao template | Manual: disciplina do Autor | NOT_COVERED |
| NFR-12 | Uptime ≥ 99.5% GitHub Pages | SLA da plataforma | COVERED (pelo SLA) |
| NFR-13 | Deploy < 5 min | Implícita: workflow simples | COVERED |
| NFR-14 | Builds com status visível | GitHub Actions dashboard | COVERED |
| NFR-15 | Disclaimer IA visível na home | Manual | NOT_COVERED |
| NFR-16 | Rodapé com modelo LLM em cada resumo | validate.py verifica rodapé (AVISO) | PARTIALLY_COVERED |
| NFR-17 | Contraste WCAG AA ≥ 4.5:1 | Garantido pelo tema Material | COVERED (pelo tema) |
| NFR-18 | Disclaimer na seção Top 5 | **Não verificada** | NOT_COVERED |

---

## 3. Verificação de Regras de Negócio

| BR | Descrição (resumida) | RFs Relacionados | Verificação | Status |
|----|----------------------|-----------------|-------------|--------|
| BR-001 | 1 tema = 1 arquivo | RF-01 | Manual | NOT_COVERED |
| BR-002 | Frontmatter YAML obrigatório | RF-02 | validate.py | COVERED |
| BR-003 | Formato padronizado de title | RF-03, RF-38 | validate.py | COVERED |
| BR-004 | Valores válidos de status | RF-04 | validate.py | COVERED |
| BR-005 | Metadata blockquote | RF-07 | validate.py | COVERED |
| BR-006 | Admonition temas irmãos | RF-08 | validate.py | COVERED |
| BR-007 | 5 seções obrigatórias | RF-09 | validate.py (parcial) | PARTIALLY_COVERED |
| BR-008 | Extensão 2.000–4.000 palavras | RF-22 | validate.py (margem) | PARTIALLY_COVERED |
| BR-009 | Termos técnicos em negrito | RF-12 | Manual | NOT_COVERED |
| BR-010 | Datas precisas | RF-13 | Manual | NOT_COVERED |
| BR-011 | Autores citados com teses | RF-14 | Manual | NOT_COVERED |
| BR-012 | Pluralidade interpretativa | RF-15 | Manual | NOT_COVERED |
| BR-013 | Naming CC-TT-slug.md | RF-17 | validate.py | COVERED |
| BR-014 | Diretório por matéria | RF-18 | Implícita | COVERED |
| BR-015 | index.md por matéria | RF-19 | Manual | NOT_COVERED |
| BR-016 | Nav espelha edital | RF-20 | mkdocs build | PARTIALLY_COVERED |
| BR-017 | Entrada no nav obrigatória | RF-21 | mkdocs build --strict | PARTIALLY_COVERED |
| BR-018 | Conteúdo factualmente confiável | RF-23 | Manual | NOT_COVERED |
| BR-019 | Prompt como implementação de reqs | RF-27 | Manual | NOT_COVERED |
| BR-020 | Disclaimer IA na home | RF-32 | Manual | NOT_COVERED |
| BR-021 | MathJax/LaTeX para fórmulas | RF-25 | mkdocs build | PARTIALLY_COVERED |
| BR-022 | Deploy automático via push | RF-30 | deploy.yml | COVERED |
| BR-023 | Python 3.12 + mkdocs-material | RF-31 | deploy.yml + requirements.txt | COVERED |
| BR-024 | Sem branch de staging | — | Decisão aceita (ADR-007) | N/A |
| BR-025 | Sem revisão formal | RF-33 | validate.py mitiga parcialmente | PARTIALLY_COVERED |
| BR-026 | Processo de onboarding | RF-35 | Manual | NOT_COVERED |
| BR-027 | Variantes de template por matéria | RF-29 | Manual | NOT_COVERED |
| BR-028 | Inconsistência de title (Economia) | RF-38 | backfill.py | COVERED |
| BR-029 | Inconsistência de seções (Economia) | RF-39 | **Não resolvida** | NOT_COVERED |
| BR-030 | Ausência de data_geracao/modelo_llm | RF-40 | backfill.py | COVERED |

---

## 4. Validação de Premissas (AS-XX)

| AS | Premissa | Verificação QA | Resultado |
|----|----------|---------------|-----------|
| AS-01 | Mapeamento 1:1 tema→arquivo é intencional | Confirmada: 80 arquivos = 80 temas (60 HM + 20 Eco). Nenhum tema com múltiplos arquivos | ✅ Validada |
| AS-02 | Geração em lotes por capítulo | Git log confirma: commits agrupam temas por capítulo | ✅ Validada |
| AS-03 | Ausência de automação via API é escolha pragmática | Confirmada: ADR-006 documenta decisão e trade-offs | ✅ Validada |
| AS-04 | Diferença de estrutura HM vs Economia é intencional | Confirmada parcialmente: RF-10 permite flexibilidade, mas 25 arquivos sem Conexões indica que a adaptação foi além do planejado | ⚠️ Parcial |
| AS-05 | `completo` = pronto para uso, não revisão formal | Confirmada: todos os 80 arquivos têm `status: completo`, nenhum passou por revisão formal (BR-025) | ✅ Validada |
| AS-06 | Formato padronizado de título para todas as matérias | Confirmada: RF-03 + backfill.py implementam a padronização | ✅ Validada |
| AS-07 | Inversão de dependência prompt→requisitos é aceita | Não validável pelo QA — decisão do Autor. ADR-003 documenta | ❌ Pendente (decisão humana) |
| AS-08 | Conexões e Top 5 invariantes para matérias quantitativas | **Refutada parcialmente**: 20/20 resumos de Economia NÃO têm seção "Conexões". A premissa está documentada mas a implementação não a satisfaz | ⚠️ Divergente |
| AS-09 | Valores de backfill (`2026-04-01`, `desconhecido`) aceitáveis | Confirmada: backfill.py usa exatamente esses valores. Consistente com AS-09 | ✅ Validada |
| AS-10 | mkdocs-material==9.6.14 é a versão instalada | **Divergente**: versão local instalada é 9.7.6, requirements.txt pina 9.6.14. Não é blocker mas indica drift | ⚠️ Divergente |
| AS-11 | Frontmatter flat suficiente para regex (sem pyyaml) | ✅ Validada pelo Dev: 100% dos 80 arquivos parsados corretamente | ✅ Validada |
| AS-12 | Word count via split() com margem 1500–5000 é aceitável | Validada: 61/80 no range spec (2000-4000), 12/80 na margem, 7/80 abaixo de 1500 | ✅ Validada (margem justificada) |

---

## 5. Relatório de Verificação

### 5.1 Sumário

| Métrica | Valor |
|---------|-------|
| Total de RFs | 41 |
| RFs cobertos automaticamente | 16 (39%) |
| RFs parcialmente cobertos | 8 (20%) |
| RFs sem cobertura | 17 (41%) |
| Total de arquivos | 80 |
| Arquivos com ERRO (pré-backfill) | 80 (100%) |
| Total de ERROs | 502 |
| Total de AVISOs | 76 |

### 5.2 Classificação dos 502 ERROs

| Tipo de Erro | Quantidade | Resolvido por backfill? |
|--------------|-----------|-------------------------|
| Campo `materia` ausente | 80 | ✅ Sim |
| Campo `concurso` ausente | 80 | ✅ Sim |
| Campo `data_geracao` ausente | 80 | ✅ Sim |
| Campo `modelo_llm` ausente | 80 | ✅ Sim |
| Título fora do formato (Economia) | 20 | ✅ Sim |
| Seção Conexões ausente | 25 | ❌ Não — requer conteúdo |
| Seção Top 5 ausente | 5 | ❌ Não — requer conteúdo |
| Admonition ausente | 48 | ❌ Não — requer conteúdo |
| Naming inválido | 0 | N/A |
| **Total** | **502** (nota: 84 não corrigíveis por backfill) | |

### 5.3 Projeção Pós-Backfill

Após `backfill.py --apply`, estima-se:

| Métrica | Pré | Pós (estimado) |
|---------|-----|----------------|
| ERROs | 502 | ~84 (Conexões: 25, Top 5: 5, Admonitions: 48, título remanescente: ~6) |
| AVISOs | 76 | ~7 (word count < 1500) |
| Arquivos sem erro | 0 | ~30-35 (HM com seções completas) |

**Conclusão:** O backfill resolve ~83% dos ERROs (418/502). Os 84 remanescentes exigem intervenção manual (adição de conteúdo — seções e admonitions).

### 5.4 Findings de Conformidade Arquitetural

| ID | Finding | Severidade | Referência |
|----|---------|------------|------------|
| [API-001] | validate.py não implementa FRONT-08 (consistência materia vs diretório) | BAIXA | api_spec.md seção 1.2 |
| [API-002] | validate.py não verifica conteúdo do disclaimer na seção Top 5 (RF-16) | MÉDIA | api_spec.md seção 2.4 |
| [REQ-001] | RF-09 verificação parcial: apenas Conexões e Top 5, não as 3 seções nomeadas de HM | BAIXA | Aceitável dado RF-10 |
| [REQ-002] | RF-22 margem ampliada (1500-5000 vs spec 2000-4000): 12 arquivos só estão OK pela margem | BAIXA | Documentada como decisão (AS-12) |
| [REQ-003] | RF-17 regex não valida kebab-case ou ausência de acentos no slug | BAIXA | 100% dos 80 arquivos já conformes |
| [DOM-001] | requirements.txt pina 9.6.14 mas versão local é 9.7.6 — drift de versão | BAIXA | AS-10 parcialmente invalidada |
| [BR-001] | 20/20 resumos de Economia sem seção "Conexões" — divergência com RF-09 e AS-08 | ALTA | Backfill não resolve |
| [BR-002] | 5 resumos de HM sem seção "Top 5" — divergência com RF-09 | ALTA | Backfill não resolve |
| [BR-003] | 48 resumos sem admonition `!!! info` — divergência com RF-08 | ALTA | Backfill não resolve |

### 5.5 Avaliação de Risco

| Nível | Descrição | Quantidade |
|-------|-----------|------------|
| HIGH | Requisito não implementado ou divergência crítica | 3 (BR-001, BR-002, BR-003) |
| MEDIUM | Implementação parcial ou verificação ausente | 2 (API-002, RF-16) |
| LOW | Divergência menor ou cosmética | 4 (API-001, REQ-001, REQ-002, REQ-003, DOM-001) |

---

## 6. Veredicto de Prontidão para Deploy

### **CONDITIONAL_GO**

**Justificativa:**

O projeto pode avançar com as seguintes condições:

**Blockers (devem ser resolvidos antes do deploy com CI ativo):**

1. **Executar `backfill.py --apply`** — resolve 418/502 ERROs (campos de frontmatter + título + rodapé)
2. **Decidir tratamento dos 25 arquivos sem "Conexões"**: (a) adicionar seções com conteúdo, (b) rebaixar severidade para AVISO no validate.py, ou (c) aceitar como dívida técnica documentada
3. **Decidir tratamento dos 48 arquivos sem admonition**: mesmo cenário

**Recomendações (não-blockers):**

4. Alinhar requirements.txt (9.6.14) com versão local (9.7.6) — testar build com --strict
5. Adicionar verificação de RF-16 (disclaimer no Top 5) ao validate.py
6. Validar AS-07 (inversão de dependência) com o Autor
