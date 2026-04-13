# Padrões de Verificação — Study Vault

> **Artefato RUP:** Padrões de Teste (Qualidade)
> **Proprietário:** [RUP] Analista de Qualidade
> **Status:** Complete
> **Última atualização:** 2026-07-21

---

## 1. Execução do validate.py

### 1.1 Validação Completa

```bash
cd /path/to/study-vault
python3 scripts/validate.py --path docs/ --verbose
```

### 1.2 Interpretação do Output

**Estrutura do output:**
```
─── docs/economia/01-01-demanda-do-consumidor.md
  [ERRO] Campo obrigatório ausente no frontmatter: 'materia'
  [ERRO] Seção obrigatória ausente: 'Conexões com Outros Temas'
  [AVISO] Rodapé com disclaimer de IA ausente ('*Gerado por IA...')

════════════════════════════════════════════════════════════
Validação concluída: 80 arquivos analisados
  502 erro(s) em 80 arquivo(s)
  76 aviso(s) em 69 arquivo(s)
  0 arquivo(s) sem erros
════════════════════════════════════════════════════════════
```

**Severidades:**

| Severidade | Significado | Bloqueia CI? | Exit code |
|------------|------------|--------------|-----------|
| `[ERRO]` | Violação de requisito obrigatório — o resumo não está conforme | Sim | 1 |
| `[AVISO]` | Desvio de recomendação — desejável corrigir mas não impeditivo | Não | 0 |

**Exit codes:**
- `0` — todos os arquivos passaram (avisos são aceitáveis)
- `1` — pelo menos 1 ERRO encontrado

### 1.3 Checks Executados (11 verificações)

| # | Check | Severidade | RF | O que busca |
|---|-------|------------|-----|-------------|
| 1 | Frontmatter presente | ERRO | RF-02 | Bloco `---...---` no início do arquivo |
| 2 | 8 campos obrigatórios | ERRO | RF-02, RF-05, RF-06 | title, edital_ref, capitulo, materia, concurso, status, data_geracao, modelo_llm |
| 3 | Formato do title | ERRO | RF-03 | Regex: `^\d{4}\s*-\s*.+\s*-\s*.+\s*-\s*.+$` |
| 4 | Valor de status | ERRO | RF-04 | ∈ {completo, em_revisao, pendente} |
| 5 | Formato data_geracao | AVISO | RF-05 | Regex: `^\d{4}-\d{2}-\d{2}$` |
| 6 | Metadata blockquote | ERRO | RF-07 | Linha com `>` após H1 |
| 7 | Admonition temas irmãos | ERRO | RF-08 | Linha começando com `!!! info` |
| 8 | Seção Conexões | ERRO | RF-09 | H2 contendo "Conex" |
| 9 | Seção Top 5 | ERRO | RF-09 | H2 contendo "Top 5" |
| 10 | Word count | AVISO | RF-22 | Entre 1.500 e 5.000 palavras (margem sobre spec de 2.000-4.000) |
| 11 | Rodapé disclaimer | AVISO | RF-11 | Linha `*Gerado por IA...` |

### 1.4 O que NÃO é checado

| Item | RF | Por que não é checado |
|------|-----|----------------------|
| Conteúdo do disclaimer no Top 5 | RF-16 | Apenas presença do H2 é verificada |
| Consistência materia vs diretório | FRONT-08 | Não implementado |
| Kebab-case/acentos no slug | RF-17 | Regex aceita qualquer char após CC-TT- |
| 3 seções nomeadas (HM) | RF-09 | Flexibilidade RF-10 torna opcional |
| Termos em negrito, datas precisas | RF-12, RF-13 | Exige análise semântica |

---

## 2. Checklist Manual de Revisão de Resumo

Para verificações que o validate.py não cobre, usar este checklist ao revisar um resumo:

### 2.1 Checklist Estrutural (complementar ao validate.py)

- [ ] **RF-01**: O arquivo cobre UM tema — não há split ou merge
- [ ] **RF-07**: Metadata blockquote contém todos os 5 campos (Concurso, Matéria, Capítulo, Referência no edital, Status)
- [ ] **RF-08**: Admonition lista TODOS os temas irmãos do capítulo (verificar contra index.md da matéria)
- [ ] **RF-16**: Seção Top 5 começa com disclaimer explícito sobre percepção da LLM
- [ ] **RF-19**: index.md da matéria está atualizado com status do tema

### 2.2 Checklist de Qualidade de Conteúdo

