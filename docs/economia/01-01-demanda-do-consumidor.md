---
title: "Demanda do Consumidor: Preferências, Equilíbrio e Elasticidade"
edital_ref: "1.1"
capitulo: "1. Microeconomia"
status: completo
---

# Demanda do Consumidor

> **Concurso:** CACD 2026
> **Matéria:** Economia
> **Capítulo:** 1. Microeconomia
> **Referência no edital:** 1.1 (1.1.1 a 1.1.4)
> **Status:** ✅ Completo

!!! info "Subtemas de 1.1 — Demanda do Consumidor"
    - **1.1.1** — Preferências *(este resumo)*
    - **1.1.2** — Equilíbrio do consumidor
    - **1.1.3** — Curva de demanda
    - **1.1.4** — Elasticidade-preço e elasticidade-renda

---

## 1. Preferências do Consumidor (1.1.1)

### 1.1 Axiomas das Preferências

A teoria do consumidor parte do pressuposto de que os indivíduos têm **preferências** sobre cestas de bens que podem ser ordenadas de forma consistente. Os axiomas fundamentais são:

- **Completude:** Dado qualquer par de cestas A e B, o consumidor sempre consegue compará-las: prefere A a B, prefere B a A ou é indiferente.
- **Transitividade:** Se A ≿ B e B ≿ C, então A ≿ C. Garante consistência lógica nas escolhas.
- **Reflexividade:** Toda cesta é tão boa quanto ela mesma (A ≿ A).

Sob esses axiomas, as preferências podem ser representadas por uma **função-utilidade** U(x₁, x₂, ..., xₙ), que atribui um número a cada cesta, preservando a ordenação das preferências.

!!! note "Utilidade: ordinal vs. cardinal"
    A teoria moderna (neoclássica) trabalha com **utilidade ordinal** — o número em si não tem significado, apenas a *ordem*. A noção de **utilidade cardinal** (que pressupõe unidades mensuráveis de satisfação) remonta aos utilitaristas clássicos (**Bentham, Jevons**) e foi abandonada pela maioria dos economistas no século XX após a crítica de **Pareto** e **Hicks**.

### 1.2 Curvas de Indiferença

Uma **curva de indiferença** representa o conjunto de todas as cestas que proporcionam o mesmo nível de utilidade ao consumidor. Propriedades:

- **Declinantes** (inclinação negativa): para manter o mesmo nível de utilidade, se aumenta o consumo de x₁, deve reduzir x₂ — reflexo da **Taxa Marginal de Substituição (TMS)** positiva entre os bens.
- **Convexas em relação à origem:** refletem o princípio da **utilidade marginal decrescente** — quanto mais se consome de um bem, menos se está disposto a abrir mão do outro para obtê-lo.
- **Não se cruzam:** se duas curvas se cruzassem, violariam o axioma da transitividade.

A **Taxa Marginal de Substituição (TMS)** mede a quantidade de y que o consumidor está disposto a sacrificar para obter uma unidade adicional de x, mantendo o mesmo nível de utilidade:

$$TMS_{x,y} = -\frac{\Delta y}{\Delta x}\bigg|_{U=\text{const}} = \frac{UMg_x}{UMg_y}$$

### 1.3 Casos Especiais de Preferências

| Tipo | Forma da curva | TMS | Exemplo |
|------|---------------|-----|---------|
| **Bens substitutos perfeitos** | Retas | Constante | Moedas de R$1 vs. duas de R$0,50 |
| **Bens complementares perfeitos** | Formato L (ângulo reto) | 0 ou ∞ | Pé esquerdo e pé direito do sapato |
| **Preferências côncavas** | Côncavas | Crescente | Comportamento de "tudo ou nada" |
| **Preferências regulares** | Convexas | Decrescente | Caso padrão |

### 1.4 Restrição Orçamentária

O consumidor enfrenta uma **restrição orçamentária**: sua cesta de consumo deve custar no máximo sua **renda (m)**:

$$p_1 x_1 + p_2 x_2 \leq m$$

A fronteira da restrição é a **reta orçamentária**, com inclinação $-p_1/p_2$, que representa o **preço relativo** dos bens. Deslocamentos:
- **Renda aumenta (m↑):** deslocamento paralelo para fora (mesma inclinação).
- **Preço de x₁ aumenta (p₁↑):** rotação da reta sobre o intercepto em x₂ (torna-se mais inclinada).

---

## 2. Equilíbrio do Consumidor (1.1.2)

### 2.1 Condição de Ótimo

