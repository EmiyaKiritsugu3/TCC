# `data/processed/` — base derivada (gerada localmente)

O arquivo `matches_processed.csv` (7.219 partidas, Série A 2006–2024) **não é
redistribuído neste repositório**: a fonte primária
(`adaoduque/Brasileirao_Dataset`, commit `15f027c`) não tem arquivo LICENSE,
e não há autorização escrita do autor (ver `data/raw/FONTE.md`).

Para gerar localmente:

```bash
python3 scripts/fetch_raw.py         # baixa o bruto do commit pinado (confere SHA-256)
python3 scripts/build_processed.py   # gera matches_processed.csv + quality_report.json
```

O `quality_report.json` (contagens, cobertura por temporada, notas de 2016 e
2020) **é** versionado e permite auditar a construção sem o CSV.
