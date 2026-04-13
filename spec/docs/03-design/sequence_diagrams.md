# Diagramas de Sequência — Study Vault

> **Artefato RUP:** Diagramas de Sequência (Análise & Design)
> **Proprietário:** [RUP] Arquiteto
> **Status:** Complete
> **Última atualização:** 2026-07-19

---

## 1. Fluxo de Geração de Resumo (UC-01)

Fluxo end-to-end desde a seleção do tema até o resumo pronto para commit.

```mermaid
sequenceDiagram
    actor Autor
    participant IndexMD as index.md<br>(matéria)
    participant Template as Prompt<br>Template
    participant LLM as LLM<br>(variada)
    participant Arquivo as Arquivo<br>.md
    participant Validador as validate.py<br>(proposto)

    Autor->>IndexMD: Seleciona próximo tema pendente
    IndexMD-->>Autor: Tema, edital_ref, capítulo

    Autor->>Template: Preenche variáveis<br>({concurso}, {materia}, {capitulo},<br>{tema}, {subtemas_irmaos}, {bibliografia})
    Template-->>Autor: Prompt preenchido

    Autor->>+LLM: Submete prompt
    LLM-->>-Autor: Conteúdo gerado

    alt Output satisfatório
        Autor->>Arquivo: Monta arquivo completo
        Note over Arquivo: 1. Frontmatter YAML<br>2. Título H1<br>3. Metadata blockquote<br>4. Admonition temas irmãos<br>5. Conteúdo (5 seções)<br>6. Disclaimer Top 5<br>7. Rodapé com modelo
    else Output insatisfatório
        Autor->>Template: Ajusta prompt (mais contexto)
        Autor->>+LLM: Resubmete
        LLM-->>-Autor: Novo output
    end

    Autor->>Arquivo: Salva como CC-TT-slug.md

    opt Validação automatizada (proposto)
        Autor->>+Validador: python validate.py arquivo.md
        Validador-->>-Autor: Resultado (OK / lista de desvios)
        alt Desvios encontrados
            Autor->>Arquivo: Corrige desvios
        end
    end

    Autor->>IndexMD: Atualiza status: pendente → completo
```

---

## 2. Fluxo de Onboarding de Nova Matéria (UC-02)

Fluxo desde a decisão de adicionar uma matéria até a estrutura pronta para geração.

```mermaid
sequenceDiagram
    actor Autor
    participant Edital as Edital CACD<br>(fonte canônica)
    participant DataYML as data/<materia>.yml<br>(proposto)
    participant DocsDir as docs/<materia>/
    participant IndexMD as index.md<br>(matéria)
    participant PromptDir as scripts/prompts/
    participant MkDocs as mkdocs.yml
    participant HomeMD as docs/index.md

    Autor->>Edital: Consulta programa oficial
    Edital-->>Autor: Matéria, capítulos, temas, bibliografia

    Autor->>DocsDir: Cria diretório docs/<materia>/

    opt Metadados centralizados (ADR-004)
        Autor->>DataYML: Cria YAML com capítulos, temas, bibliografia
    end

    Autor->>IndexMD: Cria index.md com tabela de todos os temas
    Note over IndexMD: Todos os temas com status "pendente"<br>Links previstos (CC-TT-slug.md)

    Autor->>PromptDir: Avalia template base vs. necessidade de variante

    alt Variante necessária (ex: MathJax, artigos legais)
        Autor->>PromptDir: Cria summary-<materia>.md
        Note over PromptDir: Documenta diferenças<br>em relação ao base
    end

    Autor->>MkDocs: Adiciona matéria ao nav
    Note over MkDocs: Seção com Visão Geral +<br>capítulos + temas (links)

    Autor->>HomeMD: Atualiza tabela de matérias
    Note over HomeMD: Nome, capítulos, temas,<br>status "Em andamento"
```

---

## 3. Fluxo de Validação Pós-Geração (UC-05)

Fluxo do checklist de conformidade — manual ou automatizado.

```mermaid
sequenceDiagram
    actor Autor
    participant Validador as validate.py
    participant Resumo as Arquivo .md
    participant Relatorio as Relatório<br>de desvios

    Autor->>Validador: python validate.py [--materia X | arquivo.md]

    loop Para cada resumo no escopo
        Validador->>+Resumo: Lê arquivo

        Validador->>Validador: 1. Frontmatter parseável?
        Validador->>Validador: 2. 8 campos obrigatórios?
        Validador->>Validador: 3. Formato do title?
        Validador->>Validador: 4. status válido?
        Validador->>Validador: 5. data_geracao ISO 8601?
        Validador->>Validador: 6. Metadata blockquote?
        Validador->>Validador: 7. Admonition temas irmãos?
        Validador->>Validador: 8. Seções obrigatórias?
        Validador->>Validador: 9. Word count 2K-4K?
        Validador->>Validador: 10. Rodapé com disclaimer?
        Validador->>Validador: 11. Naming CC-TT-slug?

        Resumo-->>-Validador: Resultado por arquivo
    end

    Validador->>Relatorio: Gera relatório de desvios
    Relatorio-->>Autor: Lista: arquivo, desvio, severidade

    alt Desvios ERRO
        Autor->>Resumo: Corrige (UC-03)
    else Apenas AVISO
        Autor->>Autor: Avalia caso a caso
    else Tudo OK
        Autor->>Autor: ✅ Pronto para commit
    end
```

