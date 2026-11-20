# Fontes externas para público e arbitragem — relatório de viabilidade

**Data:** 20/11/2026  
**Objetivo:** verificar se existem bases públicas capazes de acrescentar
público por partida e arbitragem à base do TCC (2006–2024), e testar a
junção com os 7.219 jogos já validados.

## 1. Fontes avaliadas

| Fonte | Cobertura | Público | Árbitro | Cartões/faltas | Acesso |
|---|---|---|---|---|---|
| Base dos Dados / Transfermarkt (`brasileirao_serie_a`) | 2003–2024 | `publico`, `publico_max` | `arbitro` | `faltas_*`, chutes, escanteios (faltas só 2018+) | BigQuery público; projeto GCP |
| FBref | 2014–2024 | `Attendance` | `Referee` | cartões e estatísticas | scraping com restrições |
| CBF borderôs/súmulas | 2003–2024 | público pagante, renda | árbitro | cartões, ocorrências | PDFs/HTML oficiais |
| BrazilianFootball/Data (MIT) | 2013–2025 | não | sim (PDFs) | cartões, gols, escalações | GitHub/DOI |
| football-data.co.uk | 2012–2026 | não | não | odds e resultados | CSV gratuito |
| Transfermarkt-datasets (DuckDB) | 2025–2026 (BRA1) | `attendance` | `referee` | eventos | repositório/Kaggle |
| worldfootball.net | 2006–2025 | sim | sim | cartões | scraping |
| ClubElo | 1939– | não | não | Elo | site gratuito |
| Open-Meteo | 1940– | não | não | clima | API CC BY 4.0 |

A tabela da Base dos Dados é a única que combina **público + árbitro +
faltas/chutes + classificação** no mesmo registro, cobrindo o recorte
histórico. É a fonte primária recomendada.

## 2. Base dos Dados: cobertura

Tabela: `basedosdados.mundo_transfermarkt_competicoes.brasileirao_serie_a`.  
Consulta: 7.126 linhas, 35 colunas, acesso em 20/11/2026.

| Temporada | Jogos | Com BD | Público | Público = 0 | Árbitro | Faltas |
|---|---:|---:|---:|---:|---:|---:|
| 2006 | 380 | 376 | 0 | 0 | 0 | 0 |
| 2007 | 380 | 380 | 380 | 4 | 380 | 0 |
| 2008 | 380 | 380 | 380 | 217 | 380 | 0 |
| 2009 | 380 | 380 | 380 | 6 | 380 | 0 |
| 2010 | 380 | 380 | 380 | 1 | 380 | 0 |
| 2011 | 380 | 380 | 380 | 2 | 380 | 0 |
| 2012 | 380 | 380 | 380 | 0 | 380 | 0 |
| 2013 | 380 | 380 | 380 | 0 | 380 | 0 |
| 2014 | 380 | 380 | 380 | 5 | 380 | 0 |
| 2015 | 380 | 380 | 380 | 6 | 380 | 0 |
| 2016 | 379 | 379 | 379 | 0 | 379 | 0 |
| 2017 | 380 | 380 | 380 | 3 | 380 | 0 |
| 2018 | 380 | 380 | 380 | 0 | 380 | 211 |
| 2019 | 380 | 380 | 380 | 1 | 380 | 168 |
| 2020 | 380 | 380 | 380 | 380 | 380 | 374 |
| 2021 | 380 | 380 | 380 | 218 | 380 | 375 |
| 2022 | 380 | 380 | 380 | 3 | 380 | 373 |
| 2023 | 380 | 380 | 380 | 12 | 380 | 378 |
| 2024 | 380 | 286 | 286 | 0 | 286 | 211 |

Leituras:

- **2006 não tem público nem árbitro** na tabela; o Join ainda usa 376 jogos para outras variáveis.
- **2008 tem 217 zeros** e média de público muito baixa (7.844): provavelmente
  ausência codificada como zero, não portões fechados. Precisa de limpeza.
- **2020 tem 380 zeros**: são portões fechados (COVID-19), não missing.
- **2021 tem 218 zeros**: retorno parcial de público, com parte dos jogos sem torcida.
- **2024 está incompleto** (286/380) no snapshot; usar FBref para completar.
- **Faltas só existem a partir de 2018** (2.090 jogos), e ainda com falhas em 2018–2019.
- Não há colunas de cartões amarelos/vermelhos; para isso, usar FBref,
  CBF súmulas ou BrazilianFootball/Data.

## 3. FBref 2024

Página: `https://fbref.com/en/comps/24/2024/schedule/2024-Serie-A-Scores-and-Fixtures`

- 380 partidas;
- 376 com público (99,0%);
- 253 com árbitro (66,6%);
- 380 com estádio.

O FBref fica atrás de Cloudflare para requisições automatizadas. A extração
foi feita no navegador (ver `data/external/fbref/FONTE.md`) e normalizada
por `scripts/parse_fbref.py`.

## 4. Junção com a base do TCC

