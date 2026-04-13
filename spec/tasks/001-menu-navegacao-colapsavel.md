# Task 001: Menu de navegação colapsável por disciplina

## Status
Done

## Contexto
O menu lateral do site exibe todas as disciplinas (História Mundial, Economia) com todos os capítulos e temas expandidos por default. Com 84 temas e a previsão de mais 5 matérias, a navegação fica excessivamente longa e difícil de usar.

## Problema
A feature `navigation.expand` no `mkdocs.yml` força todos os grupos de navegação a abrirem automaticamente. Isso elimina a possibilidade de colapsar/expandir seções.

## Objetivo
Permitir que cada agrupamento (disciplina, capítulo) seja colapsável, iniciando fechado no nível das disciplinas. O usuário clica para expandir apenas a seção de interesse.

## Escopo
- Remover `navigation.expand` do mkdocs.yml
- Manter `navigation.sections` para renderizar os agrupamentos como seções
- Validar que o menu inicia colapsado no nível das disciplinas

## Fora do Escopo
- Alterações no conteúdo dos resumos
- Mudanças de tema ou cores

## Artefatos Impactados
- `mkdocs.yml` (features do theme)

## Requisitos Funcionais
- RF-NAV-01: Menu lateral deve ser colapsável em todos os níveis de agrupamento
- RF-NAV-02: Menu deve iniciar colapsado no nível das disciplinas (História Mundial, Economia)
- RF-NAV-03: Clicar em um grupo deve expandir/colapsar seus filhos

## Requisitos Não-Funcionais
- NFR-NAV-01: Não adicionar dependências extras (feature nativa do MkDocs Material)

## Critérios de Aceite
- [ ] Menu inicia colapsado no nível das disciplinas
- [ ] Cada agrupamento (disciplina, capítulo) pode ser expandido/colapsado com clique
- [ ] A navegação para páginas individuais continua funcionando
- [ ] O build do site (`mkdocs build --strict`) passa sem erros

## Dependências
Nenhuma
