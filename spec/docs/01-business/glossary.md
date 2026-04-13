# Glossário — Study Vault

> **Artefato RUP:** Glossário (Modelagem de Negócios)
> **Proprietário:** [RUP] Analista de Negócios
> **Status:** Complete
> **Última atualização:** Reverse-engineered from source code (2026-07-19)
>
> ⚠️ Este artefato foi INFERIDO a partir da análise da implementação existente. Pode não refletir integralmente a intenção original do criador.

---

## 1. Termos do Domínio — Concurso e Edital

| Termo | Definição | Contexto |
|-------|-----------|----------|
| **CACD** | Concurso de Admissão à Carreira de Diplomata, organizado pelo CESPE/CEBRASPE para o Ministério das Relações Exteriores (MRE/Itamaraty). Um dos concursos mais difíceis do Brasil. | O concurso-alvo da primeira implementação do Study Vault. |
| **Edital** | Documento oficial que define o programa do concurso: matérias, capítulos, temas e bibliografia de referência. Fonte primária para a organização do conteúdo. | O edital determina a árvore de conteúdo (`matéria > capítulo > tema`). |
| **Matéria** | Disciplina do edital (ex: História Mundial, Economia, Direito Internacional, Política Internacional). Cada matéria corresponde a um diretório em `docs/`. | Atualmente 2 matérias cobertas: História Mundial (60 temas) e Economia (24 temas). |
| **Capítulo** | Agrupamento de temas dentro de uma matéria, numerado sequencialmente (ex: "1. Estruturas e Ideias Econômicas"). Corresponde a uma seção no `nav` do `mkdocs.yml`. | Os capítulos seguem exatamente a numeração do edital. |
| **Tema** | Unidade atômica de conteúdo — cada tema do edital gera exatamente um arquivo markdown. Identificado por `CC.TT` (capítulo.tema). | Mapeamento 1:1 entre tema do edital e arquivo `.md`. |
| **Referência no edital** (`edital_ref`) | Numeração oficial do tema no programa do edital, registrada no frontmatter de cada resumo (ex: `1.5`, `3.12`). | Usada para rastreabilidade entre conteúdo gerado e programa oficial. |
| **Primeira Fase** | Etapa objetiva do CACD (questões de múltipla escolha). Os resumos são dimensionados prioritariamente para esta fase. | Define a extensão-alvo dos resumos (2.000–4.000 palavras). |
| **Segunda Fase** | Etapa discursiva do CACD (redações e questões dissertativas). Exige maior profundidade e debate historiográfico/teórico. | Mencionada no prompt como extensão futura — resumos atuais são insuficientes para esta fase. |
| **Bibliografia de referência** | Lista de obras acadêmicas indicadas no edital para cada matéria. Alimenta a variável `{bibliografia}` do prompt template. | Determina a base teórica e os autores que devem ser citados nos resumos. |

---

## 2. Termos do Domínio — Estrutura do Conteúdo

| Termo | Definição | Contexto |
|-------|-----------|----------|
| **Resumo denso** | Documento markdown de 2.000–4.000 palavras que sintetiza um tema do edital em formato estruturado de 5 seções. Não é fichamento nem resenha — é conteúdo autossuficiente para revisão. | Produto central do Study Vault. |
| **Frontmatter YAML** | Bloco de metadados no início de cada arquivo markdown, delimitado por `---`. Contém: `title`, `edital_ref`, `capitulo`, `status`. | Permite indexação, navegação e rastreabilidade. |
| **Metadata blockquote** | Bloco `>` abaixo do frontmatter que exibe concurso, matéria, capítulo, referência no edital e status de forma legível para o leitor. | Redundante com o frontmatter (este é para humanos, o frontmatter para máquinas). |
| **Admonition de temas irmãos** | Bloco `!!! info "Temas do mesmo capítulo"` que lista todos os temas do mesmo capítulo, permitindo ao leitor navegar entre conteúdos correlatos. | Alimentado pela variável `{subtemas_irmaos}` do prompt. |
| **Seção "Contexto e Periodização"** | Primeira seção obrigatória do resumo. Situa o tema no tempo e espaço: quando, onde, por quê. | Presente em todos os resumos de História Mundial. Adaptada em Economia como "Contexto". |
| **Seção "Desenvolvimento"** | Segunda seção — o conteúdo substantivo: conceitos, eventos, processos, atores, teorias. | Seção mais extensa de cada resumo. |
| **Seção "Interpretações e Debates"** | Terceira seção — apresenta correntes historiográficas, debates teóricos e posições divergentes sobre o tema. | Crítica para o CACD, que cobra capacidade de análise, não apenas memorização. |
| **Seção "Conexões"** | Quarta seção — relaciona o tema com outros pontos do edital, promovendo visão integrada. | Diferencial do material: conecta temas que em livros são tratados isoladamente. |
| **Seção "Top 5"** | Quinta seção — "🎯 Top 5 — O que mais cai no CACD". Os cinco pontos mais recorrentes nas provas, baseados no padrão histórico de cobrança. | Foco prático: direciona a revisão para o que tem maior probabilidade de cair. |
| **Convenção de naming** | Formato dos nomes de arquivo: `CC-TT-slug-do-tema.md` onde `CC` = capítulo (2 dígitos), `TT` = tema (2 dígitos), seguido de slug descritivo em kebab-case. | Ex: `01-05-crise-de-1929-e-new-deal.md` = Capítulo 01, Tema 05. |
| **Título do frontmatter** | Formato: `"<ano> - <concurso> - <matéria> - <tema>"`. Ex: `"2026 - CACD - História Mundial - As crises e os mecanismos anticrise"`. | Padronizado para indexação e identificação única. |

