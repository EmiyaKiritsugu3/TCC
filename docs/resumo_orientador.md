# Resumo executivo para o orientador — TCC vantagem de jogar em casa

**Aluno:** [nome] · **Curso:** Sistemas de Informação · **Data:** 28/10/2026
**Título proposto:** *Análise estatística da vantagem de jogar em casa no Campeonato
Brasileiro Série A: desenvolvimento de um dashboard interativo para análise de
resultados históricos* (alternativo curto na spec, §2).

## 1. O que é

Pesquisa quantitativa aplicada + software: dashboard interativo (Streamlit) sobre
7.219 partidas da Série A 2006–2024, com proporções de resultados, médias de gols
e índice de Pollard por temporada e por equipe. Sem previsão, sem IA, sem apostas.

## 2. Status (software pronto, dados validados)

- Base primária auditada: zero duplicatas, zero placares ausentes, zero divergências
  vencedor×placar; 2016 com 379 jogos (Chapecoense×Atlético-MG cancelada) e 2020
  estendida até 25/02/2021 — ambos documentados.
- Pipeline reproduzível + 12 testes automatizados passando.
- **Validação cruzada:** confronto com OpenFootball (domínio público, CC0) em
  2018–2024 → 2.659/2.660 partidas idênticas, zero divergências de placar.
- Fonte sem licença explícita → adotado plano B: CSV bruto não versionado,
  download pinado no build + citação (ver `data/raw/FONTE.md`).

## 3. Resultados preliminares (respondem à pergunta de pesquisa)

- Mandante venceu **49,0%**, empates 26,8%, visitante 24,1%; gols 1,49 × 1,00.
- **Pollard geral: 63,7%** → H1 (> 50%) confirmada no período.
- Pollard anual **58,2% (2017) – 69,5% (2018)** → H2 (variação entre temporadas) sustentada.

## 4. Decisões solicitadas (spec §23)

1. Aprovar recorte 2006–2024 e título.
2. Aceitar dashboard + pesquisa quantitativa como artefato de SI.
3. Confirmar fonte e plano B de licença.
4. **Incluir ou não a correlação de Spearman** (tendência) — hoje o trabalho é
   só descritivo; incluir vira análise exploratória adicional.
5. Formato exigido de projeto/TCC e avaliação do software.

## 5. Riscos assumidos e mitigação

Escopo fechado (§7 da spec: fora previsão, IA, apostas, Séries B–D); análise
observacional sem alegação causal; nomes de clubes normalizados com tabela de
decisões documentada.
