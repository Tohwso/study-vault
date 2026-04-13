# Dívidas Técnicas — Study Vault

> **Artefato RUP:** Technical Debt Catalog (Gestão de Mudanças)
> **Proprietário:** [RUP] Analista de Qualidade
> **Status:** Complete
> **Última atualização:** 2026-07-21

---

## Catálogo de Dívidas Técnicas

| ID | Categoria | Descrição | Impacto | Esforço | Prioridade |
|----|-----------|-----------|---------|---------|------------|
| TD-001 | Conteúdo | Backfill pendente: 80 arquivos, 426 alterações (frontmatter, título, rodapé) | Alto — CI com validate.py bloqueia deploy | Baixo — 1 comando (`backfill.py --apply`) | **P0** |
| TD-002 | Conteúdo | 25 resumos sem seção "Conexões" (20 Economia + 5 HM) e 5 HM sem "Top 5" | Alto — viola RF-09 (seções invariantes). CI bloqueia | Alto — requer geração de conteúdo para cada arquivo | **P1** |
| TD-003 | Conteúdo | 48 resumos sem admonition `!!! info` de temas irmãos | Alto — viola RF-08. CI bloqueia | Médio — template mecânico, mas 48 arquivos | **P1** |
| TD-004 | Processo | Prompt template não derivado dos requisitos (inversão pendente, AS-07) | Médio — requisitos existem mas o template ainda é a fonte de facto | Médio — reescrever template a partir dos RFs | **P2** |
| TD-005 | Testing | validate.py não verifica consistência `materia` vs diretório (FRONT-08 do api_spec.md) | Baixo — backfill garante consistência inicial | Baixo — ~10 linhas de código | **P3** |
| TD-006 | Testing | validate.py não verifica conteúdo do disclaimer na seção Top 5 (RF-16, NFR-18) | Médio — transparência ao leitor em projeto público | Baixo — regex adicional | **P2** |
| TD-007 | Configuração | Drift de versão: requirements.txt pina 9.6.14 mas versão local é 9.7.6 | Baixo — ambas funcionam, mas CI usa 9.6.14 e local usa 9.7.6 | Trivial — atualizar 1 linha | **P3** |
| TD-008 | Conteúdo | Word count: 7 resumos abaixo de 1500 palavras (Economia: oferta, contas externas, IS-LM-BP, etc.) | Médio — abaixo da margem do validador. Viola NFR-05 | Médio — requer expansão de conteúdo | **P2** |
| TD-009 | Processo | `data/` (metadados YAML do edital) proposto (ADR-004) mas não implementado | Baixo atualmente — viabiliza automação futura (nav, index, prompt vars) | Médio — criar 2 YAMLs + scripts de geração | **P3** |
| TD-010 | Testing | Scripts (validate.py, backfill.py) não têm testes automatizados próprios | Baixo — scripts são simples e output é diretamente verificável | Médio — pytest requer setup e fixtures de markdown | **P3** |
| TD-011 | Segurança | Actions pinadas por major version (`@v4`) em vez de SHA | Baixo — prática padrão, mas supply chain attack é risco teórico | Baixo — substituir por SHA | **P3** |
| TD-012 | Conteúdo | `os` importado mas não utilizado em backfill.py | Trivial — import não usado | Trivial — remover 1 linha | **P4** |

---

## Detalhamento das Dívidas Críticas

### TD-001 — Backfill Pendente (P0)

**Situação:** Os 80 resumos existentes NÃO possuem os campos `materia`, `concurso`, `data_geracao`, `modelo_llm` no frontmatter. Os 20 resumos de Economia têm título em formato descritivo. ~69 resumos não têm rodapé.

**Impacto:** O validate.py retorna 502 ERROs. Se o CI (deploy.yml) rodar com o validate.py step, TODO deploy será bloqueado.

**Resolução:** `python3 scripts/backfill.py --path docs/ --apply`. Comando único, resolve 418 dos 502 ERROs.

**Rastreabilidade:** RF-02, RF-03, RF-05, RF-06, RF-11, RF-38, RF-40, RF-41.

### TD-002 — Seções Conexões e Top 5 Ausentes (P1)

**Situação:**
- 20/20 resumos de Economia não possuem seção "Conexões com Outros Temas do Edital"
- 5/60 resumos de HM não possuem seção "Top 5"
- 5/60 resumos de HM não possuem seção "Conexões"

**Impacto:** Cada arquivo gera 1-2 ERROs no validate.py. Total: ~30 ERROs remanescentes pós-backfill. Viola RF-09 (seções invariantes) e a premissa AS-08.

**Resolução:** Requer intervenção humana ou geração via LLM:
- **Opção A**: Gerar conteúdo para as seções ausentes (usando LLM com prompt específico)
- **Opção B**: Rebaixar severidade dessas seções de ERRO para AVISO no validate.py para Economia (aceitar como adaptação da matéria)
- **Opção C**: Marcar como dívida aceita e remover do quality gate do CI

**Rastreabilidade:** RF-09, RF-10, RF-39, BR-007, BR-029.

### TD-003 — Admonitions Ausentes (P1)

**Situação:** 48/80 resumos não possuem admonition `!!! info "Temas do mesmo capítulo"`. Afeta tanto Economia (3 arquivos) quanto HM (45 arquivos).

**Impacto:** 48 ERROs no validate.py. Viola RF-08.

**Nota:** A contagem alta sugere que muitos resumos de HM também não têm a admonition, não apenas Economia. Isso não foi documentado nas inconsistências (BR-028 a BR-030) pelo Analista de Negócios — é um gap que emergiu na verificação.

**Resolução:** A admonition é mecânica (lista de temas irmãos do capítulo). Pode ser gerada por script a partir da estrutura de diretórios e do index.md de cada matéria. Considerar adicionar essa funcionalidade ao backfill.py.

**Rastreabilidade:** RF-08, BR-006.

---

## Classificação por Prioridade

| Prioridade | Dívidas | Ação |
|------------|---------|------|
| **P0 — Blocker** | TD-001 | Executar antes de qualquer deploy |
| **P1 — Alta** | TD-002, TD-003 | Resolver para viabilizar CI limpo |
| **P2 — Média** | TD-004, TD-006, TD-008 | Resolver no próximo ciclo de desenvolvimento |
| **P3 — Baixa** | TD-005, TD-007, TD-009, TD-010, TD-011 | Backlog — resolver quando oportuno |
| **P4 — Trivial** | TD-012 | Corrigir em qualquer commit |
