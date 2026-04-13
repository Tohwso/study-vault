# Visão do Produto — Study Vault

> **Artefato RUP:** Documento de Visão (Modelagem de Negócios)
> **Proprietário:** [RUP] Analista de Negócios
> **Status:** Complete
> **Última atualização:** Reverse-engineered from source code (2026-07-19)
>
> ⚠️ Este artefato foi INFERIDO a partir da análise da implementação existente. Pode não refletir integralmente a intenção original do criador.

---

## 1. Declaração do Problema

| Dimensão | Descrição |
|----------|-----------|
| **O problema** | A preparação para o CACD exige domínio de um volume massivo de conteúdo (8+ matérias, centenas de temas) espalhado por dezenas de livros acadêmicos densos. O candidato gasta tempo desproporcional na leitura exploratória antes de conseguir consolidar o conhecimento em formato revisável. |
| **Afeta** | Candidatos ao CACD 2026 (e potencialmente a edições futuras), que precisam cobrir todo o programa do edital em tempo limitado. |
| **Impacto** | Perda de eficiência no estudo: leitura de 20+ livros para cada matéria consome meses, com retenção desigual. Não há material consolidado, estruturado e navegável que cubra o programa inteiro de forma densa. |
| **Solução proposta** | Um pipeline de geração de conteúdo que transforma a bibliografia do edital em resumos densos (2.000–4.000 palavras cada), estruturados em formato padronizado, navegáveis via site estático com busca, organizados por capítulo/tema do edital — gerados por IA e publicados automaticamente via GitHub Pages. |

---

## 2. Posicionamento do Produto

| Dimensão | Descrição |
|----------|-----------|
| **Para** | Candidatos ao CACD 2026 (uso pessoal — atualmente single-user) |
| **Que precisam** | Consolidar o programa do edital em material denso, revisável e navegável |
| **O Study Vault é** | Um pipeline de geração de conteúdo estático que produz resumos densos por IA, publicados como site MkDocs |
| **Que** | Cobre o programa oficial do edital tema a tema, com estrutura padronizada (Contexto → Desenvolvimento → Interpretações → Conexões → Top 5), interligação entre temas e busca full-text |
| **Diferente de** | Resumos manuais (lentos, inconsistentes em profundidade), cursinhos preparatórios (genéricos, sem controle do candidato), livros originais (extensos demais para revisão rápida) |
| **O diferencial é** | Densidade controlada por prompt template, estrutura uniforme que facilita revisão, cobertura exaustiva do edital, e custo marginal próximo de zero para gerar novos temas (apenas o custo de tokens da LLM) |

---

## 3. Resumo dos Stakeholders

| Stakeholder | Interesse | Influência |
|-------------|-----------|------------|
| Candidato/Autor (Ricardo Costa) | Usar o material para estudo pessoal; garantir qualidade e cobertura completa do edital | Alta |
| IA (LLM geradora) | Ator de sistema — gera os resumos a partir do prompt template | Média |
| GitHub Pages | Ator de sistema — hospeda e serve o site estático | Baixa |
| Potenciais leitores futuros | Eventual público se o projeto for aberto | Baixa |

> Detalhamento completo em `stakeholders.md`.

---

## 4. Objetivos de Negócio e Critérios de Sucesso

| ID | Objetivo | Critério de Sucesso | Prioridade |
|----|----------|---------------------|------------|
| BG-01 | Cobertura completa do edital por matéria | 100% dos temas listados no edital possuem resumo publicado | Alta |
| BG-02 | Densidade e qualidade do conteúdo | Cada resumo contém entre 2.000 e 4.000 palavras, com as 5 seções obrigatórias | Alta |
| BG-03 | Navegabilidade e usabilidade | O candidato consegue localizar qualquer tema em ≤3 cliques a partir da home | Média |
| BG-04 | Busca transversal | Termos e conceitos são encontráveis via busca full-text do MkDocs | Média |
| BG-05 | Reprodutibilidade do pipeline | Adicionar uma nova matéria segue o mesmo processo (prompt template + naming + nav) | Alta |
| BG-06 | Publicação automática | Push em `main` publica automaticamente via GitHub Actions + GitHub Pages | Média |
| BG-07 | Extensibilidade para outros concursos | A estrutura (prompt template, naming, organização) pode ser reaproveitada para outros concursos (ex: ABIN, EPPGG, ANPEC) | Baixa |

---

## 5. Escopo

### 5.1 Dentro do Escopo

- Geração de resumos densos para cada tema do edital do CACD 2026
- Organização por matéria → capítulo → tema, seguindo a numeração do edital
- Prompt template parametrizado para cada matéria
- Frontmatter YAML padronizado para metadados de cada resumo
- Convenção de naming de arquivos (`CC-TT-slug.md`)
- Navegação hierárquica em `mkdocs.yml`
- Deploy automático via GitHub Actions
- Suporte a fórmulas matemáticas (MathJax) para matérias quantitativas (Economia)
- Admonitions para notas, avisos e temas correlatos
- Diagramas Mermaid quando necessário

### 5.2 Fora do Escopo

- Geração automática via script/API (atualmente o prompt é executado manualmente na LLM)
- Controle de versão de qualidade dos resumos (não há "revisão formal" com checklist)
- Exercícios, simulados ou questões de prova
- Conteúdo para a Segunda Fase (discursiva) — mencionado no prompt como extensão futura
- Multi-tenancy ou sistema de usuários
- Monetização ou distribuição comercial
- Integração com plataformas de estudo (Anki, Notion, etc.)

### 5.3 Restrições

| # | Restrição | Impacto |
|---|-----------|---------|
| R-01 | O conteúdo é gerado por IA sem validação humana sistemática — pode conter imprecisões historiográficas ou conceituais | Risco de internalizar informações incorretas |
| R-02 | Dependência de um único prompt template — ajustes para matérias com natureza diferente (Direito, Política Internacional) são manuais | Esforço adicional para cada nova matéria |
| R-03 | MkDocs é gerador estático — não suporta interatividade, personalização por usuário ou progresso de estudo | Funcionalidades interativas exigiriam migração de stack |
| R-04 | GitHub Pages tem limite de tamanho de site (1GB) e largura de banda | Para o volume atual (~84 arquivos markdown) não é limitante |

### 5.4 Riscos

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|-------|---------------|---------|-----------|
| RS-01 | Conteúdo factualmente incorreto nos resumos gerados por IA | Média | Alto | Cruzar com bibliografia de referência nos temas mais críticos |
| RS-02 | Mudança de edital para CACD 2026 invalida parte dos temas | Baixa | Médio | A estrutura modular (1 arquivo por tema) permite ajustes pontuais |
| RS-03 | Viés de "resumo por IA" — falta de nuance historiográfica que a banca espera | Média | Alto | A seção "Interpretações e Debates" mitiga parcialmente; leitura das obras de referência continua necessária para 2ª fase |

### 5.5 Premissas

| # | Premissa |
|---|----------|
| AS-01 | O programa do edital CACD 2026 é suficientemente estável para que os temas gerados permaneçam válidos |
| AS-02 | Resumos densos de 2.000–4.000 palavras são suficientes para a Primeira Fase (objetiva); para a Segunda Fase, servem como ponto de partida |
| AS-03 | A qualidade da LLM utilizada é suficiente para produzir conteúdo factualmente confiável com a bibliografia indicada |
| AS-04 | O formato MkDocs Material atende às necessidades de navegação e busca do candidato |
| AS-05 | Cada tema do edital mapeia 1:1 para um arquivo markdown (sem necessidade de split ou merge) |
