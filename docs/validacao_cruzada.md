# Validação cruzada — base primária × OpenFootball (2018–2024)

**Objetivo:** confrontar a base primária (`adaoduque`, sem licença explícita)
com fonte independente de domínio público (OpenFootball, CC0-1.0), como
triangulação metodológica.

**Como reproduzir:** `python3 scripts/validate_cross.py`
(parser em `src/openfootball.py`; mapa de nomes em `MAPA_TIMES`).

## Resultado (2026-10-28)

| Ano | Base | OF | Em ambas | Placar igual | Diverg. placar |
|---|---:|---:|---:|---:|---:|
| 2018 | 380 | 380 | 380 | 380 | 0 |
| 2019 | 380 | 380 | 380 | 380 | 0 |
| 2020 | 380 | 380 | 380 | 380 | 0 |
| 2021 | 380 | 380 | 380 | 380 | 0 |
| 2022 | 380 | 380 | 380 | 380 | 0 |
| 2023 | 380 | 380 | 379 | 379 | 0 |
| 2024 | 380 | 380 | 380 | 380 | 0 |

**2.659 de 2.660 partidas idênticas em data, mando e placar (99,96%). Zero
divergências de placar ou de mando.**

## A única exceção (explicada, não é erro)

Botafogo-RJ × Athletico-PR 1–1, 28ª rodada de 2023: base primária registra
**22/10/2023**, OpenFootball registra **21/10/2023**. É o "jogo de dois dias"
do Nilton Santos — iniciado no sábado (21/10), interrompido por quedas de
energia e concluído no domingo (22/10). Fontes: ge.globo em 22/10/2023
("empate ... em jogo de dois dias") e globoplay ("jogo que durou dois dias").
Mantida a data da base primária (conclusão), com esta nota. Codificada como
`KNOWN_DATE_EXCEPTIONS` em `scripts/validate_cross.py`.

## Limites

- O OpenFootball só cobre a Série A de 2018 em diante — 2006–2017 dependem
  só da auditoria interna (zero duplicatas/divergências, cf. `auditoria_fase1.md`).
- Nomes de clubes diferem entre fontes (ex.: `CA Paranaense` × `Athletico-PR`);
  o mapa completo está em `src/openfootball.py::MAPA_TIMES` (51 variantes → 30 canônicos).
- **Decisão do autor (2026-10-28):** mapa aprovado — `América MG`/`Mineiro`,
  `Grêmio Porto Alegre`/`FBPA`, `RB`/`Red Bull Bragantino` e `CA`/`Athletico
  Paranaense` tratados como o mesmo clube em cada caso. O fechamento de 100%
  dos pareamentos valida empiricamente o mapa.