O equilíbrio do consumidor ocorre no ponto em que sua **cesta ótima** maximiza a utilidade sujeita à restrição orçamentária. Geometricamente, é o ponto de **tangência** entre a curva de indiferença mais alta atingível e a reta orçamentária.

Algebricamente, a condição de ótimo interior é:

$$TMS_{x_1,x_2} = \frac{p_1}{p_2} \iff \frac{UMg_{x_1}}{UMg_{x_2}} = \frac{p_1}{p_2}$$

Rearranjando: $\dfrac{UMg_{x_1}}{p_1} = \dfrac{UMg_{x_2}}{p_2}$

**Interpretação:** o consumidor aloca sua renda de modo que a **utilidade marginal por unidade monetária gasta** seja igual em todos os bens. Caso contrário, ele poderia realocar gastos e aumentar a utilidade.

### 2.2 Método de Lagrange

Formalmente, o problema do consumidor é:

$$\max_{x_1, x_2} U(x_1, x_2) \quad \text{s.a.} \quad p_1 x_1 + p_2 x_2 = m$$

O **Lagrangiano** é: $\mathcal{L} = U(x_1, x_2) - \lambda(p_1 x_1 + p_2 x_2 - m)$

As condições de primeira ordem (CPO) geram o sistema que determina as **funções de demanda marshalliana** $x_1^*(p_1, p_2, m)$ e $x_2^*(p_1, p_2, m)$.

### 2.3 Efeitos Renda e Substituição (Decomposição de Slutsky)

Quando o preço de um bem muda, o efeito sobre a demanda se decompõe em:

- **Efeito Substituição (ES):** mudança na quantidade demandada devido à alteração do preço relativo, *mantendo o poder de compra constante* (o consumidor se move ao longo da curva de indiferença). **Sempre negativo** (Lei da Demanda) para bens normais e inferiores.

- **Efeito Renda (ER):** mudança na quantidade demandada devido à variação no poder de compra real. Para **bens normais** (renda↑ → demanda↑), o ER reforça o ES quando o preço cai. Para **bens inferiores**, o ER é contrário ao ES.

**Equação de Slutsky:**
$$\frac{\partial x_i}{\partial p_j} = \frac{\partial x_i^h}{\partial p_j} - x_j \frac{\partial x_i}{\partial m}$$

onde $x_i^h$ é a demanda **hicksiana** (compensada).

!!! warning "Bens de Giffen"
    **Bens de Giffen** são casos extremos em que o aumento de preço leva ao *aumento* da demanda — o efeito renda negativo supera o efeito substituição. São raros empiricamente; o exemplo clássico é a batata na Irlanda do século XIX (durante a Grande Fome). Diferem dos **bens de Veblen** (luxo ostentatório), cuja demanda aumenta com o preço por motivos de status social.

---

## 3. Curva de Demanda (1.1.3)

### 3.1 Derivação da Curva de Demanda

A **curva de demanda marshalliana** é obtida traçando as cestas ótimas do consumidor para diferentes níveis de preço de um bem, mantendo preços dos outros bens e renda constantes. Relaciona quantidade demandada com preço:

$$Q_d = D(p, p_{\text{outros}}, m, \text{preferências})$$

A **Lei da Demanda** estabelece que, *ceteris paribus*, quantidade demandada e preço se relacionam inversamente ($\partial Q_d / \partial p < 0$) — decorre do efeito substituição para bens normais.

### 3.2 Curva de Demanda de Mercado

A demanda de mercado é a **soma horizontal** das demandas individuais de todos os consumidores:

$$Q_D^{\text{mercado}}(p) = \sum_{i=1}^{n} q_i(p)$$

### 3.3 Deslocamentos da Curva vs. Movimento Sobre a Curva

- **Movimento sobre a curva:** variação no preço do próprio bem (mudança de $Q_d$ ao longo da curva).
- **Deslocamento da curva:** variação em qualquer outro determinante (renda, preços de outros bens, preferências, expectativas, número de consumidores). A curva inteira se desloca.

| Determinante | Bem Normal | Bem Inferior |
|---|---|---|
| Renda ↑ | Demanda ↑ (direita) | Demanda ↓ (esquerda) |
| Preço de bem substituto ↑ | Demanda ↑ | Demanda ↑ |
| Preço de bem complementar ↑ | Demanda ↓ | Demanda ↓ |

---

## 4. Elasticidades da Demanda (1.1.4)

### 4.1 Elasticidade-Preço da Demanda (EPD)

Mede a **sensibilidade** da quantidade demandada a variações no preço do bem:

