# QA final — 17/11/2026 (branch `main`, merge `5105dd5`)

> **Revalidação em clone limpo concluída** (abaixo, seção 0) no merge `5105dd5`:
> clone novo, venv Python 3.11.15, instalação com hashes e cadeia completa do CI.
> As seções 1–5 são o registro histórico do commit `9b9540c`.

## 0. Revalidação em clone limpo — `main` @ `5105dd5` (17/11/2026)

- Clone de `main` em `/tmp/opencode/tcc-qa-clean`; venv novo (`venv/bin/python`, Python 3.11.15).
- Instalação: `pip install --require-hashes --only-binary :all: -r requirements-hashed.txt`
  e `pip install --only-binary=:all: --no-deps -e .` — ambas OK.
- `scripts/fetch_raw.py` baixou os 2 arquivos do commit pinado (1.187.343 e 2.113 bytes);
  `fetch_raw.py --check` → **OK. Arquivos conferidos.**
- `scripts/build_processed.py` → 7.219 partidas; cobertura 380/temporada, 2016 com 379.
- `scripts/bootstrap.py --check` → **OK: 5 verificações passaram.**
- `scripts/make_figures.py`, `export_table1.py` e `build_docx.py` → OK.
- `pytest tests/ -q --cov=src --cov-report=term --cov-fail-under=90` →
  **71 passed**, cobertura **98,24%** (341 statements, 6 não cobertos).
- `scripts/validate_cross.py` → **PASS — bases idênticas** (2.659/2.660).
- `scripts/validate_champions.py` → **PASS — 19/19 campeões**.
- `scripts/check_monografia.py` → **AUDITORIA NUMÉRICA: tudo confere**.

## 1. Clone limpo (worktree `/tmp/opencode/tcc-qa`, venv novo, `requirements-lock.txt`) — histórico

- `scripts/fetch_raw.py` — baixou os 2 arquivos do commit pinado (1.187.343 e 2.113 bytes); SHA-256 conferido.
- `scripts/build_processed.py` — `lidas: 8785, mantidas: 7219`, exclusão única `fora_do_recorde_2006_2024: 1566`; cobertura 380/temporada, 2016 com 379.
- `pytest tests/ -q` — **22 passed** (valor histórico do commit `9b9540c`).
- `scripts/validate_cross.py` — **RESULTADO: PASS — bases idênticas** (2.659/2.660; 1 exceção de data explicada, jogo de dois dias 2023).
- `scripts/validate_champions.py` — **RESULTADO: PASS — 19/19 campeões**.

## 2. Smoke test da aplicação (repo principal)

- `tests/test_app.py` — 2 passed (Flamengo 2019: 53/37/90/38; filtro global respeitado; sem `America-MG` fora da temporada).
- Checagem direta: 4 abas presentes; filtro 2020 mostra Pollard **60,17%** (380 jogos); sem avisos de `use_container_width`.

## 3. Consistência numérica e de contagem

- `pytest tests/ -q` — **71 passed**.
- Baseline de cobertura (`.venv/bin/python -m pytest tests/ -m "not integration" --cov=src`): **98%** (64 passed, 7 deselecionados; 341 statements, 6 não cobertos em `src/clean_data.py:182-188`, gravação do relatório).
- Busca por restos obsoletos (`12 testes`, `Doze testes`, `0 pts`, `55 pts`, `108 pts`): só ocorre em `docs/arquivo/cap4_rascunho.md` (rascunho histórico arquivado, substituído pela monografia vigente).
- Números principais preservados: 7.219 partidas; 49,0% / 26,8% / 24,1%; 1,49 × 1,00; Pollard 63,66%; anual 58,2%–69,5%; Flamengo 2019 53/37/90/38.

## 4. Monografia (`docs/monografia_v2.md`)

- Primeira citação das figuras em ordem: [1, 2, 3, 4, 5, 6, 7, 8].
- Tabela 1 com 19 linhas (2006–2024); Tabelas 2–4 criadas; Lista de Tabelas atualizada.
- Só resta a tag `[PENDENTE - ORIENTADOR]` (bloqueios externos).
- Corpo: 6.098 palavras (meta proativa ≥ 5.500).
- PDF final pendente do template UFRN — bloqueio registrado em `docs/decisoes_orientador.md`.

## 5. Deck e PDF (`apresentacao/`)

- `apresentacao_tcc.pptx`: 10 slides; continha `63,7%`, link do repositório e `22 testes` (snapshot histórico; no branch atual o deck diz `71 testes`).
- `apresentacao_tcc.pdf`: 10 páginas, regenerado via LibreOffice após a correção do slide 9.

## Artefatos de entrega

- `apresentacao/apresentacao_tcc.pdf` (10 p.)
- `apresentacao/apresentacao_tcc.pptx` (10 slides)
- `docs/monografia_final.pdf` — pendente (template do curso)
