# Resumo executivo para o orientador — TCC vantagem de jogar em casa

**Aluno:** José Inamar de Medeiros Júnior · **Curso:** Sistemas de Informação · **Data:** 19/11/2026
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
- Pipeline reproduzível + **96 testes automatizados** passando (87 rápidos + 9 de integração).
- Monografia v2 fechada (04/11/2026): Tabela 1 no texto, figuras 1–8 em ordem,
  referências ABNT alfabéticas, apêndices A–D preenchidos; ampliação proativa
  da fundamentação em curso (meta ≥ 5.500 palavras), sem alterar resultados.
- **Validação cruzada:** confronto com OpenFootball (domínio público, CC0) em
  2018–2024 → 2.659/2.660 partidas idênticas, zero divergências de placar.
- Fonte sem licença explícita → adotado plano B: CSV bruto não versionado,
  download pinado no build + citação (ver `data/raw/FONTE.md`).
- **Variáveis contextuais (fase adicional):** `src/context.py` e `src/associations.py`
  com viagem, clássico, estádio, descanso, força e era (Tabela 5 na monografia),
  além de mudança de nível, ICs anuais e vantagem por equipe (Tabela 6).
  Achados principais: a distância não move o índice (63,37% / 63,80% / 63,90%);
  clássicos sem viagem ficam em 58,23%; estádio habitual 64,10% vs. outro 59,40%;
  mandante zebra ainda fica em 55,65%. A série tem mudança de nível pós-2018:
  64,88% em 2006–2018 vs. 61,01% em 2019–2024 (diferença 3,87 p.p.; IC 2,15–5,58).
  Tudo descritivo, sem leitura causal, pendente de validação do orientador.

## 3. Resultados preliminares (respondem à pergunta de pesquisa)

- Mandante venceu **49,0%**, empates 26,8%, visitante 24,1%; gols 1,49 vs. 1,00.
- **Pollard geral: 63,7%** → H1 (> 50%) confirmada no período.
- Pollard anual **58,2% (2017) – 69,5% (2018)** → H2 (variação entre temporadas) sustentada,
  com mudança de nível pós-2018 (64,9% → 61,0%; IC 2,1–5,6).
- Contexto: viagem não é o principal; estádio habitual e força modulam; torcida/arbitragem
  seguem não medidas. A conclusão é multifatorial, não causal.

## 4. Decisões solicitadas (spec §23)

1. Aprovar recorte 2006–2024 e título.
2. Aceitar dashboard + pesquisa quantitativa como artefato de SI.
3. Confirmar fonte e plano B de licença.
4. **Validar a análise exploratória de tendência/mudança de nível e as associações
   contextuais (H3–H5)** — o texto atual já as apresenta como descritivas; falta o
   aval do orientador para mantê-las no depósito.
5. Formato exigido de projeto/TCC e avaliação do software.

## 5. Riscos assumidos e mitigação

Escopo fechado (§7 da spec: fora previsão, IA, apostas, Séries B–D); análise
observacional sem alegação causal; nomes de clubes normalizados com tabela de
decisões documentada.