$$\varepsilon_{p} = \frac{\% \Delta Q_d}{\% \Delta p} = \frac{\partial Q_d}{\partial p} \cdot \frac{p}{Q_d}$$

Como a Lei da Demanda implica relação inversa, $\varepsilon_p < 0$. Convenção: usa-se o **valor absoluto**.

| Valor de |ε| | Classificação | Significado |
|---|---|---|
| |ε| > 1 | **Demanda elástica** | Quantidade responde mais que proporcionalmente ao preço |
| |ε| = 1 | **Demanda unitária** | Variação proporcional |
| |ε| < 1 | **Demanda inelástica** | Quantidade responde menos que proporcionalmente |
| |ε| = 0 | **Perfeitamente inelástica** | Vertical — quantidade não varia |
| |ε| = ∞ | **Perfeitamente elástica** | Horizontal — preço não varia |

**Determinantes da elasticidade-preço:**
- **Disponibilidade de substitutos:** mais substitutos → mais elástica
- **Essencialidade do bem:** bens essenciais (insulina) → mais inelástica
- **Parcela no orçamento:** maior parcela → mais elástica
- **Horizonte temporal:** no longo prazo, mais tempo para adaptar → mais elástica
- **Definição do mercado:** mercado mais amplo → menos elástico (gasolina vs. Shell específica)

**Relação entre elasticidade e receita total:**
$$RT = p \cdot Q \implies \frac{\partial RT}{\partial p} = Q(1 + \varepsilon_p)$$

- |ε| > 1: redução de preço → aumento de RT
- |ε| < 1: aumento de preço → aumento de RT
- |ε| = 1: RT máxima

### 4.2 Elasticidade-Renda da Demanda (ERD)

Mede a variação percentual na quantidade demandada ante variação percentual na renda:

$$\varepsilon_m = \frac{\% \Delta Q_d}{\% \Delta m} = \frac{\partial Q_d}{\partial m} \cdot \frac{m}{Q_d}$$

| Valor de ε_m | Tipo de bem | Exemplo |
|---|---|---|
| ε_m > 1 | **Bem de luxo** (elástico superior) | Viagens internacionais, joias |
| 0 < ε_m < 1 | **Bem normal** (elástico inferior) | Alimentos básicos |
| ε_m < 0 | **Bem inferior** | Transporte público (para renda alta), margarina |

!!! tip "Lei de Engel"
    **Ernst Engel** (1857) observou empiricamente que a **proporção da renda gasta em alimentos** decresce à medida que a renda aumenta — os alimentos são bens normais mas com elasticidade-renda < 1. Isso implica que países mais ricos tendem a ter setores agrícolas relativamente menores (% do PIB).

### 4.3 Elasticidade-Preço Cruzada

Mede como a quantidade demandada do bem i responde a variações no preço do bem j:

$$\varepsilon_{ij} = \frac{\% \Delta Q_i}{\% \Delta p_j} = \frac{\partial Q_i}{\partial p_j} \cdot \frac{p_j}{Q_i}$$

- **ε_ij > 0:** bens **substitutos** (café e chá: aumento do preço do café → mais chá demandado)
- **ε_ij < 0:** bens **complementares** (carro e gasolina: aumento do preço da gasolina → menos carros demandados)
- **ε_ij = 0:** bens **independentes**

### 4.4 Excedente do Consumidor

O **excedente do consumidor (EC)** é a diferença entre o que os consumidores estariam dispostos a pagar e o que efetivamente pagam. Geometricamente, é a área abaixo da curva de demanda e acima do preço de mercado. Medida de **bem-estar** crucial para análise de políticas públicas, impostos e regulação.

---

## 🎯 Top 5 — O que mais cai no CACD sobre Demanda do Consumidor

1. **Decomposição de Slutsky** — Separar efeito substituição e efeito renda, identificar bens normais, inferiores e de Giffen. Dominar os sinais de cada efeito em cada caso.

2. **Elasticidade-preço e receita total** — Relação entre |ε| e variação na receita: cobrada em questões sobre poder de monopólio, tributação e política agrícola.

3. **Elasticidade-renda e classificação de bens** — Distinguir bem de luxo, normal e inferior; aplicar a Lei de Engel a questões de desenvolvimento.

4. **Condição de ótimo do consumidor** — TMS = razão de preços; saber derivar a curva de demanda individualmente e agregar para a demanda de mercado.

5. **Curvas de indiferença** — Propriedades, interpretação da TMS, casos especiais (substitutos/complementares perfeitos). Frequentemente cobrado em questões interpretativas com gráficos.
