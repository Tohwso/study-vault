# Riscos e Limitações — Study Vault

> **Artefato RUP:** Risk & Limitations Assessment (Gestão de Mudanças)
> **Proprietário:** [RUP] Analista de Qualidade
> **Status:** Complete
> **Última atualização:** 2026-07-21

---

## 1. Riscos Operacionais

| ID | Risco | Probabilidade | Impacto | Mitigação Atual | Mitigação Proposta |
|----|-------|--------------|---------|-----------------|---------------------|
| R-001 | **Conteúdo factualmente incorreto publicado** — LLMs geram informações plausíveis mas errôneas (alucinações) | Alta | Alto — candidato internaliza informação incorreta para concurso | Disclaimer na home (RF-32) e rodapé (RF-11). Menção à bibliografia no prompt | Validação cruzada com bibliografia para temas críticos (UQ-002 permanece aberta) |
| R-002 | **CI bloqueado pós-backfill** — os 84 ERROs remanescentes (seções/admonitions) impedem deploy | Alta (se backfill parcial) | Alto — site não atualiza | Backfill resolve 418/502 ERROs | Decidir entre: gerar conteúdo faltante, rebaixar severidade, ou excluir do gate |
| R-003 | **Prompt template diverge dos requisitos** — inversão de dependência (AS-07) não executada | Média | Médio — resumos novos podem não seguir a spec se o template não for atualizado | ADR-003 documenta a decisão | Reescrever template a partir dos RFs (TD-004) |
| R-004 | **Degradação de MathJax CDN** — MathJax carregado via cdn.jsdelivr.net sem fallback local | Baixa | Médio — fórmulas de Economia ficam ilegíveis | Degradação graciosa: LaTeX raw é legível | Bundle local de MathJax (aumenta tamanho do artefato) |
| R-005 | **Supply chain: GitHub Actions** — Actions pinadas por major version, não SHA | Baixa | Médio — comprometimento de action = code execution no pipeline | Prática padrão do ecossistema | Pinar por SHA (TD-011) |
| R-006 | **Deploy acidental de conteúdo incompleto** — push direto em main sem staging (ADR-007) | Média | Baixo — site de estudo pessoal, reversível em minutos | Build local (mkdocs serve) + validate.py antes de push | Aceito como trade-off (single-user) |
| R-007 | **Backfill corrompe conteúdo** — script modifica 80 arquivos de uma vez | Baixa | Alto — perda de conteúdo de resumos | Dry-run por default. Script NÃO modifica corpo do markdown | Git permite rollback (git checkout -- docs/) |

---

## 2. Limitações Conhecidas

### 2.1 Limitações do Conteúdo

| ID | Limitação | Origem | Consequência |
|----|-----------|--------|--------------|
| L-001 | **Validação factual impossível por automação** | UQ-002 (aberta) | A qualidade factual dos 80 resumos depende inteiramente da revisão humana. Nenhuma ferramenta do pipeline verifica se datas, autores, teses ou fatos estão corretos |
| L-002 | **"Top 5" baseado em percepção da LLM**, não em análise estatística de provas | UQ-005 (resolvida) | Os tópicos "mais cobrados" podem não refletir a realidade. Disclaimer obrigatório (RF-16) mitiga parcialmente |
| L-003 | **Consistência terminológica não verificada** | NFR-08 | O mesmo conceito pode usar termos diferentes em resumos distintos. Verificação exigiria NLP cross-documento — fora do escopo |
| L-004 | **Word count via `split()` é aproximação** | AS-12 | Inclui tokens markdown, LaTeX, YAML. A margem 1500-5000 (vs spec 2000-4000) compensa, mas a contagem não é precisa |
| L-005 | **Frontmatter parser é regex, não YAML** | ADR-005, AS-11 | Funciona para YAML flat (validado em 100% dos 80 arquivos). Se o frontmatter evoluir para incluir listas ou nesting, o parser quebra silenciosamente |

### 2.2 Limitações do Pipeline

