# Vantagem de jogar em casa — Brasileirão Série A (2006–2024)

Dashboard interativo + pesquisa quantitativa descritiva (TCC, Sistemas de Informação).
Proposta completa em `spec_tcc_vantagem_casa_brasileirao.md`.

## Resultados principais (base validada, 7.219 partidas)

- Vitórias do mandante **49,0%** · empates **26,8%** · vitórias do visitante **24,1%**
- Gols/partida: casa **1,49** × fora **1,00** (diferença +0,49)
- **Pollard geral: 63,66%** → H1 (> 50%) confirmada no período
- Pollard anual varia de **58,2% (2017)** a **69,5% (2018)**, com **mudança de nível** pós-2018:
  **64,9%** em 2006–2018 vs. **61,0%** em 2019–2024 (diferença 3,9 p.p.; IC 95% 2,1–5,6)
- Contexto: distância não move o índice (63,4%–63,9%); clássicos sem viagem ficam em **58,2%**;
  estádio habitual **64,1%** vs. outro **59,4%**; mandante zebra ainda fica em **55,7%**

## Como executar

```bash
python3 scripts/bootstrap.py          # prepara tudo: instalação, base e testes
# ou passo a passo:
python3 -m pip install -r requirements-lock.txt  # versões exatas do ambiente validado
python3 -m pip install -e .           # instala o pacote (imports de src/ sem sys.path)
python3 scripts/fetch_raw.py         # baixa o bruto (não versionado, plano B)
python3 scripts/fetch_raw.py --check # confere o SHA-256 das cópias locais
python3 scripts/build_processed.py   # gera data/processed/
python3 scripts/analyze_context.py   # gera tab5, tab6 e contexto.json
python3 scripts/make_figures.py      # gera figuras e tab1
python3 -m pytest tests/ -q          # 94 testes (85 rápidos + 9 de integração)
python3 scripts/validate_cross.py    # validação OpenFootball 2018–2024
python3 -m streamlit run app.py
```

`python3 scripts/bootstrap.py --check` apenas verifica o ambiente sem alterar
nada. `python3 -m pytest tests/ -q -m "not integration"` roda só os testes
rápidos, sem precisar do CSV gerado. A cadeia completa também roda no CI
(`.github/workflows/ci.yml`) a cada push e pull request.

`requirements.txt` traz faixas compatíveis (pandas 2.2–3.x); `requirements-lock.txt`
fixa as versões do ambiente em que os resultados foram validados. Para desenvolver,
`requirements-dev.txt` acrescenta `python-pptx` (deck), `python-docx` (rascunho ABNT) e `pytest-cov` (cobertura). `requirements-hashed.txt` fixa hashes para o CI e `pylock.toml` é o lock PEP 751 equivalente.

A base bruta (`data/raw/`, commit `15f027c`) não é redistribuída — ver `data/raw/FONTE.md`
(repositório sem LICENSE; `scripts/fetch_raw.py` baixa do commit pinado).
O `data/processed/matches_processed.csv` também não é versionado: é gerado
localmente por `scripts/build_processed.py` (ver `data/processed/README.md`).
Validação cruzada 2018–2024 contra o OpenFootball (CC0, versionado em
`data/external/`): **2.659/2.660 idênticas, zero divergências de placar**
(1 exceção de data explicada — jogo de dois dias). Ver `docs/validacao_cruzada.md`.

## Monografia

Texto vigente em `docs/monografia_v2.md` (Tabelas 1–6, Figuras 1–10, apêndices A–D).
Antes de alterar qualquer número no texto, rode `python3 scripts/check_monografia.py`
— ele acumula as divergências entre texto, base e tabelas e falha (exit 1) ao final da auditoria.
O PDF final de depósito (`docs/monografia_final.pdf`) será adicionado quando existir.
Titularidade e proveniência em `NOTICE.md`.

## Estrutura

- `app.py` — dashboard (5 abas, incluindo Contexto)
- `pyproject.toml` — empacotamento (`pip install -e .`) e configuração do pytest
- `src/load_data.py`, `src/clean_data.py`, `src/metrics.py`, `src/context.py`, `src/associations.py`, `src/charts.py`
- `scripts/bootstrap.py`, `scripts/build_processed.py`, `scripts/analyze_context.py`, `scripts/check_monografia.py`
- `tests/` — testes rápidos com fixtures em `tests/data/`; testes com o CSV real levam o marker `integration`
- `.github/workflows/ci.yml` — cadeia de validação (instalação, base, testes, validações, auditoria)
- `docs/auditoria_fase1.md`, `docs/data_dictionary.md`
