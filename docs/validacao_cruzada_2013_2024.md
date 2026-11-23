# Validação cruzada 2013–2024 (OpenFootball, CC0)

```text
base: data/processed/matches_processed_2013_2024.csv
 ano | base   OF ambas placar_ok div só_base só_OF
2018 |  380  380   380       380   0       0     0
2019 |  380  380   380       379   1       0     0
  -- diverg (1):
      date     home_team   away_team  home_goals_base  away_goals_base  home_goals_of  away_goals_of
2019-12-08 Internacional Atletico-MG                0                0              2              1
2020 |  380  380   380       380   0       0     0
2021 |  380  380   380       380   0       0     0
2022 |  380  380   380       380   0       0     0
2023 |  380  380   379       379   0       1     1  <- exceção conhecida (jogo de dois dias)
2024 |  380  380   380       380   0       0     0
RESULTADO: DIVERGÊNCIAS ACIMA — investigar
```

## Nota de auditoria (2026-11-23)

A divergência de placar de **2019-12-08, Internacional × Atlético-MG** é
conhecida: a base MIT registra 0–0; as fontes oficiais (ge.globo e ESPN)
registram **2–1 para o Internacional**. O artigo a mantém como limitação
explícita em vez de alterar a fonte bruta.

Impacto estimado da correção: 1 partida em 4.559 (0,02%); o Pollard agregado
permanece 63,0%, a mudança de nível permanece 65,0% → 61,0% e o coeficiente
de interação do Poisson permanece −0,128. O ICC passaria de 2,2% para 2,3%
(97,8% → 97,7% de variação equipe-temporada). As conclusões qualitativas não
mudam.
