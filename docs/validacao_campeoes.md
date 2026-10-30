# Validação dos campeões — integridade da base (Sprint 9)

**Método:** `scripts/validate_champions.py` recalcula a classificação de cada
temporada (pontos → vitórias → saldo, critérios CBF) a partir de
`data/processed/matches_processed.csv` e compara com o campeão oficial.

**Resultado (30/10/2026): PASS — 19/19**, com pontuações compatíveis com o
histórico (ex.: Flamengo 90 em 2019; Flamengo 71 × Internacional 70 em 2020;
Palmeiras 70 × Botafogo 68 em 2023). Nenhum topo empatado em pontos.

Isso prova que placares, mandos e a atribuição de temporadas estão corretos em
todas as 19 temporadas — inclusive 2016 (379 jogos) e 2020 (ano-virada).
Complementa a validação cruzada externa (`validacao_cruzada.md`, 2018–2024).