---

## 4. Fluxo de CI/CD — Push → Build → Deploy (UC-04)

Fluxo do pipeline atual com melhorias propostas (quality gate de validação).

```mermaid
sequenceDiagram
    actor Autor
    participant Git as Git Local
    participant GitHub as GitHub<br>(main)
    participant Actions as GitHub Actions
    participant Validador as validate.py<br>(proposto)
    participant MkDocs as mkdocs build
    participant Pages as GitHub Pages

    Autor->>Git: git add + git commit
    Autor->>GitHub: git push origin main

    GitHub->>+Actions: Dispara workflow deploy.yml

    Note over Actions: Job: build

    Actions->>Actions: checkout código
    Actions->>Actions: setup-python 3.12

    opt Quality Gate proposto
        Actions->>+Validador: pip install pyyaml<br>python scripts/validate.py
        alt Desvios ERRO
            Validador-->>-Actions: Exit code 1
            Actions-->>GitHub: ❌ Build failed
            GitHub-->>Autor: Notificação de falha
            Note over Autor: Corrige e faz novo push
        else OK / apenas AVISOs
            Validador-->>Actions: Exit code 0 (warnings no log)
        end
    end

    Actions->>Actions: pip install mkdocs-material
    Actions->>+MkDocs: mkdocs build

    alt Build OK
        MkDocs-->>-Actions: Artefato /site gerado
        Actions->>Actions: upload-pages-artifact

        Note over Actions: Job: deploy
        Actions->>+Pages: deploy-pages
        Pages-->>-Actions: URL do site

        Actions-->>-GitHub: ✅ Deploy concluído
    else Build falha
        MkDocs-->>Actions: Exit code != 0
        Actions-->>GitHub: ❌ Build failed
        GitHub-->>Autor: Notificação de falha
    end
```

---

## 5. Fluxo de Backfill de Resumos Existentes (RF-38 a RF-41)

Processo único de migração para padronizar os 84 resumos existentes.

```mermaid
sequenceDiagram
    actor Autor
    participant Validador as validate.py<br>--report
    participant Relatorio as backfill-report.md
    participant Resumo as Arquivos .md<br>(84 resumos)
    participant Git as Git

    Note over Autor: Processo único de migração

    Autor->>+Validador: python validate.py --report backfill-report.md
    Validador->>Validador: Varre todos os 84 resumos
    Validador->>Validador: Detecta: títulos fora do padrão,<br>campos ausentes, seções faltando,<br>rodapé ausente
    Validador-->>-Relatorio: Relatório por arquivo:<br>desvio | valor atual | valor esperado

    Autor->>Relatorio: Revisa relatório

    loop Para cada resumo com desvios
        Autor->>+Resumo: Abre arquivo
        Note over Autor, Resumo: RF-38: Ajusta title de Economia<br>RF-39: Verifica Conexões/Top 5<br>RF-40: Adiciona data_geracao e modelo_llm<br>RF-41: Adiciona rodapé
        Autor->>-Resumo: Salva correções
    end

    Autor->>+Validador: python validate.py
    Validador-->>-Autor: Verificação final: 0 erros

    Autor->>Git: git add + commit + push
    Note over Git: "fix: padroniza frontmatter e<br>estrutura de todos os resumos<br>conforme RF-38 a RF-41"
```

---

## 6. Fluxo de Revisão e Correção (UC-03)

Fluxo reativo quando o Autor identifica um erro em resumo publicado.

```mermaid
sequenceDiagram
    actor Autor
    participant Site as Site<br>(GitHub Pages)
    participant Resumo as Arquivo .md
    participant Biblio as Bibliografia
    participant Git as Git
    participant Actions as GitHub Actions

    Autor->>Site: Identifica erro durante estudo

    alt Erro factual
        Autor->>Biblio: Pesquisa fonte correta
        Biblio-->>Autor: Informação verificada
        Autor->>Resumo: Corrige trecho factual
    else Erro de formatação
        Autor->>Resumo: Corrige markdown diretamente
    else Erro de renderização (MathJax/Mermaid)
        Autor->>Resumo: Corrige sintaxe LaTeX/Mermaid
    else Erro de conformidade
        Autor->>Resumo: Ajusta para atender RFs
    end

    Autor->>Git: git commit -m "fix: <descrição>"
    Autor->>Git: git push origin main
    Git->>+Actions: Dispara workflow
    Actions->>Actions: Build + Deploy
    Actions-->>-Site: Site atualizado (~2-5 min)
```
