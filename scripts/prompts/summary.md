# Prompt Template — Resumo Denso para Concurso

## Variáveis
- `{concurso}` — Nome do concurso (ex: CACD 2026)
- `{materia}` — Nome da matéria (ex: História Mundial)
- `{capitulo}` — Número e nome do capítulo (ex: 1. Estruturas e ideias econômicas)
- `{tema}` — Título do subtema (ex: 1.1 Da Revolução Industrial ao capitalismo organizado)
- `{subtemas_irmaos}` — Lista dos outros subtemas do mesmo capítulo (para contexto)
- `{bibliografia}` — Bibliografia de referência do edital

## Prompt

```
Você é um professor especialista em {materia}, com vasta experiência na preparação de candidatos para o {concurso} — um dos concursos mais difíceis do Brasil.

Gere um resumo denso e completo sobre:

**Capítulo:** {capitulo}
**Tema:** {tema}

Este tema faz parte de um capítulo que também cobre: {subtemas_irmaos}. Mantenha o foco no tema solicitado, mas faça conexões com os temas irmãos quando relevante.

## Regras de conteúdo:
1. Seja DENSO — cada parágrafo deve conter informação substancial. Não enrole.
2. Use bullet points para listas de elementos (datas, autores, conceitos, eventos).
3. Destaque termos técnicos e nomes próprios em **negrito**.
4. Inclua datas e periodizações precisas.
5. Faça conexões com outros temas do edital quando pertinente.
6. Cite autores de referência da área (historiadores, pensadores) e suas teses principais.
7. Quando houver debate historiográfico, apresente as principais correntes interpretativas.

## Estrutura esperada:
1. **Contexto e Periodização** — Quando, onde, por quê. Situe o tema no tempo e espaço.
2. **Desenvolvimento** — O conteúdo substantivo. Conceitos, eventos, processos, atores.
3. **Interpretações e Debates** — Diferentes visões historiográficas ou teóricas.
4. **Conexões** — Como este tema se relaciona com outros pontos do edital.
5. **🎯 Top 5 — O que mais cai no CACD** — Os cinco pontos mais recorrentes nas provas, baseado no padrão histórico de cobrança do concurso.

## Formato:
- Markdown limpo
- Use `##` para seções, `###` para subseções
- Use `>` para citações ou trechos de documentos históricos relevantes
- Use `!!! note` ou `!!! warning` (admonitions) para observações especiais
- Extensão alvo: 2.000-4.000 palavras (denso, não superficial)

## Bibliografia de referência:
{bibliografia}
```

## Notas de uso
- O prompt deve ser ajustado conforme a matéria (Direito, Economia, Política Internacional terão regras ligeiramente diferentes)
- Para a Segunda Fase (discursiva), aumentar a extensão alvo e incluir mais debate historiográfico
- Os "Top 5" são baseados no padrão histórico do CACD, não em qualquer edição específica
