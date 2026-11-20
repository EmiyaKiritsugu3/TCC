# 📋 Auditoria de dados — TCC vantagem de casa

**Data:** 20/11/2026  
**Escopo:** base primária 2006–2024, bases externas de público/arbitragem, junção, métricas e artefatos da monografia.  
**Script reproduzível:** `python3 scripts/audit_data.py` (150 verificações).

## ✅ STATUS: PASS com ressalvas

Não há falha crítica. As 150 verificações passaram. As ressalvas são de
cobertura/heterogeneidade das fontes externas e estão documentadas abaixo.

## 1. Base primária (TCC)

| Verificação | Resultado |
|---|---:|
| Linhas carregadas da fonte bruta | 8.785 |
| Linhas excluídas (2003–2005 e 2025) | 1.566 |
| Partidas mantidas | **7.219** |
| Temporadas | 19 (2006–2024) |
| 2016 | 379 (Chapecoense × Atlético-MG cancelada) |
| `match_id` duplicado | 0 |
| Linha integral duplicada | 0 |
| Tripla data/mandante/visitante duplicada | 0 |
| Placares ausentes/negativos/fracionários | 0 |
| Mandante = visitante | 0 |
| Estádio ausente | 0 |
| Rodadas fora de 1–38 | 0 |

Métricas recalculadas:

- Mandante 49,0%; empate 26,8%; visitante 24,1%.
- Gols: 1,49 (casa) e 1,00 (fora).
- Pollard geral: **63,66%**.
- Pontos: 12.554 (casa) e 7.166 (fora).
- Flamengo 2019: 53 pontos em casa, 37 fora, 90 no total, 38 jogos; casa 17-2-0, fora 11-4-4.

**Reprodutibilidade:** `scripts/fetch_raw.py --check` confere o SHA-256 do
arquivo bruto; `scripts/build_processed.py` reproduz a base **byte a byte**
(hash antes = hash depois). O `quality_report.json` registra 8.785 lidas,
1.566 excluídas e 7.219 mantidas.

## 2. Base dos Dados / Transfermarkt

| Verificação | Resultado |
|---|---:|
| Linhas | 7.126 |
| Temporadas | 2006–2024 |
| 2024 | 286 jogos |
| Chave (temporada, mandante, visitante, placar) duplicada | 0 |
| Público negativo | 0 |
| Público > `publico_max` | 0 |
| Público máximo | plausível (< 200 mil) |
| 2008: zeros | 217 |
| 2008: jogos não-zero | 163 |
| 2008: média dos não-zero | 18.287 |
| 2007 / 2009: médias | 17.659 / 17.712 |
| 2020: zeros | 380 (portões fechados) |
| 2021: zeros | 218 (retorno gradual) |
| 2024: zeros | 0 |
| 2024: primeira/última data | 2024-04-13 / 2024-10-27 |

Os 217 zeros de 2008 estão espalhados por **todos os clubes** e por **todos
os meses** (maio a dezembro), e a média dos 163 jogos não-zero é compatível
com 2007/2009. Isso sustenta a decisão de tratá-los como falha de registro,
não como portão fechado.

## 3. FBref 2024

| Verificação | Resultado |
|---|---:|
| Jogos | 380 |
| Público não nulo | 376 |
| Árbitro não nulo | 253 |
| Chave duplicada | 0 |
| Público negativo | 0 |
| Público máximo | plausível (< 200 mil) |

## 4. Junção com a base do TCC

A junção usa **temporada + mandante + visitante + placar**, não a data.
Nomes passam por aliases; Barueri/Grêmio Prudente (2010) é tratado como a
mesma franquia.

| Temporada | Base | Com BD | Observação |
|---|---:|---:|---|
| 2006 | 380 | 376 | 4 divergências de mando/placar |
| 2007–2019 | 380 cada | 380 cada | — |
| 2016 | 379 | 379 | jogo cancelado |
| 2020 | 380 | 380 | — |
| 2021–2023 | 380 cada | 380 cada | — |
| 2024 | 380 | 286 | BD termina em 27/10 |
| **Total** | **7.219** | **7.121 (98,6%)** | — |

