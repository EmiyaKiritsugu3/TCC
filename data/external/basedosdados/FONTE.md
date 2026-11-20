# Fonte — Base dos Dados / Transfermarkt

- **Tabela:** `basedosdados.mundo_transfermarkt_competicoes.brasileirao_serie_a`
- **Dataset:** https://basedosdados.org/dataset/c861330e-bca2-474d-9073-bc70744a1b23
- **Organização:** Transfermarkt
- **Cobertura:** 2003–2024 (o recorte local é 2006–2024)
- **Acesso:** 20/11/2026, via BigQuery REST + Application Default Credentials
- **Linhas exportadas:** 7.126
- **SHA-256:** `e9b1a675166a88877937f2bb53c128a02692ea920d731d04feca50caf0ddc4fb`
- **Arquivo local:** `brasileirao_serie_a_2006_2024.csv` (não versionado)

## Consulta

Ver `FETCH_METADATA.json` e `scripts/fetch_basedosdados.py`. A consulta
seleciona 35 colunas, incluindo `publico`, `publico_max`, `arbitro`,
`faltas_*`, `chutes_*`, `colocacao_*` e `valor_equipe_titular_*`.

## Licença e uso

A Base dos Dados trata e publica a tabela, mas a fonte original é o
Transfermarkt. **Verificar os termos da Base dos Dados e do Transfermarkt**
antes de redistribuir. Para o TCC, usar dados derivados, citar a fonte e
não versionar o CSV bruto.

## Observações de cobertura

- 2006: sem `publico`, `arbitro` e `faltas`.
- 2008: 217 `publico = 0` — provavelmente missing, não portões fechados.
- 2020: 380 `publico = 0` — portões fechados (COVID-19), valor real.
- 2021: 218 `publico = 0` — retorno parcial.
- 2024: 286 jogos no snapshot; completar com FBref.
- `faltas_*`: só a partir de 2018, com lacunas.
- Não há cartões amarelos/vermelhos nesta tabela.
