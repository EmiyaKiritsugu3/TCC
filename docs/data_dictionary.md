# Dicionário de dados — `data/processed/matches_processed.csv`

Base limpa gerada por `scripts/build_processed.py` a partir de
`data/raw/campeonato-brasileiro-full.csv` (ver `data/raw/FONTE.md` e
`docs/auditoria_fase1.md`). Uma linha por partida válida, Série A 2006–2024.

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---:|---|
| `match_id` | texto | Sim | ID original da partida na fonte (`ID`). Chave única. |
| `season` | inteiro | Sim | Temporada atribuída por intervalo entre partidas (não por ano civil — a temporada 2020 termina em 25/02/2021). 2006–2024. |
| `date` | data ISO (`YYYY-MM-DD`) | Sim | Data da partida. |
| `round` | inteiro | Sim | Rodada **original** da fonte (`rodata`, com typo no original). Jogos reagendados mantêm a rodada original. |
| `home_team` | texto | Sim | Clube designado mandante (nome da fonte, sem acentos). |
| `away_team` | texto | Sim | Clube designado visitante. Diferente de `home_team` em todas as linhas. |
| `home_goals` | inteiro ≥ 0 | Sim | Gols do mandante. Nunca preenchido a partir de ausente. |
| `away_goals` | inteiro ≥ 0 | Sim | Gols do visitante. |
| `result` | `H`/`D`/`A` | Sim | Resultado recalculado do placar: vitória mandante / empate / vitória visitante. |
| `home_points` | 0/1/3 | Sim | Pontos do mandante (3/1/0). |
| `away_points` | 0/1/3 | Sim | Pontos do visitante. |
| `stadium` | texto | Não | Arena da fonte (espaços removidos na limpeza). |
| `source` | texto | Sim | Rastreabilidade: `Brasileirao_Dataset commit 15f027c (acesso 2026-10-28)`. |

## Regras aplicadas (seção 15 da spec)

1. Data inválida, placar ausente/não-numérico/negativo/fracionário, mandante = visitante ou clube vazio → linha excluída e contabilizada em `quality_report.json`.
2. Placar ausente **nunca** vira 0–0.
3. Duplicatas (`match_id`, linha integral ou tripla data/mandante/visitante): mantém a primeira, registra o resto. Na base atual: zero ocorrências.
4. `result` e pontos vêm do placar; o campo `vencedor` da fonte serve só para auditoria.
5. Filtro de recorte: 2006–2024 (1.566 linhas de 2003–2005 e 2025 excluídas).

## Casos conhecidos

- **2016:** 379 partidas. Falta Chapecoense × Atlético-MG (rodada 38, 11/12/2016), cancelada após a tragédia do voo.
- **2020:** 380 partidas de 08/08/2020 a 25/02/2021 (COVID-19).
- **Aliases:** nenhum aplicado. Barueri (só 2009) e Grêmio Prudente (só 2010) são a mesma franquia renomeada entre temporadas — mantidas separadas por temporada.
- **Nomes sem acento** na fonte (ex.: `Gremio`, `Ceara`, `Sao Paulo`) — preservados como estão.
