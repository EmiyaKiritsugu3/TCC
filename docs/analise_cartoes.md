# Cartões e arbitragem — análise descritiva (2013–2024)

Fonte: BrazilianFootball/Data (MIT), extraída dos borderôs da CBF.
Cada cartão é contado para a equipe que o recebeu; cartões não atribuídos
são registrados no controle de qualidade.

## Cartões por temporada

| Temporada | Jogos | Amarelos casa | Amarelos fora | Diferença (IC 95%) | Vermelhos casa | Vermelhos fora |
|---|---:|---:|---:|---|---:|---:|
| 2013 | 380 | 2,06 | 2,37 | -0,31 (-0,46 a -0,16) | 0,04 | 0,09 |
| 2014 | 380 | 2,14 | 2,31 | -0,16 (-0,34 a +0,01) | 0,09 | 0,12 |
| 2015 | 380 | 2,22 | 2,72 | -0,50 (-0,68 a -0,32) | 0,08 | 0,19 |
| 2016 | 379 | 2,06 | 2,50 | -0,44 (-0,61 a -0,27) | 0,07 | 0,15 |
| 2017 | 380 | 2,13 | 2,60 | -0,46 (-0,66 a -0,28) | 0,08 | 0,10 |
| 2018 | 380 | 2,30 | 2,55 | -0,25 (-0,41 a -0,07) | 0,09 | 0,16 |
| 2019 | 380 | 2,10 | 2,28 | -0,18 (-0,36 a +0,01) | 0,09 | 0,16 |
| 2020 | 380 | 2,24 | 2,13 | +0,11 (-0,06 a +0,29) | 0,13 | 0,14 |
| 2021 | 380 | 2,21 | 2,25 | -0,04 (-0,22 a +0,14) | 0,10 | 0,10 |
| 2022 | 380 | 2,22 | 2,62 | -0,41 (-0,60 a -0,22) | 0,11 | 0,16 |
| 2023 | 380 | 2,54 | 2,72 | -0,18 (-0,36 a +0,00) | 0,14 | 0,12 |
| 2024 | 380 | 2,42 | 2,71 | -0,28 (-0,47 a -0,10) | 0,16 | 0,16 |

## Diferença-em-diferenças 2019 → 2020

- Amostra completa: **+0,346** cartões por jogo (EP 0,179; IC 95% -0,005 a +0,697; n=760).
- Equipes presentes nos dois anos: **+0,337** (EP 0,181; IC 95% -0,018 a +0,693; n=480).

Coeficiente positivo = a diferença casa−fora **aumentou** em 2020: o
mandante deixou de receber relativamente menos cartões. Em 2019 a
diferença era -0,18; em 2020, +0,11; a mudança bruta é +0,29 e a
estimativa com efeitos fixos de equipe é +0,35.

O IC 95% clusterizado inclui zero; a mudança é sugestiva, mas não estatisticamente conclusiva ao nível de 5%.

## Leitura

- Com torcida (2013–2019), o mandante recebia, em média, cerca de
  0,3 cartão amarelo a menos que o visitante por jogo.
- Em 2020, sem torcida, a diferença ficou próxima de zero ou levemente
  positiva.
- Em 2021–2024, com o retorno do público, a diferença voltou a ser
  negativa, embora com oscilação.
- O padrão é compatível com pressão da torcida sobre decisões de
  arbitragem, mas não identifica causalidade: VAR, calendário, protocolos
  e comportamento dos jogadores também mudaram.

## Cartões por falta (2018+)

| Temporada | Jogos com faltas | Amarelos/falta casa | Amarelos/falta fora |
|---|---:|---:|---:|
| 2018 | 211 | 0,156 | 0,167 |
| 2019 | 168 | 0,093 | 0,119 |
| 2020 | 374 | 0,143 | 0,138 |
| 2021 | 375 | 0,145 | 0,154 |
| 2022 | 373 | 0,165 | 0,196 |
| 2023 | 378 | 0,174 | 0,193 |
| 2024 | 211 | 0,201 | 0,229 |

A cobertura de faltas é parcial em 2018–2019 e 2024; a comparação
de cartões por falta serve como robustez, não como teste definitivo.

## Limitações

- Cartão é decisão do árbitro, mas também reflete comportamento do jogador.
- 2020 tem pandemia, calendário atípico e protocolos; VAR já existia em 2019.
- 2006–2012 não têm cartões nesta fonte.
- A série 2013–2024 tem 1 cartão não atribuído em 2022 (formato quebrado).
- Não há pênaltis nem cartões por arbítrio separados por tipo; o teste do
  canal arbitral é indireto.

## Reprodução

```bash
# Base primária (matches_processed.csv não é versionado)
python3 scripts/fetch_raw.py
python3 scripts/build_processed.py
PYTHONPATH=src python3 scripts/fetch_cards.py
PYTHONPATH=src python3 scripts/build_cards.py
# Opcional: cartões por falta (context_clean.csv exige o pipeline externo)
PYTHONPATH=src python3 scripts/build_external.py
PYTHONPATH=src python3 scripts/analyze_cards.py
```
