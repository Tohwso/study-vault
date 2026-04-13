# Stakeholders — Study Vault

> **Artefato RUP:** Registro de Stakeholders (Modelagem de Negócios)
> **Proprietário:** [RUP] Analista de Negócios
> **Status:** Complete
> **Última atualização:** Reverse-engineered from source code (2026-07-19)
>
> ⚠️ Este artefato foi INFERIDO a partir da análise da implementação existente. Pode não refletir integralmente a intenção original do criador.

---

## 1. Registro de Stakeholders

### Stakeholders Humanos

| # | Papel | Descrição | Interesse | Influência | Expectativas |
|---|-------|-----------|-----------|------------|--------------|
| SH-01 | **Autor/Candidato** (Ricardo Costa) | Criador do projeto e usuário primário. Candidato ao CACD 2026. Executa manualmente o pipeline de geração e consome o conteúdo para estudo. | Cobertura completa do edital, qualidade e precisão do conteúdo, eficiência do processo de geração | Alta | Material confiável, denso e navegável que otimize o tempo de estudo; processo reprodutível para novas matérias |
| SH-02 | **Leitores eventuais** | Potenciais leitores caso o projeto seja tornado público (outros candidatos ao CACD ou concursos correlatos) | Acesso a material de qualidade, navegabilidade, confiabilidade | Baixa | Material compreensível sem contexto prévio; indicação clara de que é gerado por IA |

### Atores de Sistema

| # | Ator | Descrição | Interesse | Influência | Expectativas |
|---|------|-----------|-----------|------------|--------------|
| SA-01 | **LLM (modelo de linguagem)** | Ator que recebe o prompt template preenchido e gera o conteúdo textual dos resumos. Atualmente operada manualmente (sem API). | N/A (ferramenta) | Média — a qualidade do output depende do modelo e do prompt | Prompt bem estruturado, com contexto suficiente (variáveis preenchidas, bibliografia referenciada) |
| SA-02 | **MkDocs (gerador de site)** | Transforma os arquivos markdown em site HTML navegável com tema Material, busca e extensões. | N/A (ferramenta) | Média — define as capacidades de apresentação (busca, admonitions, MathJax, Mermaid) | Markdown bem-formado, `mkdocs.yml` com `nav` atualizado, extensões configuradas |
| SA-03 | **GitHub Actions (CI/CD)** | Pipeline automatizado que executa `mkdocs build` e faz deploy para GitHub Pages a cada push em `main`. | N/A (ferramenta) | Baixa — funciona de forma transparente | Workflow válido, dependências instaláveis (`mkdocs-material`) |
| SA-04 | **GitHub Pages (hosting)** | Hospedagem estática que serve o site compilado para acesso via browser. | N/A (infraestrutura) | Baixa | Site compilado dentro dos limites de tamanho (1GB) e bandwidth |
| SA-05 | **Git/GitHub (versionamento)** | Controle de versão dos arquivos fonte e histórico de evolução do conteúdo. | N/A (ferramenta) | Baixa | Commits atômicos, branches organizados |

---

## 2. Matriz de Influência × Interesse

```
                    INTERESSE
                Baixo         Alto
           ┌────────────┬────────────┐
    Alto    │            │  SH-01     │
           │            │  (Autor)   │
INFLUÊNCIA │            │            │
           ├────────────┼────────────┤
    Baixo  │  SA-03,    │  SH-02     │
           │  SA-04,    │  (Leitores │
           │  SA-05     │  eventuais)│
           │            │  SA-01,    │
           │            │  SA-02     │
           └────────────┴────────────┘
```

### Interpretação

- **SH-01 (Autor/Candidato)** é o stakeholder dominante: alta influência (decide tudo) e alto interesse (é o consumidor do conteúdo). Toda decisão do pipeline gravita ao redor de suas necessidades de estudo.
- **SA-01 (LLM) e SA-02 (MkDocs)** têm interesse indireto alto — a qualidade final depende fortemente deles — mas influência limitada (são ferramentas substituíveis).
- **SA-03 a SA-05** são infraestrutura de suporte com influência e interesse baixos.
- **SH-02 (Leitores eventuais)** não são atores ativos hoje, mas representam um cenário futuro de distribuição.

---

## 3. Observações sobre o Contexto de Stakeholders

### Projeto single-user
O Study Vault é atualmente um **projeto de uso pessoal**. O único stakeholder humano ativo é o Autor/Candidato. Isso tem implicações:

- **Todas as decisões são unilaterais** — não há negociação entre interesses conflitantes
- **Qualidade é auto-avaliada** — não há peer review formal dos resumos
- **O pipeline é manual por escolha** — a automação via API da LLM não foi implementada porque o volume de temas é finito e o processo manual permite ajuste caso a caso
- **Documentação do processo é mínima** — o conhecimento de como gerar resumos está na cabeça do Autor, não em procedimentos escritos

### Risco de bus factor
O projeto tem **bus factor = 1**. Todo o conhecimento operacional (qual LLM usar, como preencher o prompt, como ajustar para novas matérias, como atualizar o `mkdocs.yml`) está concentrado em uma única pessoa. O SDD em construção mitiga parcialmente esse risco ao formalizar o processo.
