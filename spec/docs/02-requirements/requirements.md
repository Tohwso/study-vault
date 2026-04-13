# Requisitos do Sistema — Study Vault

> **Artefato RUP:** Especificação de Requisitos (Requisitos)
> **Proprietário:** [RUP] Analista de Requisitos
> **Status:** Complete
> **Última atualização:** Reverse-engineered from source code (2026-07-19)
>
> ⚠️ Requisitos foram INFERIDOS a partir da implementação existente e das regras de negócio documentadas. Requisitos marcados como "Novo" representam necessidades identificadas durante a análise que ainda não estão implementadas.

---

## Decisão Arquitetural de Requisitos

**Os requisitos são a FONTE DE VERDADE do projeto.** O prompt template (`scripts/prompts/summary.md`) é um artefato derivado que implementa os requisitos — não o contrário.

Essa inversão de dependência resolve um problema fundamental: na situação atual, o prompt funciona como "spec informal", o que impede rastreabilidade, versionamento de regras e extensibilidade controlada para novas matérias. Com os requisitos como fonte canônica:

- Alterações nas regras de conteúdo são feitas nos requisitos e propagadas ao template
- O template pode ter variantes por matéria sem divergir da spec
- QA pode verificar conformidade de resumos contra requisitos formais, não contra um prompt volátil

---

## 1. Requisitos Funcionais

### 1.1 Estrutura dos Resumos

| ID | Descrição | Fonte | Prioridade | Rastreabilidade |
|----|-----------|-------|------------|-----------------|
| RF-01 | Cada tema do edital deve produzir exatamente um arquivo markdown. Não é permitido split de um tema em múltiplos arquivos nem merge de temas em um único arquivo. | BR-001 | Must Have | spec/docs/01-business/business-rules.md |
| RF-02 | Todo resumo deve conter um bloco de **frontmatter YAML** como primeiro elemento do arquivo, delimitado por `---`, com os campos obrigatórios: `title`, `edital_ref`, `capitulo`, `status`, `materia`, `concurso`. | BR-002, BR-028 | Must Have | spec/docs/01-business/business-rules.md |
| RF-03 | O campo `title` do frontmatter deve seguir o formato padronizado: `"<ano> - <concurso> - <matéria> - <tema>"`. Ex: `"2026 - CACD - Economia - Demanda do Consumidor"`. Este formato aplica-se a **todas** as matérias. | BR-003, BR-028 | Must Have | Padronização cross-matéria (resolve inconsistência BR-028) |
| RF-04 | O campo `status` do frontmatter deve aceitar exatamente os valores: `completo`, `em_revisao`, `pendente`. | BR-004 | Must Have | spec/docs/01-business/business-rules.md |
| RF-05 | O frontmatter deve incluir um campo `data_geracao` no formato ISO 8601 (`YYYY-MM-DD`) registrando a data de geração do resumo. | BR-030 | Must Have | Resolve inconsistência BR-030 (rastreabilidade temporal) |
| RF-06 | O frontmatter deve incluir um campo `modelo_llm` registrando o identificador do modelo LLM usado na geração (ex: `claude-opus-4-6`, `gpt-4o`, `gemini-1.5-pro`). O rodapé do resumo deve exibir o nome legível do modelo. Este campo é **obrigatório** — todo resumo deve rastrear qual modelo o gerou. | UQ-001 (resolvida), UQ-006 (resolvida) | Must Have | Novo requisito do stakeholder |
| RF-07 | Todo resumo deve iniciar (após frontmatter e título H1) com um **metadata blockquote** (`>`) contendo: Concurso, Matéria, Capítulo, Referência no edital, Status. | BR-005 | Must Have | spec/docs/01-business/business-rules.md |
| RF-08 | Todo resumo deve conter um **admonition de temas irmãos** (`!!! info "Temas do mesmo capítulo"`) listando todos os demais temas do mesmo capítulo, com numeração CC.TT. | BR-006 | Must Have | spec/docs/01-business/business-rules.md |
| RF-09 | Todo resumo deve conter as **5 seções obrigatórias**, nesta ordem: (1) Contexto e Periodização, (2) Desenvolvimento, (3) Interpretações e Debates, (4) Conexões com Outros Temas do Edital, (5) 🎯 Top 5 — O que mais cai no {concurso}. | BR-007, BR-029 | Must Have | Padronização cross-matéria (resolve inconsistência BR-029) |
| RF-10 | Para matérias de natureza analítica/quantitativa (Economia, Direito), é permitida a organização interna das seções Contexto, Desenvolvimento e Interpretações por **subseções temáticas numeradas** (ex: `## 1. Preferências do Consumidor`), desde que a seção "Conexões" e "Top 5" permaneçam como seções finais obrigatórias com seus nomes padronizados. | BR-029, BR-027 | Should Have | Resolve inconsistência BR-029 com flexibilidade controlada |
| RF-11 | Todo resumo deve terminar com um **rodapé** de uma linha: `*Gerado por IA ({modelo_llm}). Sujeito a revisão.*` | BR-020, RF-06 | Must Have | Novo — combina disclaimer de IA com rastreabilidade de modelo |
| RF-12 | Termos técnicos e nomes próprios devem ser formatados em **negrito** (`**termo**`). | BR-009 | Must Have | spec/docs/01-business/business-rules.md |
| RF-13 | Datas e periodizações devem ser **precisas** — anos e datas específicas, não séculos ou décadas vagas. | BR-010 | Must Have | spec/docs/01-business/business-rules.md |
| RF-14 | Autores de referência da área devem ser **citados com suas teses principais**, incluindo obra e ano quando conhecidos. | BR-011 | Must Have | spec/docs/01-business/business-rules.md |
| RF-15 | Quando houver debate historiográfico, teórico ou interpretativo, o resumo deve apresentar as **principais correntes**, não uma única visão. Deve incluir autores-chave e suas posições. | BR-012 | Must Have | spec/docs/01-business/business-rules.md |
| RF-16 | A seção "Top 5" deve incluir um **disclaimer explícito** de que os tópicos listados são baseados na percepção do modelo de IA sobre o padrão histórico de cobrança, **não** em análise estatística factual de provas anteriores. | UQ-005 (resolvida) | Must Have | Transparência ao leitor — projeto público |

