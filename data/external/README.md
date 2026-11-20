# Dados externos (público/arbitragem)

Esta pasta guarda **dados locais** de fontes externas usadas para avaliar a
incorporação de público e arbitragem ao TCC. Os CSVs não são versionados
porque a licença das fontes não permite redistribuição automática.

## Ordem de geração

```bash
# Base dos Dados (BigQuery; requer gcloud ADC e projeto de billing)
python3 scripts/fetch_basedosdados.py --project SEU_PROJETO

# FBref: extrair o JSON no navegador (ver fbref/FONTE.md)
python3 scripts/parse_fbref.py --input .playwright-mcp/fbref_2024.json

# Junção bruta com data/processed/matches_processed.csv
python3 scripts/join_external.py

# Base limpa (2008 como ausente; FBref completa 2024)
python3 scripts/build_external.py

# Análise final
python3 scripts/analyze_external.py
```

## Arquivos

- `basedosdados/brasileirao_serie_a_2006_2024.csv` — tabela histórica local.
- `basedosdados/FETCH_METADATA.json` — consulta, data, linhas e SHA-256.
- `fbref/2024_serie_a.csv` — 380 jogos de 2024.
- `fbref/FETCH_METADATA.json` — URL, linhas, cobertura e SHA-256.
- `joined_context.csv` — junção bruta (sem limpeza de 2008).
- `context_clean.csv` — base final com público/árbitro/faltas e flags.
- `quality_external.json` — cobertura por temporada e regras de limpeza.
- `external_summary.json` — análise final (blocos, correlações, arbitragem).

O relatório interpretativo está em `docs/analise_publico_arbitragem.md`.

## Licença

Ver `docs/fontes_externas.md` e os `FONTE.md` de cada subpasta. Em resumo:
não redistribuir os CSVs; citar as fontes; usar dados derivados.
