# Progression Log — Study Vault

> **Artefato RUP:** Progression Log (Governança)
> **Proprietário:** [RUP] Governante (👑)
> **Status:** In Progress
> **Última atualização:** 2026-07-19
>
> Este artefato é a memória transversal do pipeline. Mantido exclusivamente
> pelo Governante e lido por TODOS os agentes antes de iniciar sua fase.
> Registra decisões, alternativas descartadas, armadilhas, questões não
> resolvidas e premissas — o contexto que artefatos formais não capturam.

---

## Pipeline Status

| Fase | Agente | Status | Artefatos | Confiança |
|------|--------|--------|-----------|-----------|
| Modelagem de Negócios | 📋 AN | ✅ Completo | 5/5 | 🟢 Alta |
| Requisitos | 📋 AR | ✅ Completo | 2/2 | 🟢 Alta |
| Design | 🏛️ Arq | ✅ Completo | 4/4 | 🟢 Alta |
| Implementação | 🔀 Dev | ✅ Completo | 4/4 | 🟢 Alta |
| Qualidade | 🧪 QA | ✅ Completo | 3/3 | 🟢 Alta |
| Deployment | 🏛️ Arq + 🔀 Dev | ✅ Spec completa | 2/2 | 🟢 Alta |

---

## Contexto do Projeto

Study Vault é um projeto de geração de resumos densos por IA para concursos públicos,
começando pelo CACD 2026 (Carreira de Diplomata). Não é um sistema convencional —
é um pipeline de geração de conteúdo estático (MkDocs Material + GitHub Pages).

**O que já existe:** 84 resumos completos (60 História Mundial + 24 Economia),
prompt template, CI/CD, site publicado.

**O que o SDD visa resolver:** Padronização do processo de geração, especificação
formal da estrutura dos tópicos, convenções de naming, critérios de qualidade,
extensibilidade para novas matérias, e automação do pipeline.

**Natureza não-ortodoxo:** O "sistema" aqui é um pipeline de conteúdo, não um
microserviço. Os agentes devem adaptar seus artefatos a esse contexto — sem
forçar abstrações de software onde não cabem.

**Modo de supervisão:** Key Gates Only (gates em AN→AR e Arq→Dev)

---

## Questões Não Resolvidas

> Questões que nenhum agente conseguiu responder. Persistem até serem
> resolvidas pelo humano ou agente downstream. Nunca deletar — marcar como RESOLVIDA.

| ID | Levantada por | Fase | Questão | Status | Resolução |
|----|---------------|------|---------|--------|-----------|
| UQ-001 | 📋 AN | Business | Qual LLM é usada para gerar os resumos? (GPT-4, Claude, Gemini?) | RESOLVIDA | LLMs variadas. Novo requisito: registrar modelo usado no rodapé de cada resumo |
| UQ-002 | 📋 AN | Business | O Autor faz validação factual cruzada com a bibliografia? Com que rigor? | ABERTA | — |
| UQ-006 | 📋 AR | Requisitos | Qual granularidade para `modelo_llm`? Só nome (gpt-4o) ou com snapshot (gpt-4o-2024-05-13)? | RESOLVIDA | Nome do modelo sem snapshot (ex: claude-opus-4-6). Rodapé exibe nome legível (Claude Opus 4.6) |
| UQ-007 | 📋 AR | Requisitos | Backfill dos 84 resumos existentes (RF-38 a RF-41) será manual ou com script? | RESOLVIDA | Script Python (recomendação do Arquiteto — ADR-005) |
| UQ-008 | 🏛️ Arq | Design | validate.py deve tratar index.md diferentemente? (sem frontmatter de resumo) | RESOLVIDA | index.md excluído da coleta (Dev) |
| UQ-009 | 🏛️ Arq | Deployment | Vale adicionar --strict ao mkdocs serve local? | RESOLVIDA | --strict apenas no CI build, serve local sem (Dev) |
| UQ-003 | 📋 AN | Business | Há plano concreto para matérias além de HM e Economia? (Direito, PolInt, Francês, Inglês, Português?) | RESOLVIDA | Sim. Plano: História do Brasil, Português, Geografia, Política Internacional, Direito — todos CACD |
| UQ-004 | 📋 AN | Business | O projeto será tornado público? Impacta acessibilidade, disclaimers, reputação | RESOLVIDA | Sim, será público |
| UQ-005 | 📋 AN | Business | A seção "Top 5" é baseada em análise real de provas anteriores ou percepção da LLM? | RESOLVIDA | Percepção da LLM — não é baseado em análise factual de provas |