**2006 — 4 partidas sem correspondência** (divergência entre fontes, sem
impacto na análise externa porque 2006 não tem público/árbitro):

| Base do TCC | Base dos Dados |
|---|---|
| 2006-05-28 Internacional 1×1 Cruzeiro | 2006-06-04 Cruzeiro 1×1 Internacional |
| 2006-06-01 Corinthians 0×1 Goiás | 2006-07-16 Goiás 0×1 Corinthians |
| 2006-08-12 São Caetano 2×0 Santa Cruz | 2006-08-26 São Caetano 2×1 Santa Cruz |
| 2006-10-25 Corinthians 1×0 Palmeiras | 2006-12-03 Corinthians 0×1 Palmeiras (e 2006-08-06 Palmeiras 1×0 Corinthians) |

**2024 — 94 partidas ausentes na BD**, concentradas em junho (jogos
remarcados) e novembro/dezembro. O FBref completa 90 com público e 76 com
árbitro; 4 ficam sem público e 18 sem árbitro.

Validação do público no overlap de 2024 (286 jogos):

| Métrica | Resultado |
|---|---:|
| Públicos idênticos | 243 (85,0%) |
| Diferença ≤ 100 | 248 (86,7%) |
| Diferença ≤ 1.000 | 271 (94,8%) |
| Diferença média absoluta | 316,3 |

As maiores diferenças são de critério/registro, não necessariamente erro:
Cruzeiro × Botafogo (36.661 vs. 20.701), Atlético-GO × Corinthians
(12.089 vs. 1.208), Fluminense × Atlético-MG (14.202 vs. 5.168) e
Grêmio × Fluminense (16.221 vs. 8.549). O público deve ser tratado como
**proxy**, não medida exata.

## 5. Base externa limpa

| Verificação | Resultado |
|---|---:|
| Partidas | 7.219 |
| Com registro de público | **6.618 (91,7%)** |
| Com árbitro | **6.821 (94,5%)** |
| Zeros totais | 641 |
| Zeros reais (2020 + 2021) | **598** |
| Zeros esparsos (2007–2023) | 43 |
| Faltas (2018+) | 2.090 |
| Público negativo | 0 |
| Público > `publico_max` | 0 |
| 2008: zeros restantes | 0 |
| 2020: zeros | 380 |
| 2021: zeros | 218 |
| 2024: registros de público | 376 |
| 2024: média / mediana | **27.330,9 / 26.582** |
| 2024: sem público | 4 |
| 2024: com árbitro | 362 (95,3%) |
| 2024: sem árbitro | 18 |
| Público: BD / FBref | 6.528 / 90 |
| Público ausente | 601 |

**2024:** a média de 2024 combina 286 jogos da BD (média 26.929,5) e 90 do
FBref (média 28.606,3); os 90 preenchidos são cerca de 6% maiores. A média de
2024 é, portanto, mais incerta do que as temporadas completas da BD.

**2008:** a cobertura parcial (163/380) adiciona ruído às médias
equipe-temporada. Teste de robustez: excluir 2008 muda a correlação
HA × público de 0,043 para −0,009 e pontos × público de 0,786 para 0,777 —
a conclusão (HA ~0, pontos forte) não muda.

## 6. Análise externa

| Verificação | Resultado |
|---|---:|
| Pollard 2007–2018 | 64,94% |
| Pollard 2019 | 62,38% |
| Pollard 2020 | 60,17% |
| Pollard 2021 | 61,83% |
| Pollard 2022–2024 | 60,55% |
| HA × público (equipe-temporada) | 0,068 |
| HA × público sem 2020–2021 | −0,010 |
| Pontos × público | 0,461 |
| Saldo × público (partida, bruto) | 0,079 |
| Quartis: pontos Q1→Q4 | 43,1 → 59,4 |
| Quartis: HA Q1→Q4 | 0,657 / 0,815 / 0,762 / 0,731 |
| Público × pontos (equipe) | 0,786 |
| Público × HA (equipe) | 0,043 |

**Arbitragem:** 6.821 jogos, **177 árbitros** (nomes normalizados entre BD e
FBref), mediana de 14 jogos, máximo de 284. Taxa de vitória do mandante:
48,9%. Entre os 50 árbitros com 40+ jogos, a faixa é 40,8%–67,4%; apenas 1
fica fora de ±2 DP (esperado: 2,3). Sem cartões/pênaltis, não há teste de
viés.

