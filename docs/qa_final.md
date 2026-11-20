# QA final — 17/11/2026 (branch `main`, merge `5105dd5`)

> **Revalidação em clone limpo concluída** (abaixo, seção 0) no merge `5105dd5`:
> clone novo, venv Python 3.11.15, instalação com hashes e cadeia completa do CI.
> As seções 1–5 são o registro histórico do commit `9b9540c`.

## Atualização 20/11/2026 — cartões (branch `feat/cartoes`)

- `pytest tests/ -q` → **114 passed** (105 rápidos + 9 de integração); cobertura **91,2%**.
- `scripts/check_monografia.py` → **AUDITORIA NUMÉRICA: tudo confere**
  (Tabela 11, Figura 13, DiD 2019→2020 e contagem de testes).
- `scripts/audit_data.py` → **150 verificações, 0 falhas**.
- Monografia: §5.7 de cartões, Tabela 11 e Figura 13; 11 tabelas e 13 figuras.
- Deck: 16 slides, com dois slides de cartões e a ressalva do IC.

## Atualização 19/11/2026 — branch `feat/contexto-vantagem-casa`

- `pytest tests/ -q` → **104 passed** (95 rápidos + 9 de integração).
- `scripts/analyze_context.py` → `tab5_contexto.csv`, `tab6_equipes.csv`,
  `tab7_correlacoes_equipe.csv`, `matriz_equipe.csv`, `matriz_partida.csv`,
  `contexto.json`; Geral 63,66% (IC 62,63–64,70); quebra em 2019.
- `scripts/make_figures.py` → Figura 9 (série com IC), Figura 10 (contexto) e Figura 11 (matriz de correlação).
- `scripts/check_monografia.py` → **AUDITORIA NUMÉRICA: tudo confere**
  (Tabelas 1 e 5–7; ICs; mudança de nível; correlações; figuras 1–11; 9.390 palavras).
- Dashboard: 5 abas; AppTest cobre a aba Contexto.
- Monografia v3: §5.4–5.5, Tabelas 5–7, Figuras 9–11, ICs na Tabela 1.

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

- `apresentacao_tcc.pptx`: **14 slides** (v3), gerado por `scripts/build_deck.py`;
  inclui mudança de nível, contexto, matriz e público/arbitragem. O snapshot
  histórico de 10 slides foi substituído.
- `apresentacao_tcc.pdf`: **14 páginas**, regenerado via LibreOffice.

## Artefatos de entrega

- `apresentacao/apresentacao_tcc.pdf` (14 p.)
- `apresentacao/apresentacao_tcc.pptx` (14 slides)
- `docs/monografia_final.pdf` — pendente (template do curso)