### 1.2 Convenções de Naming e Organização

| ID | Descrição | Fonte | Prioridade | Rastreabilidade |
|----|-----------|-------|------------|-----------------|
| RF-17 | Nome de arquivo de resumo segue o formato: `CC-TT-slug-do-tema.md`, onde `CC` = capítulo (2 dígitos zero-padded), `TT` = tema (2 dígitos zero-padded), slug em kebab-case sem acentos. | BR-013 | Must Have | spec/docs/01-business/business-rules.md |
| RF-18 | Cada matéria ocupa um diretório próprio em `docs/`, com nome em kebab-case sem acentos: `docs/historia-mundial/`, `docs/economia/`, `docs/historia-do-brasil/`, etc. | BR-014 | Must Have | spec/docs/01-business/business-rules.md |
| RF-19 | Cada matéria deve possuir um arquivo de índice `index.md` no seu diretório, contendo: metadata blockquote (concurso, fase, total de capítulos/temas), tabela por capítulo com links e status de cada tema, e seção de progresso. | BR-015 | Must Have | spec/docs/01-business/business-rules.md |
| RF-20 | A hierarquia de navegação no `mkdocs.yml` deve espelhar a estrutura `Matéria > Capítulo > Tema`, seguindo a numeração do edital. | BR-016 | Must Have | spec/docs/01-business/business-rules.md |
| RF-21 | Todo resumo adicionado ao repositório deve ter entrada correspondente no `nav` do `mkdocs.yml` antes do push. | BR-017 | Must Have | spec/docs/01-business/business-rules.md |

### 1.3 Qualidade do Conteúdo

