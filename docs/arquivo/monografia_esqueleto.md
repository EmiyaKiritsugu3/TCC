# Esqueleto da monografia (seguir a ordem da spec §20; [TODO] = parte humana)

## 1. Introdução
- Contexto: vantagem de jogar em casa no futebol; lacuna: série histórica longa + sistema reproduzível.
- Problema: qual foi a magnitude da vantagem em 2006–2024 e como variou por temporada?
- Objetivos (§5 da spec) + delimitação (§7). [TODO: justificar escolha do tema]
- Estrutura do trabalho.

## 2. Referencial teórico
- Vantagem de jogar em casa; índice de Pollard (1986) com fórmula.
- Comparar definições da literatura (não misturar escalas — spec §10.4).
- Análise de dados, estatística descritiva, visualização da informação.
- [TODO: redigir a partir de `docs/arquivo/referencial_fichamentos.md` (fichas 1–5 prontas;
  Pollard via *apud* + Matos 2020 como âncora legível)]

## 3. Metodologia
- Classificação (§9.1): aplicada, quantitativa, exploratória-descritiva, dados secundários.
- Fonte primária + plano B + commit/data de acesso (`data/raw/FONTE.md`).
- Validação cruzada OpenFootball CC0 2018–2024: 99,96% (`docs/validacao_cruzada.md`).
- Critérios de inclusão/exclusão (§9.3); regras de limpeza (§15); casos 2016 e 2020.
- Fórmulas (§10). [TODO: amostra de confronto CBF, se o orientador exigir]

## 4. Análise e desenvolvimento do sistema
- Arquitetura: pipeline bruto → processado → métricas → Streamlit (§14).
- Requisitos RF01–RF11 e telas (resumir; prints do `app.py` como evidência).
- Testes: 12 automatizados + caso de referência §16.1 (Pollard = 50%).

## 5. Resultados e discussão (números prontos — só redigir em torno)
- Período: mandante 49,0% · empate 26,8% · visitante 24,1% (Fig. 1).
- Gols: casa 1,49 × fora 1,00 (Fig. 4). → responde perguntas 1–2.
- Pollard geral **63,7%** → H1 confirmada; anual **58,2% (2017)–69,5% (2018)** → H2 sustentada (Fig. 2, Tab. 1). → perguntas 3–4.
- Comparar com literatura fichada. Sem alegação causal.

## 6. Conclusão
- Resposta à pergunta; contribuição (recorte + pipeline reproduzível + dashboard);
- Limitações (§19 — declarar todas); trabalhos futuros (Spearman, Séries B–D, dados de elenco).

## 7. Referências + Apêndices
- 6 iniciais na spec §22 (confirmar dados bibliográficos). [TODO: norma do curso]
- Apêndices: `docs/data_dictionary.md`, casos de teste, instruções (`README.md`).

**Pós-orientador:** aplicar as 5 decisões de `docs/resumo_orientador.md` aqui antes de redigir.