> **Correção aplicada:** a contagem bruta de nomes sugeria 185 árbitros.
> Após unificar acentos, espaços e abreviações do FBref (por exemplo,
> “Paulo Zanovelli” → “Paulo Cesar Zanovelli”), o número correto é **177**.
> O mesmo ajuste elevou o grupo com 40+ jogos de 48 para **50**.

### Cartões (2013–2024)

Fonte separada: **BrazilianFootball/Data** (MIT, DOI `10.5281/zenodo.15207727`),
extraída dos borderôs da CBF. Cobertura: **4.559/4.559** partidas de
2013–2024; **1 cartão não atribuído** (formato quebrado em 2022); 2006–2012
não têm cartões nessa fonte. A análise está em `docs/analise_cartoes.md`.
Em 2019, o mandante recebia 0,18 amarelo a menos que o visitante; em 2020,
+0,11; a mudança com efeitos fixos de equipe é **+0,35** (IC 95% 0,03–0,67).
O padrão é compatível com o canal da arbitragem, mas não prova causalidade.

## 7. Validações independentes

| Validação | Resultado |
|---|---|
| OpenFootball 2018–2024 | **2.659/2.660** placares idênticos; 1 exceção de data conhecida (jogo de dois dias em 2023) |
| Campeões recalculados | **19/19** |
| Testes automatizados | **104 passed** |
| Auditor da monografia | **tudo confere** |

## 8. Achados

### 🔴 Críticos

Nenhum.

### ⚠️ Médios (documentados)

1. **2006:** 4 partidas divergem entre a base primária e a BD (mando, data ou
   placar). Não afetam a análise externa porque 2006 não tem público/árbitro.
2. **2024:** a BD termina em 27/10; 94 jogos foram completados pelo FBref.
   Os 90 com público têm média ~6% maior que os 286 da BD; a média de 2024 é
   mais incerta.
3. **2008:** cobertura parcial (163/380); as médias equipe-temporada de 2008
   são mais ruidosas, mas a conclusão de HA ~0 é robusta à exclusão de 2008.
4. **Público:** FBref e BD divergem em 15% dos jogos de 2024; usar como proxy.
5. **Arbitragem:** a identidade do árbitro não mede decisões; cartões,
   pênaltis e faltas por árbitro não estão na base.
6. **Faltas:** só existem a partir de 2018 e com lacunas; não servem para a
   série completa.

### ✅ Aprovados

- Proveniência e SHA-256 do arquivo bruto.
- Reconstrução byte a byte da base processada.
- Contagem, unicidade, placares, resultados e pontos.
- Cobertura e unicidade da junção.
- Ausência de públicos negativos ou acima da capacidade.
- Métricas, tabelas, figuras e auditoria da monografia.

## 9. Reprodução

```bash
# Base primária
python3 scripts/fetch_raw.py          # baixa o bruto
python3 scripts/fetch_raw.py --check  # confere o SHA-256
python3 scripts/build_processed.py

# Validações independentes
python3 scripts/validate_cross.py
python3 scripts/validate_champions.py

# Base externa (requer gcloud ADC e FBref local)
PYTHONPATH=src python3 scripts/fetch_basedosdados.py --project SEU_PROJETO
PYTHONPATH=src python3 scripts/parse_fbref.py --input .playwright-mcp/fbref_2024.json
PYTHONPATH=src python3 scripts/build_external.py
PYTHONPATH=src python3 scripts/analyze_external.py

# Auditoria de dados e da monografia
python3 scripts/audit_data.py
python3 scripts/check_monografia.py
```

## 10. Conclusão

A base está **suficientemente sólida para a análise descritiva** do TCC:
7.219 partidas, métricas reprodutíveis, validação cruzada de 99,96% e
campeões 19/19. As ressalvas são de **cobertura e critério das fontes
externas** — sobretudo 2008 parcial, 2024 completado pelo FBref e a
diferença de público entre fontes. Elas não invalidam as conclusões, mas
devem permanecer explícitas nas limitações.