---

## Premissas

> Decisões tomadas sem confirmação. Toda premissa é um risco.
> QA deve validar especificamente estas durante verificação.

| ID | Feita por | Fase | Premissa | Risco | Validada? |
|----|-----------|------|----------|-------|-----------|
| AS-01 | 📋 AN | Business | Mapeamento 1:1 (tema → arquivo) é intencional e desejado | Baixo | ❌ |
| AS-02 | 📋 AN | Business | Geração em lotes por capítulo é prática deliberada | Baixo | ❌ |
| AS-03 | 📋 AN | Business | Ausência de automação via API é escolha pragmática (volume finito) | Médio | ❌ |
| AS-04 | 📋 AN | Business | Diferença de estrutura entre HM e Economia é adaptação intencional à matéria | Alto | ❌ |
| AS-05 | 📋 AN | Business | `status: completo` = autor considera pronto para uso, não revisão formal | Médio | ❌ |
| AS-06 | 📋 AR | Requisitos | Formato padronizado de título `"<ano> - <concurso> - <matéria> - <tema>"` é desejado para todas as matérias | Baixo | ❌ |
| AS-07 | 📋 AR | Requisitos | Autor concorda com inversão de dependência prompt→requisitos | Alto | ❌ |
| AS-08 | 📋 AR | Requisitos | "Conexões" e "Top 5" como seções finais invariantes é aceitável para matérias quantitativas | Médio | ❌ |
| AS-09 | 📋 AR | Requisitos | `data_geracao: 2026-04-01` e `modelo_llm: desconhecido` são valores de backfill aceitáveis para os 84 resumos existentes | Baixo | ❌ |
| AS-10 | 🏛️ Arq | Deployment | `mkdocs-material==9.6.14` é a versão instalada localmente | Baixo | ❌ |
| AS-11 | 🏛️ Arq | Deployment | Frontmatter é flat o suficiente para parse via regex (sem pyyaml) | Médio | ✅ Validada pelo Dev (100% dos 80 arquivos) |
| AS-12 | 🔀 Dev | Implementação | Word count via split() é aproximação aceitável (margem 1500-5000 vs spec 2000-4000) | Baixo | ❌ |

---

## Handoff Log

> Append-only. O Governante escreve uma entrada após cada fase concluída.

<!-- Entries appended as pipeline progresses -->

### [2026-07-19] 📋 Analista de Negócios → 📋 Analista de Requisitos

**Entregues:**
- `spec/docs/01-business/vision.md` — Problem statement, posicionamento, 7 Business Goals (BG-01 a BG-07), escopo in/out, restrições, riscos, premissas
- `spec/docs/01-business/glossary.md` — 43 termos em 4 categorias (edital, conteúdo, pipeline, siglas)
- `spec/docs/01-business/stakeholders.md` — 2 stakeholders humanos + 5 atores de sistema, matriz influência×interesse
- `spec/docs/01-business/business-rules.md` — 30 regras (BR-001 a BR-030) em 6 categorias
- `spec/docs/01-business/business-processes.md` — 4 processos (BP-01 a BP-04) com flowcharts Mermaid

**Decisões-chave:**
- Classificação de regras de negócio adaptada ao contexto (sem regulação externa real — edital CACD usado como proxy de "regulatório")
- LLM tratada como ator de sistema, não stakeholder humano
- Inconsistências de formato documentadas como regras BR-028 a BR-030 (não como gap analysis separado)

**Alternativas descartadas:**
- Tratar LLM como stakeholder com "interesses" → antropomorfiza ferramenta
- Processos separados para geração manual vs automatizada → prematura, documentar estado atual
- Gap analysis como artefato separado → mantido dentro de business-rules com categoria "Inconsistências Observadas"

**Armadilhas para agentes downstream:**
- ⚠️ BR-028 a BR-030 são GAPS observados, não regras prescritivas — AR deve avaliar se viram requisitos de padronização
- ⚠️ Ausência de processo formal de revisão (BR-025) é o maior risco de qualidade
- ⚠️ O prompt template é o artefato mais importante do projeto — funciona como "spec informal". AR deve decidir: requisitos derivados DO template, ou template derivado DOS requisitos?
- ⚠️ Diferença estrutural entre resumos de HM (5 seções nomeadas) e Economia (seções numeradas) pode ser intencional — AS-04

