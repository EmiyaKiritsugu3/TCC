# Rascunho — Capítulo 4. Análise e desenvolvimento do sistema

> Fatos verificáveis no repositório. Prints do `app.py` entram como figuras.

## 4.1 Arquitetura

Pipeline em camadas separadas (RNF06): `src/load_data.py` (leitura da cópia
imutável), `src/clean_data.py` (padronização e regras da spec §15),
`src/metrics.py` (funções puras dos indicadores), `src/charts.py` (Plotly) e
`app.py` (Streamlit, 4 abas). Base processada em `data/processed/` com relatório
de qualidade em JSON; reprodução por `fetch_raw.py → build_processed.py`.

## 4.2 Tratamento dos dados e cálculos

Conversão de tipos sem coerção silenciosa (placar ausente nunca vira 0–0;
negativos rejeitados); temporada atribuída por intervalo entre partidas (robusta
a reagendamentos, caso 2020); resultado e pontos recalculados do placar. Dois
casos documentados: 2016 com 379 jogos e conclusão da temporada 2020 em 2021.

## 4.3 Requisitos e telas

11 requisitos funcionais (RF01–RF11: carga validada, filtros, indicadores,
séries temporais, gols, equipe, tabela, ajuda metodológica, proveniência,
estado vazio, exportação CSV) e 8 não funcionais (RNF01–RNF08). Telas: visão
geral, evolução histórica, equipes e partidas, metodologia e dados.

## 4.4 Testes

12 testes automatizados (`pytest`): caso de referência da spec (3 partidas →
Pollard 50%), proporções, denominador zero, recorte vazio e regras de limpeza.
Validação cruzada externa (OpenFootball, CC0): 99,96% de concordância.