A junção usa **temporada + mandante + visitante + placar**, não a data,
porque as fontes divergem em jogos remarcados. Nomes passam por um mapa
de aliases; Barueri/Grêmio Prudente (2010) é tratado como a mesma franquia.

- **7.121 de 7.219 partidas (98,6%)** receberam alguma linha da Base dos Dados.
- 2024 responde pelas 94 partidas sem correspondência (a tabela tem 286 jogos).
- 2006 tem 4 partidas sem correspondência.
- 2010 fecha 380/380 depois do alias Barueri → Grêmio Prudente.

## 5. Validação do público (FBref × Base dos Dados, 2024)

- 380 partidas do FBref;
- 380 com correspondência por times + placar;
- 286 pares com público nas duas fontes;
- **243 idênticos (85,0%)**;
- **248 com diferença ≤ 100 (86,7%)**;
- **271 com diferença ≤ 1.000 (94,8%)**;
- diferença média absoluta: **316 espectadores**.

As diferenças provavelmente vêm de critérios distintos (público pagante vs.
público total) e de alguns jogos com arredondamento/erro. Para o TCC, o
público deve ser tratado como **proxy**, não como medida exata.

## 6. Correlações preliminares

Com a base externa unida (sem limpeza fina de 2008/2020/2021):

| Relação | Spearman | n |
|---|---:|---:|
| HA (casa − fora) × público médio por equipe-temporada | **0,025** | 360 |
| Pontos × público médio por equipe-temporada | **0,439** | 360 |
| Saldo de gols por partida × público | **0,071** | 6.745 |
| Faltas (casa − fora) × público | **−0,028** | 2.090 |

Leitura: o público médio está associado à **força do clube** (pontos, 0,44),
mas não à **vantagem casa−fora** (0,025). No nível de partida, a associação
com o saldo de gols é fraca (0,07), e a diferença de faltas não se move com
o público (−0,03). Isso **não refuta** a hipótese da torcida: o público médio
é dominado pelo tamanho do clube e a variação relevante é dentro de
equipe-temporada, além do experimento natural de 2020–2021. Mas é um sinal
de que a análise precisa ser bem desenhada, não apenas correlacionar
público com resultado.

## 7. Limitações e cuidados

- **Não usar `publico_max` como público do jogo**: é máximo/capacidade.
- **2008**: zeros provavelmente são missing; não tratar como portões fechados.
- **2020–2021**: zeros são reais (portões fechados/parciais), não missing.
- **2024**: completar com FBref antes de usar.
- **Faltas**: só 2018+, e com lacunas; não serve para a série toda.
- **Cartões**: não estão na tabela; buscar FBref/CBF/BrazilianFootball.
- **Arbitragem**: nomes precisam de normalização; um mesmo árbitro pode
  aparecer com grafias diferentes.
- **Público**: critérios podem variar (pagante vs. total); validar por amostra
  com borderôs da CBF.
- **Causalidade**: público é endógeno (depende do adversário, fase, preço,
  clima). Usar efeitos fixos de equipe-temporada e o choque de 2020–2021;
  não afirmar que a torcida causa o resultado.

## 8. Recomendação

1. Usar a **Base dos Dados como fonte primária** de público/árbitro para
   2007–2024, com limpeza documentada de 2008 e 2020–2021.
2. Usar o **FBref 2024** para completar a temporada e validar o público.
3. Fazer uma **amostra de 20–30 borderôs da CBF** para estimar a taxa de
   erro do público e escolher o critério (pagante vs. total).
4. Só depois incorporar `publico` à matriz de correlação e ao dashboard,
   com uma aba/seção de qualidade da base externa.
5. Para cartões e arbitragem fina, usar FBref (2014–2024) ou
   BrazilianFootball/Data (2013–2025); a Base dos Dados cobre faltas,
   não cartões.

## 9. Reprodução

```bash
# 1. Base dos Dados (requer gcloud ADC + projeto de billing)
python3 scripts/fetch_basedosdados.py --project SEU_PROJETO

# 2. FBref: extrair a tabela no navegador e salvar o JSON; depois:
python3 scripts/parse_fbref.py --input .playwright-mcp/fbref_2024.json

# 3. Junção e validação
python3 scripts/join_external.py

# 4. Resumo
python3 scripts/analyze_external.py
```

Os CSVs externos ficam **locais** (`data/external/...`) e não são
versionados; os scripts, metadados e este relatório são versionados.

## 10. Licença e proveniência

- **Base dos Dados / Transfermarkt:** consultar os termos da Base dos Dados
  e do Transfermarkt; usar dados derivados, citar a fonte e não redistribuir
  o bruto.
- **FBref / Sports Reference:** uso acadêmico com citação; não criar base
  concorrente nem redistribuir o bruto; respeitar rate limit.
- **CBF:** documentos públicos; verificar termos de uso e citar.
- **football-data.co.uk:** gratuito; citar.
- **Open-Meteo:** CC BY 4.0; atribuir.
