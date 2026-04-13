# Regras de Negócio — Study Vault

> **Artefato RUP:** Regras de Negócio (Modelagem de Negócios)
> **Proprietário:** [RUP] Analista de Negócios
> **Status:** Complete
> **Última atualização:** Reverse-engineered from source code (2026-07-19)
>
> ⚠️ Este artefato foi INFERIDO a partir da análise da implementação existente. Pode não refletir integralmente a intenção original do criador.

---

## 1. Regras de Estrutura do Conteúdo

Regras que governam o formato e a composição de cada resumo.

| ID | Regra | Classificação | Fonte | Impacto se violada |
|----|-------|---------------|-------|---------------------|
| BR-001 | Cada tema do edital produz **exatamente um arquivo markdown**. Não há split de um tema em múltiplos arquivos nem merge de temas em um único arquivo. | Operacional | Convenção do projeto | Quebra a rastreabilidade tema↔arquivo e a navegação |
| BR-002 | Todo resumo deve conter **frontmatter YAML** com os campos obrigatórios: `title`, `edital_ref`, `capitulo`, `status`. | Operacional | Observado em 100% dos arquivos existentes | Metadados ausentes impossibilitam indexação e rastreabilidade |
| BR-003 | O campo `title` do frontmatter segue o formato: `"<ano> - <concurso> - <matéria> - <tema>"`. | Operacional | Observado em resumos de História Mundial | Inconsistência no padrão de títulos entre matérias (ver BR-028) |
| BR-004 | O campo `status` do frontmatter aceita os valores: `completo`, `em_revisao`, `pendente`. | Operacional | Inferido dos arquivos existentes (todos `completo`) | Sem controle de ciclo de vida do conteúdo |
| BR-005 | Todo resumo deve iniciar com um **metadata blockquote** (`>`) contendo: Concurso, Matéria, Capítulo, Referência no edital, Status. | Operacional | Observado em 100% dos arquivos | Leitor perde contexto imediato sobre qual tema está lendo |
| BR-006 | Todo resumo deve conter um **admonition de temas irmãos** (`!!! info "Temas do mesmo capítulo"`) listando os demais temas do capítulo. | Operacional | Observado em 100% dos arquivos | Perde-se a navegação lateral entre temas correlatos |
| BR-007 | Todo resumo deve conter as **5 seções obrigatórias**, na seguinte ordem: (1) Contexto e Periodização, (2) Desenvolvimento, (3) Interpretações e Debates, (4) Conexões, (5) Top 5 — O que mais cai no CACD. | Operacional | Definido no prompt template (`scripts/prompts/summary.md`) | Quebra a uniformidade estrutural; dificulta revisão comparativa |
| BR-008 | A extensão-alvo de cada resumo é de **2.000 a 4.000 palavras**. | Operacional | Definido no prompt template | Abaixo de 2.000: superficial. Acima de 4.000: perde o caráter de "resumo" |
| BR-009 | Termos técnicos e nomes próprios devem ser formatados em **negrito** (`**termo**`). | Operacional | Definido no prompt template | Reduz a scannability do texto durante revisão rápida |
| BR-010 | Datas e periodizações devem ser **precisas** (anos, não séculos vagos). | Operacional | Definido no prompt template | Informação imprecisa não serve para concurso objetivo |
| BR-011 | Autores de referência devem ser **citados com suas teses principais**. | Operacional | Definido no prompt template | O CACD cobra conhecimento historiográfico, não apenas factual |
| BR-012 | Quando houver debate historiográfico, o resumo deve apresentar as **principais correntes interpretativas** — não apenas uma visão. | Operacional | Definido no prompt template | Visão unilateral pode levar a erro na prova (a banca cobra análise) |

---

## 2. Regras de Naming e Organização

Regras que governam a nomeação de arquivos e a estrutura de diretórios.

| ID | Regra | Classificação | Fonte | Impacto se violada |
|----|-------|---------------|-------|---------------------|
| BR-013 | Nome de arquivo segue o formato: `CC-TT-slug-do-tema.md`, onde `CC` = capítulo (2 dígitos zero-padded), `TT` = tema (2 dígitos zero-padded), e slug em kebab-case. | Operacional | Observado em 100% dos arquivos | Quebra a ordenação alfabética natural e a previsibilidade dos paths |
| BR-014 | Cada matéria ocupa um **diretório próprio** em `docs/`: `docs/historia-mundial/`, `docs/economia/`, etc. O nome do diretório é em kebab-case, sem acentos. | Operacional | Observado na estrutura existente | Conflito de paths, navegação quebrada |
| BR-015 | Cada matéria possui um **arquivo de índice** (`index.md`) que lista todos os capítulos e temas com links e status. | Operacional | Observado para História Mundial e Economia | Sem visão geral do progresso da matéria |
| BR-016 | A hierarquia de navegação no `mkdocs.yml` deve espelhar a estrutura `Matéria > Capítulo > Tema`, seguindo a numeração do edital. | Operacional | Observado no `mkdocs.yml` | Navegação no site fica inconsistente com o edital |
| BR-017 | Cada novo resumo adicionado deve ter sua entrada correspondente no `nav` do `mkdocs.yml`. | Operacional | Inferido (sem automação) | Resumo existe no repositório mas não aparece no site |