**Avaliação de confiança:**
- 🟢 Domínio e escopo: alta confiança — projeto bem delimitado
- 🟢 Processos existentes: alta confiança — evidências no git log e estrutura
- 🟡 Regras de qualidade: média confiança — inferidas do output, não de especificação
- 🟡 Extensibilidade: média confiança — intenção clara mas sem processo definido
- 🔴 Validação factual: baixa confiança — UQ-002 sem resposta

**Novas questões não resolvidas:**
- ❓ UQ-001 a UQ-005 [adicionadas à tabela]

**Novas premissas:**
- 💭 AS-01 a AS-05 [adicionadas à tabela]

### [2026-07-19] 📋 Analista de Requisitos → 🏛️ Arquiteto

**Entregues:**
- `spec/docs/02-requirements/requirements.md` — 41 RFs + 18 NFRs + rastreabilidade para 30 BRs
- `spec/docs/02-requirements/use_cases.md` — 5 UCs com fluxos principal/alternativo/exceção + diagrama Mermaid

**Decisões-chave:**
- **Inversão de dependência**: requisitos são fonte de verdade, prompt template é artefato derivado (não o contrário)
- **Flexibilidade controlada (RF-10)**: seções internas flexíveis por matéria, mas "Conexões" e "Top 5" invariantes
- **Novos campos frontmatter**: `data_geracao` (RF-05), `modelo_llm` (RF-06), `materia` e `concurso` (RF-02)
- **Rodapé com modelo**: `*Gerado por IA ({modelo_llm}). Sujeito a revisão.*` (RF-11)

**Alternativas descartadas:**
- Manter prompt como fonte de verdade → impede rastreabilidade formal
- Exigir 5 seções idênticas para todas as matérias → Economia/Direito não cabem
- Processo de revisão formal com múltiplos revisores → desproporcional para single-user

**Armadilhas para agentes downstream:**
- ⚠️ O "sistema" não é software convencional — Arquiteto deve resistir a propor componentes onde um checklist markdown resolve
- ⚠️ RF-33 (checklist conformidade) e UC-05 (validação) são candidatos a automação via script Python simples
- ⚠️ Resolução de BR-028 a BR-030 via RF-38 a RF-41 é lote de migração, não feature — precisa de plano de execução
- ⚠️ AS-04 resolvida por RF-10 (flexibilidade controlada) — Arq deve validar que não erode padronização

**Avaliação de confiança:**
- 🟢 Estrutura dos resumos: alta — baseada em análise direta de 84 arquivos
- 🟢 Naming e frontmatter: alta — convenções claras e rastreáveis
- 🟡 Critérios de qualidade: média — word count e densidade são verificáveis, qualidade factual não
- 🟡 Extensibilidade: média — regras definidas mas não testadas em novas matérias
- 🔴 Validação factual: baixa — UQ-002 continua aberta, sem mitigação técnica

**Novas questões não resolvidas:**
- ❓ UQ-006 (granularidade modelo_llm)
- ❓ UQ-007 (backfill manual vs script)

**Novas premissas:**
- 💭 AS-06 a AS-09 [adicionadas à tabela]

### [2026-07-19] 🏛️ Arquiteto → 🔀 Desenvolvedor

**Entregues:**
- `spec/docs/03-design/architecture.md` — Estrutura canônica, pipeline de conteúdo, 6 ADRs, tooling proposto (349 linhas)
- `spec/docs/03-design/domain_model.md` — Entidades, hierarquia, ciclo de vida, diagramas Mermaid (254 linhas)
- `spec/docs/03-design/api_spec.md` — Schema frontmatter, formato markdown, contrato prompt, nav spec (354 linhas)
- `spec/docs/03-design/sequence_diagrams.md` — 4 diagramas de fluxo Mermaid (269 linhas)
- `spec/docs/06-deployment/ci_cd_pipeline.md` — Pipeline atual + proposta com validação (283 linhas)
- `spec/docs/06-deployment/infrastructure.md` — GitHub Pages, Actions, dependências (268 linhas)

