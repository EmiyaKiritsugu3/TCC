# Vantagem de jogar em casa — Brasileirão Série A (2006–2024)

Dashboard interativo + pesquisa quantitativa descritiva (TCC, Sistemas de Informação).
Proposta completa em `spec_tcc_vantagem_casa_brasileirao.md`.

## Resultados principais (base validada, 7.219 partidas)

- Vitórias do mandante **49,0%** · empates **26,8%** · vitórias do visitante **24,1%**
- Gols/partida: casa **1,49** × fora **1,00** (diferença +0,49)
- **Pollard geral: 63,66%** → H1 (> 50%) confirmada no período
- Pollard anual varia de **58,2% (2017)** a **69,5% (2018)** → H2 (não constante) sustentada descritivamente

## Como executar

```bash
python3 -m pip install -r requirements.txt
python3 scripts/fetch_raw.py         # baixa o bruto (não versionado, plano B)
python3 scripts/build_processed.py   # gera data/processed/
python3 -m pytest tests/ -q          # 12 testes
python3 scripts/validate_cross.py    # validação OpenFootball 2018–2024
python3 -m streamlit run app.py
```

A base bruta (`data/raw/`, commit `15f027c`) não é redistribuída — ver `data/raw/FONTE.md`
(repositório sem LICENSE; `scripts/fetch_raw.py` baixa do commit pinado).
Validação cruzada 2018–2024 contra o OpenFootball (CC0, versionado em
`data/external/`): **2.659/2.660 idênticas, zero divergências de placar**
(1 exceção de data explicada — jogo de dois dias). Ver `docs/validacao_cruzada.md`.

## Estrutura

- `app.py` — dashboard (4 abas)
- `src/load_data.py`, `src/clean_data.py`, `src/metrics.py`, `src/charts.py`
- `scripts/audit_fase1.py`, `scripts/build_processed.py`
- `tests/test_metrics.py`, `tests/test_data_validation.py`
- `docs/auditoria_fase1.md`, `docs/data_dictionary.md`
