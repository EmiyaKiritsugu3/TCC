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
| CBF borderôs/súmulas | 2013–2024 (PDF eletrônico); 2003–2012 sem PDF eletrônico | público pagante, renda | árbitro | cartões, ocorrências | PDFs/HTML oficiais |
| BrazilianFootball/Data (MIT) | 2013–2025 | não | sim (PDFs) | cartões, gols, escalações | GitHub/DOI |
| football-data.co.uk | 2012–2026 | não | não | odds e resultados | CSV gratuito |
| Transfermarkt-datasets (DuckDB) | 2025–2026 (BRA1) | `attendance` | `referee` | eventos | repositório/Kaggle |
| worldfootball.net | 2006–2025 | sim | sim | cartões | scraping |
| ClubElo | 1939– | não | não | Elo | site gratuito |
| Open-Meteo | 1940– | não | não | clima | API CC BY 4.0 |

A tabela da Base dos Dados é a única que combina **público + árbitro +
faltas/chutes + classificação** no mesmo registro, cobrindo o recorte
histórico. É a fonte primária recomendada.

Os borderôs eletrônicos da CBF começam em 2013; 2006–2012 não estão no mesmo
acervo e exigiriam fontes secundárias (RSSSF, Wikipedia ou arquivos de imprensa).

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
- **2008 tem 217 zeros** e média de público muito baixa (7.844) se contados:
  os zeros estão espalhados por todos os clubes e meses, e a média dos 163
  jogos não-zero é 18.287. São tratados como ausência codificada como zero,
  não portões fechados.
- **2020 tem 380 zeros**: são portões fechados (COVID-19), não missing.
- **2021 tem 218 zeros**: retorno parcial de público, com parte dos jogos sem torcida.
- **2024 está incompleto** (286/380) no snapshot; usar FBref para completar.
- **Faltas só existem a partir de 2018** (2.090 jogos), e ainda com falhas em 2018–2019.
- Não há colunas de cartões amarelos/vermelhos; para isso, usar FBref,
  CBF súmulas ou BrazilianFootball/Data.

### Cartões por partida (BrazilianFootball/Data)

O repositório **BrazilianFootball/Data** (MIT, DOI `10.5281/zenodo.15207727`)
oferece cartões amarelos e vermelhos por partida da Série A de 2013 a 2025,
extraídos dos borderôs da CBF. A estrutura é JSON, com listas de cartões por
jogo; a cobertura é de 380 jogos por temporada (2016: 379). Para o TCC,
usamos 2013–2024 e mantemos os arquivos brutos locais; a análise está em
`docs/analise_cartoes.md`.

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

## 6. Resultados da base limpa

A análise final, com a limpeza de 2008 e o complemento do FBref em 2024,
está em **`docs/analise_publico_arbitragem.md`**. Resumo:

| Relação | Spearman | n |
|---|---:|---:|
| HA (casa − fora) × público médio por equipe-temporada | **0,068** | 360 |
| HA × público médio, sem 2020–2021 | **−0,010** | 320 |
| Pontos × público médio por equipe-temporada | **0,461** | 360 |
| Saldo de gols por partida × público (bruto) | **0,079** | 6.618 |
| Saldo × público, controlando equipe-temporada e rank pré-jogo | **−0,042** | 6.618 |

Leitura: o público médio é um **proxy de tamanho/força do clube** (pontos,
0,46), mas não da vantagem casa−fora (0,07; −0,01 sem as temporadas
pandêmicas). No nível de partida, a associação bruta positiva (0,08) é
confundida pela composição de confrontos: controlando equipe-temporada e
força pré-jogo, ela fica levemente negativa (−0,04). Jogos de maior público
tendem a ser contra adversários mais fortes, e não a favor do mandante.

O contraste de 2020 é o achado mais forte: o Pollard cai de 64,9%
(2007–2018) para 60,2% com portões fechados, mas **não desaparece**; em
2022–2024, com público de volta, fica em 60,6%. O retorno da torcida não
trouxe a vantagem de volta ao patamar pré-2019. Isso reforça a leitura
multifatorial do TCC e a cautela contra atribuir a queda à torcida.

A arbitragem tem 6.821 jogos e 177 árbitros, mas a identidade do árbitro
não mede viés: a faixa de vitória do mandante entre árbitros com 40+ jogos
(40,8%–67,4%) é compatível com ruído (1 de 50 fora de ±2 DP; esperado 2,3).
Com cartões a partir de 2013 (BrazilianFootball/Data) e sem pênaltis, o teste
do canal arbitral é parcial: dá para comparar cartões, mas não decisões
discricionárias completas.

## 7. Limitações e cuidados

- **Não usar `publico_max` como público do jogo**: é máximo/capacidade.
- **2008**: zeros provavelmente são missing; não tratar como portões fechados.
- **2020–2021**: zeros são reais (portões fechados/parciais), não missing.
- **2024**: completado com o FBref; 4 jogos ficaram sem público e 18 sem árbitro.
- **Faltas**: só 2018+, e com lacunas; não serve para a série toda.
- **Cartões**: a Base dos Dados não tem; usar BrazilianFootball/Data (2013–2024, MIT) ou as súmulas da CBF. Ver `docs/analise_cartoes.md`.
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
3. Incorporar ao TCC apenas o que a análise sustenta: público como proxy de
   tamanho de clube, contraste de 2020 e ausência de associação com HA.
   Não tratar público como medida de torcida nem a matriz como causal.
4. Não colocar arbitragem na matriz: a identidade do árbitro não mede viés;
   usar como cobertura/limitação e, se houver, uma nota descritiva.
5. Fazer uma **amostra de 20–30 borderôs da CBF** para estimar a taxa de
   erro do público e escolher o critério (pagante vs. total).
6. Para cartões e pênaltis, usar FBref (2014–2024) ou
   BrazilianFootball/Data (2013–2025); a Base dos Dados cobre faltas,
   não cartões.

## 9. Reprodução

```bash
# 1. Base dos Dados (requer gcloud ADC + projeto de billing)
PYTHONPATH=src python3 scripts/fetch_basedosdados.py --project SEU_PROJETO

# 2. FBref: extrair a tabela no navegador e salvar o JSON; depois:
PYTHONPATH=src python3 scripts/parse_fbref.py --input .playwright-mcp/fbref_2024.json

# 3. Junção bruta e validação
PYTHONPATH=src python3 scripts/join_external.py

# 4. Base limpa (2008 como ausente; FBref completa 2024)
PYTHONPATH=src python3 scripts/build_external.py

# 5. Análise final
PYTHONPATH=src python3 scripts/analyze_external.py
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