| ID | Limitação | Origem | Consequência |
|----|-----------|--------|--------------|
| L-006 | **Geração de conteúdo é 100% manual** | ADR-006 | Cada resumo requer ~15-30 min de interação humana com LLM. Para 300+ temas, isso representa ~75-150 horas de trabalho |
| L-007 | **Sem staging environment** | ADR-007 | Qualquer push em main vai direto para produção. Erros de renderização (MathJax, Mermaid) só são detectados em produção ou via build local |
| L-008 | **validate.py cobre apenas 34% dos RFs automaticamente** | Análise QA | 17/41 RFs não possuem verificação automatizada. Os RFs de qualidade de conteúdo (RF-12 a RF-15, RF-23) são inerentemente não-automatizáveis |
| L-009 | **Sem testes automatizados para os scripts** | TD-010 | validate.py e backfill.py não têm testes unitários. Alterações nos scripts podem introduzir regressões silenciosas |

### 2.3 Limitações de Extensibilidade

| ID | Limitação | Origem | Consequência |
|----|-----------|--------|--------------|
| L-010 | **Matérias futuras não testadas** | AS-08 | As regras de flexibilidade (RF-10) foram definidas para Economia. Matérias como Direito ou Política Internacional podem exigir adaptações não previstas |
| L-011 | **`data/` não implementado** | ADR-004 | Os metadados do edital estão implícitos no `mkdocs.yml` e nos `index.md`. Risco de inconsistência aumenta com > 3 matérias |
| L-012 | **Variantes de prompt template não existem** | RF-29 | Economia usa o template base de HM. Uma variante `summary-economia.md` com instruções MathJax e subseções numeradas melhoraria a qualidade |

---

## 3. Cenários de Falha e seu Tratamento

| Cenário | Probabilidade | Tratamento Atual | Gap |
|---------|--------------|-------------------|-----|
| Build falha no CI (mkdocs build --strict) | Baixa | GitHub Actions reporta erro, autor corrige e faz novo push | Nenhum — funciona |
| validate.py detecta ERROs em resumo novo | Média | CI bloqueia deploy, autor corrige | Funciona, mas precisa resolver backfill primeiro |
| Backfill corrompe fórmulas LaTeX | Muito baixa | Script não toca no corpo. Git rollback como safety net | Nenhum — design seguro |
| LLM gera resumo com erro factual grave | Alta | Revisão manual do autor. Disclaimer público | UQ-002 — sem mitigação técnica |
| CDN do MathJax fica offline | Muito baixa | Fórmulas exibidas em LaTeX raw (legível) | Considerar bundle local |
| Autor esquece de atualizar nav | Média | `mkdocs build --strict` detecta arquivo órfão (warning) | Warning pode não ser suficiente |

---

## 4. Gaps de Compliance

| Aspecto | Estado Atual | Risco |
|---------|-------------|-------|
| **Transparência (conteúdo IA)** | Disclaimer na home + rodapé por resumo. Top 5 disclaimer especificado (RF-16) mas nem sempre presente | Médio — projeto público. Leitor pode não perceber que é conteúdo sintético |
| **Direitos autorais** | Resumos são obras derivadas de síntese bibliográfica via LLM. Sem citação direta de trechos extensos | Baixo — resumo não é reprodução, é síntese. Fair use acadêmico |
| **Acessibilidade** | Tema Material garante WCAG AA. MathJax tem suporte a screen readers | Baixo — plataforma cuida |
| **Dados pessoais** | Nenhum dado pessoal no repositório ou site | Nenhum |

---

## 5. Matriz de Risco Consolidada

```
         IMPACTO
         Alto  ┃ R-001(fact)  R-007(corrupt)
               ┃ R-002(CI)
         ──────╋─────────────────────────
         Médio ┃ R-003(prompt) R-004(CDN)
               ┃ R-006(deploy) R-005(supply)
         ──────╋─────────────────────────
         Baixo ┃
               ┃
         ══════╋═══════════╤═══════════╤════════
               ┃  Baixa    │  Média    │  Alta
               ┗━━━━━━━━━━━┷━━━━━━━━━━━┷━━━━━━━━
                      PROBABILIDADE
```

**Risco dominante:** R-001 (conteúdo factualmente incorreto). É o único risco de alta probabilidade E alto impacto. A mitigação atual (disclaimers) é paliativa — a questão UQ-002 permanece aberta sem solução técnica.