- [ ] **RF-12**: Termos técnicos e nomes próprios em **negrito**
- [ ] **RF-13**: Datas e periodizações são precisas (anos, não "século XIX" vago)
- [ ] **RF-14**: Autores de referência citados com suas teses principais (obra + ano quando possível)
- [ ] **RF-15**: Debate historiográfico/teórico apresenta múltiplas correntes, não visão única
- [ ] **RF-23**: Conteúdo é baseado na bibliografia de referência do edital
- [ ] **RF-24**: Formatação usa `##` para seções, `###` para subseções, `>` para citações, `!!!` para observações
- [ ] **RF-25** (Economia): Fórmulas usam MathJax (`$$...$$` ou `$...$`), não texto plano

### 2.3 Checklist de Publicação

- [ ] **RF-21**: Resumo tem entrada correspondente no `nav` do `mkdocs.yml`
- [ ] **RF-32**: Home (`docs/index.md`) contém disclaimer de IA proeminente
- [ ] **RF-34**: Tabela de matérias na home está atualizada
- [ ] Build local (`mkdocs serve`) renderiza o resumo corretamente

---

## 3. Padrão de Verificação de Backfill (Antes/Depois)

### 3.1 Fluxo Completo

```bash
# PASSO 1: Capturar estado atual
python3 scripts/validate.py --path docs/ > estado-pre-backfill.txt 2>&1
echo "PRE: $(grep -c '\[ERRO\]' estado-pre-backfill.txt) erros"

# PASSO 2: Dry-run do backfill (ver o que vai mudar)
python3 scripts/backfill.py --path docs/ > backfill-dry-run.txt 2>&1
cat backfill-dry-run.txt  # Revisar cada mudança planejada

# PASSO 3: Verificar mudanças específicas de interesse
# Exemplo: como os títulos de Economia vão ficar?
grep '~ title' backfill-dry-run.txt

# PASSO 4: Aplicar backfill
python3 scripts/backfill.py --path docs/ --apply

# PASSO 5: Capturar estado pós-backfill
python3 scripts/validate.py --path docs/ > estado-pos-backfill.txt 2>&1
echo "POS: $(grep -c '\[ERRO\]' estado-pos-backfill.txt) erros"

# PASSO 6: Comparar
echo "=== DIFF ==="
diff estado-pre-backfill.txt estado-pos-backfill.txt | head -50
```

### 3.2 O que o Backfill Resolve

| Alteração | Quantidade estimada | Verificável |
|-----------|--------------------:|-------------|
| Adicionar `materia` | 80 | validate.py ERRO → 0 |
| Adicionar `concurso` | 80 | validate.py ERRO → 0 |
| Adicionar `data_geracao` | 80 | validate.py ERRO → 0 |
| Adicionar `modelo_llm` | 80 | validate.py ERRO → 0 |
| Padronizar `title` (Economia) | 20 | validate.py ERRO → 0 |
| Adicionar rodapé | ~69 | validate.py AVISO → 0 |
| **Total alterações** | **~426** | |

### 3.3 O que o Backfill NÃO Resolve

| Gap | Quantidade | Ação necessária |
|-----|-----------|-----------------|
| Seção "Conexões" ausente | 25 | Gerar conteúdo via LLM ou escrita manual |
| Seção "Top 5" ausente | 5 | Gerar conteúdo via LLM ou escrita manual |
| Admonition `!!! info` ausente | 48 | Adicionar manualmente (lista de temas irmãos) |

### 3.4 Verificação de Integridade Pós-Backfill

Após aplicar o backfill, verificar que o conteúdo do corpo NÃO foi alterado:

```bash
# Verificar que fórmulas LaTeX não foram corrompidas
grep -r '\$\$' docs/economia/ | head -5  # Deve ter fórmulas intactas

# Verificar que admonitions existentes não foram alteradas
grep -r '!!!' docs/ | head -10

# Build test
mkdocs build --strict  # Deve passar sem erros
```

---

## 4. Padrão de Verificação de Novo Resumo

Ao gerar um novo resumo (UC-01), executar:

```bash
# 1. Validar apenas o arquivo novo
python3 scripts/validate.py --path docs/<materia>/

# 2. Verificar build
mkdocs serve  # Navegar até o resumo no browser

# 3. Checklist manual (seção 2 deste documento)
```

**Critério de aceitação:** zero ERROs no validate.py + checklist manual aprovado.

---

## 5. Padrão de Verificação de Nova Matéria (UC-02)

Ao adicionar nova matéria, verificar:

```bash
# 1. Diretório e index existem
ls docs/<nova-materia>/
cat docs/<nova-materia>/index.md

# 2. Entrada no nav
grep '<nova-materia>' mkdocs.yml

# 3. Tabela na home atualizada
grep '<Nova Matéria>' docs/index.md

# 4. Build
mkdocs build --strict
```