---

## 3. Regras de Qualidade do Conteúdo

Regras sobre a qualidade esperada do conteúdo gerado.

| ID | Regra | Classificação | Fonte | Impacto se violada |
|----|-------|---------------|-------|---------------------|
| BR-018 | O conteúdo deve ser **factualmente confiável**, baseado na bibliografia de referência do edital. | Controle Interno | Definido no prompt template (variável `{bibliografia}`) | Internalização de informações incorretas — alto risco para o candidato |
| BR-019 | O prompt template é a **fonte canônica** de regras de conteúdo. Alterações nas regras de geração devem ser feitas no template, não ad hoc durante a execução. | Controle Interno | Decisão de projeto (centralizar regras) | Divergência entre resumos gerados em momentos diferentes |
| BR-020 | O aviso de que o conteúdo é **gerado por IA** deve estar visível na home do site (`docs/index.md`). | Controle Interno | Observado no `index.md` ("Gerado com auxílio de IA") | Questão ética: leitor pode não saber que o conteúdo é sintético |
| BR-021 | Para matérias quantitativas (Economia), fórmulas devem ser renderizadas via **MathJax/LaTeX**, não como texto ou imagem. | Operacional | Observado nos resumos de Economia (configuração MathJax em `mkdocs.yml`) | Fórmulas ilegíveis ou não-copiáveis |

---

## 4. Regras de Pipeline e Publicação

Regras que governam o processo de geração e publicação.

| ID | Regra | Classificação | Fonte | Impacto se violada |
|----|-------|---------------|-------|---------------------|
| BR-022 | O deploy é acionado **automaticamente** a cada push em `main` via GitHub Actions. | Operacional | Observado em `.github/workflows/deploy.yml` | Conteúdo publicado não reflete o estado do repositório |
| BR-023 | O workflow de deploy usa **Python 3.12** e instala apenas `mkdocs-material` (que traz MkDocs como dependência). | Operacional | Observado no workflow | Build falha se dependências mudarem |
| BR-024 | O branch principal é `main`. Não há branch de staging ou preview. | Operacional | Inferido da configuração do workflow | Todo push em `main` vai direto para produção |
| BR-025 | Não há **processo formal de revisão** dos resumos antes da publicação. O Autor lê e ajusta manualmente quando identifica problemas. | Controle Interno | Inferido (ausência de checklist ou fluxo de aprovação) | Erros factuais ou estruturais podem chegar à versão publicada |

---

## 5. Regras de Extensibilidade

Regras para adição de novas matérias e temas.

| ID | Regra | Classificação | Fonte | Impacto se violada |
|----|-------|---------------|-------|---------------------|
| BR-026 | Para adicionar uma nova matéria, é necessário: (1) criar o diretório em `docs/`, (2) criar `index.md` com a listagem de capítulos/temas, (3) gerar cada resumo usando o prompt template ajustado para a matéria, (4) adicionar a matéria ao `nav` do `mkdocs.yml`, (5) atualizar a tabela de status na home. | Operacional | Inferido do padrão observado em História Mundial e Economia | Matéria incompleta ou não-navegável |
| BR-027 | O prompt template pode necessitar de **ajustes por matéria** (ex: "regras de conteúdo" diferentes para Direito vs. História). O template atual é otimizado para História Mundial. | Operacional | Declarado nas "Notas de uso" do prompt template | Resumos de matérias distintas gerados com regras inadequadas |

---

## 6. Inconsistências Observadas

| ID | Observação | Evidência | Impacto |
|----|------------|-----------|---------|
| BR-028 | O formato do `title` no frontmatter **varia entre matérias**: em História Mundial usa `"2026 - CACD - História Mundial - <tema>"`, em Economia usa formato descritivo sem prefixo de ano/concurso (ex: `"Demanda do Consumidor: Preferências, Equilíbrio e Elasticidade"`). | Comparação entre `01-05-crise-de-1929-e-new-deal.md` e `01-01-demanda-do-consumidor.md` | Inconsistência que dificulta busca e indexação padronizada |
| BR-029 | A seção "Top 5" em resumos de Economia pode não ter o sufixo "no CACD" — os resumos de Economia observados usam numeração genérica de seções (`## 1.`, `## 2.`) em vez das 5 seções nomeadas. | Observado em `economia/01-01-demanda-do-consumidor.md` | A estrutura de 5 seções (BR-007) não é estritamente seguida em Economia — a matéria pede organização diferente |
| BR-030 | Não existe campo de **data de geração** no frontmatter — não é possível saber quando cada resumo foi gerado nem com qual versão da LLM. | Ausência em todos os frontmatters | Impossibilita rastreabilidade temporal e avaliação de envelhecimento do conteúdo |
