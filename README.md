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
python3 scripts/bootstrap.py          # prepara tudo: instalação, base e testes
# ou passo a passo:
python3 -m pip install -r requirements-lock.txt  # versões exatas do ambiente validado
python3 -m pip install -e .           # instala o pacote (imports de src/ sem sys.path)
python3 scripts/fetch_raw.py         # baixa o bruto (não versionado, plano B)
python3 scripts/fetch_raw.py --check # confere o SHA-256 das cópias locais
python3 scripts/build_processed.py   # gera data/processed/
python3 -m pytest tests/ -q          # 52 testes (48 rápidos + 4 de integração)
python3 scripts/validate_cross.py    # validação OpenFootball 2018–2024
python3 -m streamlit run app.py
```

`python3 scripts/bootstrap.py --check` apenas verifica o ambiente sem alterar
nada. `python3 -m pytest tests/ -q -m "not integration"` roda só os testes
rápidos, sem precisar do CSV gerado. A cadeia completa também roda no CI
(`.github/workflows/ci.yml`) a cada push e pull request.

`requirements.txt` traz faixas compatíveis (pandas 2.2–3.x); `requirements-lock.txt`
fixa as versões do ambiente em que os resultados foram validados. Para desenvolver,
`requirements-dev.txt` acrescenta o `python-pptx` usado na geração do deck.

A base bruta (`data/raw/`, commit `15f027c`) não é redistribuída — ver `data/raw/FONTE.md`
(repositório sem LICENSE; `scripts/fetch_raw.py` baixa do commit pinado).
O `data/processed/matches_processed.csv` também não é versionado: é gerado
localmente por `scripts/build_processed.py` (ver `data/processed/README.md`).
Validação cruzada 2018–2024 contra o OpenFootball (CC0, versionado em
`data/external/`): **2.659/2.660 idênticas, zero divergências de placar**
(1 exceção de data explicada — jogo de dois dias). Ver `docs/validacao_cruzada.md`.

## Monografia

Texto vigente em `docs/monografia_v2.md` (Tabelas 1–4, Figuras 1–8, apêndices A–D).
Antes de alterar qualquer número no texto, rode `python3 scripts/check_monografia.py`
— ele falha (exit 1) na primeira divergência entre texto, base e tabelas.
O PDF final de depósito (`docs/monografia_final.pdf`) será adicionado quando existir.
Titularidade e proveniência em `NOTICE.md`.

## Estrutura

- `app.py` — dashboard (4 abas)
- `pyproject.toml` — empacotamento (`pip install -e .`) e configuração do pytest
- `src/load_data.py`, `src/clean_data.py`, `src/metrics.py`, `src/context.py`, `src/charts.py`
- `scripts/bootstrap.py`, `scripts/build_processed.py`, `scripts/check_monografia.py`
- `tests/` — testes rápidos com fixtures em `tests/data/`; testes com o CSV real levam o marker `integration`
- `.github/workflows/ci.yml` — cadeia de validação (instalação, base, testes, validações, auditoria)
- `docs/auditoria_fase1.md`, `docs/data_dictionary.md`
