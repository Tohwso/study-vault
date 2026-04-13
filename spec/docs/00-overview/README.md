# Study Vault — Visão Geral do SDD

> **Artefato RUP:** Índice de Disciplinas (Governança)
> **Proprietário:** [RUP] Governante (👑)
> **Status:** In Progress
> **Última atualização:** 2026-07-19

---

## Sobre o Projeto

**Study Vault** é uma plataforma de resumos densos gerados por IA para preparação
em concursos públicos. O primeiro concurso coberto é o CACD 2026 (Carreira de Diplomata).

- **Stack:** MkDocs Material + Python + GitHub Pages
- **Conteúdo atual:** 84 resumos (60 História Mundial + 24 Economia)
- **Pipeline:** Geração via prompt template → revisão → publish

---

## Status das Disciplinas

| Disciplina | Diretório | Status | Proprietário |
|---|---|---|---|
| Modelagem de Negócios | `spec/docs/01-business/` | ✅ Completo | 📋 Analista de Negócios |
| Requisitos | `spec/docs/02-requirements/` | ✅ Completo | 📋 Analista de Requisitos |
| Design | `spec/docs/03-design/` | ✅ Completo | 🏛️ Arquiteto |
| Implementação | `spec/docs/04-implementation/` | ✅ Completo | 🔀 Desenvolvedor |
| Qualidade | `spec/docs/05-test/` | ✅ Completo | 🧪 Analista de Qualidade |
| Deployment | `spec/docs/06-deployment/` | ✅ Completo | 🏛️ Arquiteto + 🔀 Dev |
| Gestão de Mudanças | `spec/docs/07-change-management/` | ✅ Completo | 👑 Governante |

---

## Convenções

- **Idioma:** Português brasileiro
- **IDs técnicos:** Em inglês (RF-XX, NFR-XX, BR-XX, ADR-NNN)
- **Modo de supervisão:** Key Gates Only (AN→AR, Arq→Dev)
- **Pipeline:** Brownfield — reverse engineering do projeto existente

---

## Contexto Especial

Este projeto NÃO é um sistema de software convencional. É um pipeline de geração
de conteúdo estático. Os artefatos SDD devem ser adaptados a esse contexto:

- **Business:** Domínio do concurso, estrutura do edital, objetivos pedagógicos
- **Requirements:** Formato dos resumos, regras de naming, critérios de qualidade, extensibilidade
- **Architecture:** Estrutura do projeto, pipeline de automação, tooling
- **Implementation:** Scripts de automação, validação, configuração
- **Quality:** Conformidade dos resumos vs especificação, gaps, consistência