---

## 3. Termos do Domínio — Pipeline e Ferramentas

| Termo | Definição | Contexto |
|-------|-----------|----------|
| **Prompt template** | Arquivo `scripts/prompts/summary.md` que define o prompt parametrizado enviado à LLM para gerar cada resumo. Contém variáveis (`{concurso}`, `{materia}`, `{capitulo}`, `{tema}`, `{subtemas_irmaos}`, `{bibliografia}`), regras de conteúdo, estrutura esperada e formato. | Template único por matéria (com ajustes menores) — garante uniformidade entre resumos. |
| **LLM (Large Language Model)** | Modelo de linguagem de grande porte usado para gerar os resumos. O prompt é executado manualmente (não há automação via API). | A LLM é um ator de sistema — não é um stakeholder, é uma ferramenta. |
| **MkDocs** | Gerador de sites estáticos baseado em Python que transforma arquivos markdown em site HTML com navegação, busca e tema visual. | Framework que publica o Study Vault como site navegável. |
| **MkDocs Material** | Tema premium para MkDocs que fornece design responsivo, dark/light mode, busca aprimorada, admonitions, tabs, diagramas Mermaid e suporte a MathJax. | `theme.name: material` no `mkdocs.yml`. |
| **GitHub Pages** | Serviço de hospedagem estática do GitHub. O site é publicado automaticamente a cada push em `main`. | Deploy target — zero custo, integrado ao fluxo Git. |
| **GitHub Actions** | CI/CD do GitHub. O workflow `deploy.yml` executa `mkdocs build` e faz deploy para GitHub Pages. | Automatiza build e publicação — o único processo automatizado do pipeline. |
| **`nav`** | Seção do `mkdocs.yml` que define a hierarquia de navegação do site: Home → Matéria → Capítulo → Tema. | Precisa ser atualizada manualmente a cada novo resumo adicionado. |
| **MathJax** | Biblioteca JavaScript para renderização de fórmulas matemáticas em LaTeX no browser. Habilitada via `pymdownx.arithmatex`. | Essencial para resumos de Economia (fórmulas de elasticidade, IS-LM, etc.). |
| **Admonition** | Extensão markdown (`!!! tipo "título"`) que cria caixas estilizadas (note, info, warning, tip, etc.). | Usada para notas especiais, avisos e temas correlatos nos resumos. |
| **Mermaid** | Biblioteca de diagramação via markdown (flowcharts, sequence diagrams). Habilitada via `pymdownx.superfences`. | Usada quando o conteúdo se beneficia de representação visual (fluxos, cronologias). |

---

## 4. Siglas e Acrônimos

| Sigla | Significado |
|-------|-------------|
| **CACD** | Concurso de Admissão à Carreira de Diplomata |
| **CESPE/CEBRASPE** | Centro Brasileiro de Seleção e Promoção de Eventos — organizadora do CACD |
| **MRE** | Ministério das Relações Exteriores (Itamaraty) |
| **LLM** | Large Language Model (Modelo de Linguagem de Grande Porte) |
| **CI/CD** | Continuous Integration / Continuous Deployment |
| **YAML** | YAML Ain't Markup Language — formato de serialização de dados |
| **CC-TT** | Capítulo-Tema — codificação numérica usada nos nomes de arquivo |
| **SDD** | Specification-Driven Development — metodologia usada nesta especificação |
| **RUP** | Rational Unified Process — framework de desenvolvimento iterativo |