**Decisões-chave:**
- ADR-005: validate.py usa APENAS stdlib Python (regex para frontmatter, sem pyyaml)
- Pipeline: validação como step dentro do job build (não job separado) — economia de ~40s setup
- Backfill recomendado via script Python (resolve UQ-007)
- Estrutura canônica de diretórios formalizada (docs/, scripts/, spec/, data/)

**Armadilhas para Dev:**
- ⚠️ validate.py PRECISA ser implementado — é o quality gate do CI
- ⚠️ requirements.txt não existe — criar com mkdocs-material pinado
- ⚠️ deploy.yml atual NÃO foi alterado — Dev deve implementar as mudanças propostas
- ⚠️ Nota do Arq: architecture.md menciona "yaml stdlib" mas yaml (PyYAML) NÃO é stdlib — o ADR já corrige pra regex

**Avaliação de confiança:**
- 🟢 Estrutura e tooling: alta — proporcional ao projeto
- 🟢 Pipeline CI/CD: alta — GitHub Actions é simples e bem documentado
- 🟡 validate.py regex vs pyyaml: média — funciona para flat YAML mas frágil se frontmatter crescer
- 🟡 Pinning de versão: média — AS-10 precisa confirmar versão real

**Novas questões:** UQ-008, UQ-009
**Novas premissas:** AS-10, AS-11

### [2026-07-19] 🔀 Desenvolvedor → 🧪 Analista de Qualidade

**Entregues:**
- `scripts/validate.py` — Validador de conformidade (365 linhas, stdlib only, 11 checks)
- `scripts/backfill.py` — Normalizador de frontmatter/rodapé (294 linhas, dry-run por default)
- `requirements.txt` — mkdocs-material==9.6.14 (pinado)
- `.github/workflows/deploy.yml` — Atualizado com step de validação + --strict + cache pip
- `spec/docs/04-implementation/` — 4 artefatos (724 linhas)

**Validação executada:**
- validate.py roda com sucesso: 502 erros em 80 arquivos (esperados — campos faltantes pré-backfill)
- backfill.py em dry-run: 80 arquivos, 426 alterações planejadas
- AS-10 validada: mkdocs-material==9.6.14 confirmada
- AS-11 validada: regex cobre 100% dos frontmatters existentes

**Decisões-chave:**
- Word count margem ampliada (1500-5000 vs spec 2000-4000) como AVISO, não ERRO
- index.md excluído da validação
- --strict no CI build, não no serve local

**Armadilhas para QA:**
- ⚠️ Backfill NÃO foi executado — resumos ainda estão no estado original
- ⚠️ Alguns resumos de Economia NÃO têm seção "Conexões" — backfill não corrige corpo
- ⚠️ Heurística de extração de tema do título pode gerar slugs longos demais

### [2026-07-19] 🧪 Analista de Qualidade → 👑 Governante (Pipeline Completo)

**Entregues:**
- `spec/docs/05-test/test_strategy.md` — Estratégia de verificação adaptada a conteúdo estático (174 linhas)
- `spec/docs/05-test/test_coverage_map.md` — Matriz RF→Verificação para 41 RFs (232 linhas)
- `spec/docs/05-test/test_patterns.md` — Padrões de verificação e checklists (207 linhas)
- `spec/docs/07-change-management/technical_debt.md` — 12 dívidas técnicas catalogadas (79 linhas)
- `spec/docs/07-change-management/risks_and_limitations.md` — Riscos e limitações do projeto público (97 linhas)

**Veredicto: CONDITIONAL_GO**

Blockers para resolução:
- **TD-001 (P0):** Backfill pendente — 1 comando resolve 418/502 erros
- **TD-002 (P1):** 25 resumos sem seção "Conexões" e/ou "Top 5" — requer geração de conteúdo
- **TD-003 (P1):** 48 resumos sem admonition de temas irmãos — template mecânico mas volume alto

**Descoberta não prevista:** 48/80 resumos sem admonition `!!! info` — gap sistêmico não catalogado pelo AN

**Premissas validadas:**
- ✅ AS-10: mkdocs-material==9.6.14 (porém TD-007 nota drift para 9.7.6 local)
- ✅ AS-11: regex cobre 100% dos frontmatters
- ❌ AS-04 parcialmente invalidada: diferença HM vs Economia NÃO é apenas adaptação — Economia falta seções inteiras