| ID | Descrição | Fonte | Prioridade | Rastreabilidade |
|----|-----------|-------|------------|-----------------|
| RF-22 | A extensão de cada resumo deve estar entre **2.000 e 4.000 palavras**. Resumos fora dessa faixa devem ser marcados com `status: em_revisao` até ajuste. | BR-008 | Must Have | spec/docs/01-business/business-rules.md |
| RF-23 | O conteúdo deve ser baseado na **bibliografia de referência do edital** para a matéria. Informações que ultrapassem a bibliografia devem ser apresentadas como complementares, não como núcleo do resumo. | BR-018 | Must Have | spec/docs/01-business/business-rules.md |
| RF-24 | O formato markdown deve usar `##` para seções, `###` para subseções, `>` para citações de documentos/trechos relevantes, `!!! note/warning/tip` para observações especiais. | Prompt template | Must Have | scripts/prompts/summary.md |
| RF-25 | Para matérias quantitativas (Economia), fórmulas matemáticas devem ser renderizadas via **MathJax/LaTeX** (notação `$$...$$` ou `$...$`), nunca como texto plano ou imagem. | BR-021 | Must Have | spec/docs/01-business/business-rules.md |
| RF-26 | Diagramas Mermaid (```` ```mermaid ````) podem ser usados quando a representação visual agregar ao entendimento (cronologias, fluxos, relações). | mkdocs.yml (pymdownx.superfences) | Could Have | Inferido da configuração existente |

### 1.4 Pipeline e Publicação

| ID | Descrição | Fonte | Prioridade | Rastreabilidade |
|----|-----------|-------|------------|-----------------|
| RF-27 | O prompt template é a **implementação executável** dos requisitos de conteúdo. Deve ser mantido em `scripts/prompts/` e versionado no repositório. Ajustes de regras de conteúdo devem ser originados nos requisitos e propagados ao template. | BR-019 | Must Have | spec/docs/01-business/business-rules.md |
| RF-28 | O prompt template deve ser **parametrizado** com as variáveis: `{concurso}`, `{materia}`, `{capitulo}`, `{tema}`, `{subtemas_irmaos}`, `{bibliografia}`. | BR-019, Prompt template | Must Have | scripts/prompts/summary.md |
| RF-29 | Quando uma matéria requerer ajustes significativos no prompt (ex: Economia requer MathJax, Direito requer citação de artigos legais), deve ser criada uma **variante do template** em `scripts/prompts/summary-{materia}.md`, documentando as diferenças em relação ao template base. | BR-027 | Should Have | spec/docs/01-business/business-rules.md |
| RF-30 | O deploy é acionado automaticamente a cada push em `main` via GitHub Actions workflow `deploy.yml`. | BR-022 | Must Have | spec/docs/01-business/business-rules.md |
| RF-31 | O workflow de deploy deve usar Python 3.12 e instalar `mkdocs-material` como dependência principal. | BR-023 | Must Have | spec/docs/01-business/business-rules.md |
| RF-32 | O aviso de que o conteúdo é **gerado por IA** deve estar visível na página inicial do site (`docs/index.md`) de forma proeminente, incluindo a informação de que múltiplos modelos LLM são utilizados. | BR-020 | Must Have | Projeto público |
| RF-33 | Todo resumo gerado deve passar por um **checklist de conformidade pós-geração** antes de ser commitado. O checklist deve verificar: (a) frontmatter completo com todos os campos obrigatórios, (b) presença das 5 seções, (c) extensão dentro da faixa 2.000–4.000 palavras, (d) metadata blockquote presente, (e) admonition de temas irmãos presente, (f) rodapé com disclaimer e modelo LLM, (g) formatação markdown limpa. | BR-025 | Should Have | Novo — resolve ausência de revisão formal |
| RF-34 | A página inicial (`docs/index.md`) deve conter a **tabela de matérias** com: nome da matéria (link), número de capítulos, número de temas, status geral (Completo/Em andamento/Planejada). | Observado em index.md atual | Must Have | Inferido da implementação |

### 1.5 Extensibilidade

| ID | Descrição | Fonte | Prioridade | Rastreabilidade |
|----|-----------|-------|------------|-----------------|
| RF-35 | O processo de adição de nova matéria deve seguir uma **checklist de onboarding** documentada: (1) consultar programa do edital, (2) criar diretório em `docs/`, (3) criar `index.md` com tabela de capítulos/temas, (4) levantar bibliografia de referência, (5) avaliar necessidade de variante do prompt, (6) adicionar matéria ao `nav` do `mkdocs.yml`, (7) atualizar tabela de matérias no `docs/index.md`. | BR-026, BP-01 | Must Have | spec/docs/01-business/business-processes.md |
| RF-36 | A estrutura de diretórios, naming, frontmatter e seções obrigatórias deve ser **idêntica** para todas as matérias. A flexibilidade permitida limita-se à organização interna das seções de conteúdo (RF-10) e à variante do prompt template (RF-29). | BR-028, BR-029 | Must Have | Padronização cross-matéria |
| RF-37 | Para cada nova matéria planejada (História do Brasil, Português, Geografia, Política Internacional, Direito), o `index.md` da matéria deve ser criado com **todos os temas do edital** listados e status `pendente`, antes de iniciar a geração de qualquer resumo. | BR-015, BP-01 | Should Have | Garantir cobertura completa antes da geração |

### 1.6 Padronização Cross-Matéria (Resolução de Inconsistências)

| ID | Descrição | Fonte | Prioridade | Rastreabilidade |
|----|-----------|-------|------------|-----------------|
| RF-38 | Os resumos existentes de Economia que usam título descritivo no frontmatter (ex: `"Demanda do Consumidor: Preferências, Equilíbrio e Elasticidade"`) devem ser **atualizados** para o formato padronizado `"2026 - CACD - Economia - <tema>"`. | BR-028 | Should Have | Resolve inconsistência BR-028 |
| RF-39 | Os resumos existentes de Economia que não possuem seções nomeadas "Conexões" e "Top 5" como seções finais devem ser **verificados e ajustados** para que as duas últimas seções sigam a nomenclatura padronizada conforme RF-09. | BR-029 | Should Have | Resolve inconsistência BR-029 |
| RF-40 | Todos os resumos existentes devem receber os campos `data_geracao` e `modelo_llm` no frontmatter. Para resumos já gerados cujo modelo e data não são conhecidos com precisão, usar `data_geracao: 2026-04-01` (data aproximada) e `modelo_llm: desconhecido`. | BR-030, RF-05, RF-06 | Should Have | Resolve inconsistência BR-030 + Novo requisito |
| RF-41 | Os resumos existentes de Economia que não possuem o **rodapé** `*Gerado por IA. Sujeito a revisão.*` devem receber o rodapé padronizado conforme RF-11. | Observado na comparação HM vs Economia | Should Have | Padronização cross-matéria |

---

## 2. Requisitos Não Funcionais

### 2.1 Performance e Usabilidade

| ID | Categoria | Descrição | Métrica | Meta |
|----|-----------|-----------|---------|------|
| NFR-01 | Usabilidade | O leitor deve conseguir localizar qualquer tema em no máximo 3 cliques a partir da home do site. | Cliques para acesso a qualquer resumo | ≤ 3 (Home → Matéria → Capítulo/Tema) |
| NFR-02 | Usabilidade | Busca full-text deve retornar resultados relevantes para termos e conceitos presentes nos resumos. | Cobertura de busca | 100% dos termos em negrito indexáveis |
| NFR-03 | Performance | O site deve carregar qualquer página em tempo aceitável. | Tempo de carregamento | < 3s em conexão 4G |
| NFR-04 | Usabilidade | O site deve ser navegável em dispositivos móveis (responsividade do tema Material). | Breakpoints | Todas as resoluções ≥ 320px |

### 2.2 Qualidade do Conteúdo

| ID | Categoria | Descrição | Métrica | Meta |
|----|-----------|-----------|---------|------|
| NFR-05 | Qualidade | Cada resumo deve conter entre 2.000 e 4.000 palavras. | Word count | 2.000 ≤ WC ≤ 4.000 |
| NFR-06 | Qualidade | Nenhum resumo pode ter seções obrigatórias ausentes. | Conformidade estrutural | 100% dos resumos com 5 seções |
| NFR-07 | Qualidade | Todos os frontmatters devem conter todos os campos obrigatórios. | Conformidade de metadados | 100% dos campos preenchidos |
| NFR-08 | Qualidade | Consistência terminológica: o mesmo conceito deve usar o mesmo termo em todos os resumos de uma matéria. | Divergência de termos | 0 variações não intencionais |

### 2.3 Manutenibilidade e Extensibilidade

| ID | Categoria | Descrição | Métrica | Meta |
|----|-----------|-----------|---------|------|
| NFR-09 | Extensibilidade | Adicionar uma nova matéria ao projeto deve ser possível seguindo o checklist (RF-35) sem alterar nenhum código ou configuração além de `mkdocs.yml` e `docs/`. | Esforço de onboarding | ≤ 1 hora para setup da matéria (sem contar geração de resumos) |
| NFR-10 | Manutenibilidade | Os requisitos, o prompt template e os resumos devem ser versionados no mesmo repositório Git. | Rastreabilidade | 100% artefatos no Git |
| NFR-11 | Manutenibilidade | Alterações em requisitos de conteúdo devem ser refletidas no prompt template antes de gerar novos resumos. | Consistência spec↔template | 0 requisitos não-propagados |

### 2.4 Disponibilidade e Deploy

| ID | Categoria | Descrição | Métrica | Meta |
|----|-----------|-----------|---------|------|
| NFR-12 | Disponibilidade | O site deve estar acessível 24/7 via GitHub Pages. | Uptime | ≥ 99.5% (SLA do GitHub Pages) |
| NFR-13 | Deploy | O tempo entre push em `main` e atualização do site publicado deve ser inferior a 5 minutos. | Tempo de deploy | < 5 min |
| NFR-14 | Deploy | Build failures devem ser detectáveis pelo Autor via status do GitHub Actions. | Observabilidade | 100% dos builds com status visível |

### 2.5 Acessibilidade e Transparência (Projeto Público)

| ID | Categoria | Descrição | Métrica | Meta |
|----|-----------|-----------|---------|------|
| NFR-15 | Transparência | O site deve informar claramente na home que o conteúdo é gerado por IA e não substitui a leitura da bibliografia. | Presença de disclaimer | Visível sem scroll na home |
| NFR-16 | Transparência | Cada resumo deve informar no rodapé o modelo LLM usado na geração. | Rastreabilidade individual | 100% dos resumos com modelo identificado |
| NFR-17 | Acessibilidade | O site deve usar contraste adequado e hierarquia tipográfica clara (garantido pelo tema Material). | WCAG AA | Contraste ≥ 4.5:1 |
| NFR-18 | Transparência | A seção "Top 5" deve conter disclaimer de que é baseada em percepção da LLM, não em análise factual. | Presença de disclaimer | 100% das seções Top 5 |

---

## 3. Regras de Negócio (Referência e Interpretação)

Esta seção referencia as regras definidas em `spec/docs/01-business/business-rules.md` e adiciona a **interpretação sistêmica** — como cada regra se traduz em comportamento do pipeline.

### 3.1 Regras de Estrutura (BR-001 a BR-012)

| BR | Interpretação Sistêmica | RFs Relacionados |
|----|-------------------------|------------------|
| BR-001 | Mapeamento 1:1 tema→arquivo é invariante do sistema. Qualquer ferramenta de validação deve detectar duplicidade ou ausência. | RF-01 |
| BR-002 | Frontmatter é contrato máquina-máquina. Campos obrigatórios expandidos (RF-02) em relação ao observado originalmente. | RF-02, RF-05, RF-06 |
| BR-003 | Formato de título padronizado é contrato cross-matéria. Economia deve convergir para o padrão de HM. | RF-03, RF-38 |
| BR-004 | Ciclo de vida do resumo controlado via `status`. `completo` não significa "revisado formalmente" — significa que o Autor considera pronto para uso (AS-05). | RF-04 |
| BR-005 | Metadata blockquote é contrato humano-humano (legibilidade). Redundante com frontmatter por design. | RF-07 |
| BR-006 | Admonition de temas irmãos implementa navegação lateral entre conteúdos correlatos. | RF-08 |
| BR-007 | As 5 seções são o esqueleto do resumo. Para matérias analíticas, organização interna é flexível (RF-10), mas Conexões e Top 5 são invariantes. | RF-09, RF-10 |
| BR-008 | Faixa de 2.000–4.000 palavras é controle de qualidade de extensão. Abaixo: superficial. Acima: perde caráter de resumo. | RF-22 |
| BR-009 | Negrito em termos técnicos melhora scannability durante revisão rápida. | RF-12 |
| BR-010 | Precisão temporal é requisito do concurso. LLMs tendem a generalizar — o prompt deve reforçar esse ponto. | RF-13 |
| BR-011 | Citação de autores é diferencial do CACD em relação a outros concursos. A banca cobra conhecimento historiográfico/teórico. | RF-14 |
| BR-012 | Pluralidade interpretativa evita viés. Essencial para a segunda fase (discursiva). | RF-15 |

### 3.2 Regras de Naming (BR-013 a BR-017)

| BR | Interpretação Sistêmica | RFs Relacionados |
|----|-------------------------|------------------|
| BR-013 | Formato `CC-TT-slug.md` garante ordenação natural no filesystem e previsibilidade de paths. | RF-17 |
| BR-014 | Diretório por matéria garante isolamento e simplicidade de navegação. | RF-18 |
| BR-015 | `index.md` é o dashboard de progresso de cada matéria. | RF-19 |
| BR-016 | O `nav` do `mkdocs.yml` é a materialização da hierarquia do edital no site. | RF-20 |
| BR-017 | Entrada no `nav` é pré-condição para visibilidade no site. Operação manual — risco de esquecimento. | RF-21 |

### 3.3 Regras de Qualidade (BR-018 a BR-021)

| BR | Interpretação Sistêmica | RFs Relacionados |
|----|-------------------------|------------------|
| BR-018 | Confiabilidade factual é o requisito de maior risco. A LLM pode gerar informações plausíveis mas incorretas. Mitigação: bibliografia no prompt + disclaimer público. | RF-23, NFR-15 |
| BR-019 | Prompt como implementação dos requisitos. **Inversão de dependência:** o prompt não define regras — implementa-as. | RF-27 |
| BR-020 | Disclaimer de IA é requisito ético e de reputação, especialmente com projeto público. | RF-32, NFR-15 |
| BR-021 | MathJax é extensão habilitada no mkdocs.yml. Matérias qualitativas não a usam. | RF-25 |

### 3.4 Regras de Pipeline (BR-022 a BR-025)

| BR | Interpretação Sistêmica | RFs Relacionados |
|----|-------------------------|------------------|
| BR-022 | Deploy automático via push em `main`. Zero staging. | RF-30 |
| BR-023 | Dependência mínima (mkdocs-material). | RF-31 |
| BR-024 | Sem branch de staging = sem safety net antes de produção. Aceitável para site de estudo pessoal, mas risco aumenta com projeto público. | RF-30 |
| BR-025 | Ausência de revisão formal é o **maior gap** do pipeline. RF-33 endereça isso com checklist pós-geração. | RF-33 |

### 3.5 Regras de Extensibilidade (BR-026 a BR-027)

| BR | Interpretação Sistêmica | RFs Relacionados |
|----|-------------------------|------------------|
| BR-026 | Processo de onboarding de matéria é multistep e manual. RF-35 formaliza como checklist. | RF-35 |
| BR-027 | Variantes de template por matéria são esperadas. Devem ser versionadas e rastreáveis. | RF-29 |

### 3.6 Inconsistências Observadas (BR-028 a BR-030)

| BR | Diagnóstico | Ação Prescrita | RFs Relacionados |
|----|-------------|----------------|------------------|
| BR-028 | Formato de `title` no frontmatter diverge entre HM (com prefixo ano/concurso) e Economia (descritivo). | Padronizar para o formato com prefixo em todas as matérias. Migrar resumos existentes. | RF-03, RF-38 |
| BR-029 | Resumos de Economia usam seções numeradas (`## 1.`, `## 2.`) em vez das 5 seções nomeadas de HM. | Permitir organização interna flexível para matérias analíticas, mas exigir "Conexões" e "Top 5" como seções finais invariantes. | RF-09, RF-10, RF-39 |
| BR-030 | Ausência de `data_geracao` e `modelo_llm` no frontmatter impossibilita rastreabilidade temporal e por modelo. | Adicionar ambos os campos como obrigatórios. Backfill de resumos existentes com valores aproximados. | RF-05, RF-06, RF-40 |

---

## 4. Matriz de Rastreabilidade — Requisitos × Objetivos de Negócio

| Objetivo | RFs que implementam |
|----------|---------------------|
| BG-01 (Cobertura completa do edital) | RF-01, RF-19, RF-37 |
| BG-02 (Densidade e qualidade) | RF-09, RF-10, RF-12, RF-13, RF-14, RF-15, RF-22, RF-23 |
| BG-03 (Navegabilidade) | RF-08, RF-17, RF-18, RF-19, RF-20, RF-21, NFR-01 |
| BG-04 (Busca transversal) | RF-12, NFR-02 |
| BG-05 (Reprodutibilidade do pipeline) | RF-27, RF-28, RF-29, RF-33, RF-35, RF-36 |
| BG-06 (Publicação automática) | RF-30, RF-31, NFR-13 |
| BG-07 (Extensibilidade para outros concursos) | RF-03, RF-28, RF-29, RF-35, RF-36, NFR-09 |
