# QA final — 04/11/2026 (branch `main`, commit `9b9540c`)

## 1. Clone limpo (worktree `/tmp/opencode/tcc-qa`, venv novo, `requirements-lock.txt`)

- `scripts/fetch_raw.py` — baixou os 2 arquivos do commit pinado (1.187.343 e 2.113 bytes); SHA-256 conferido.
- `scripts/build_processed.py` — `lidas: 8785, mantidas: 7219`, exclusão única `fora_do_recorde_2006_2024: 1566`; cobertura 380/temporada, 2016 com 379.
- `pytest tests/ -q` — **22 passed**.
- `scripts/validate_cross.py` — **RESULTADO: PASS — bases idênticas** (2.659/2.660; 1 exceção de data explicada, jogo de dois dias 2023).
- `scripts/validate_champions.py` — **RESULTADO: PASS — 19/19 campeões**.

## 2. Smoke test da aplicação (repo principal)

- `tests/test_app.py` — 2 passed (Flamengo 2019: 53/37/90/38; filtro global respeitado; sem `America-MG` fora da temporada).
- Checagem direta: 4 abas presentes; filtro 2020 mostra Pollard **60,17%** (380 jogos); sem avisos de `use_container_width`.

## 3. Consistência numérica e de contagem

- `pytest tests/ -q` — **22 passed**.
- Busca por restos obsoletos (`12 testes`, `Doze testes`, `0 pts`, `55 pts`, `108 pts`): só ocorre em `docs/arquivo/cap4_rascunho.md` (rascunho histórico arquivado, substituído pela monografia vigente).
- Números principais preservados: 7.219 partidas; 49,0% / 26,8% / 24,1%; 1,49 × 1,00; Pollard 63,66%; anual 58,2%–69,5%; Flamengo 2019 53/37/90/38.

## 4. Monografia (`docs/monografia_v2.md`)

- Primeira citação das figuras em ordem: [1, 2, 3, 4, 5, 6, 7, 8].
- Tabela 1 com 19 linhas (2006–2024); Tabelas 2–4 criadas; Lista de Tabelas atualizada.
- Só restam tags `[TODO-BANCA/SIGLAS/CBF/ORIENTADOR]` (bloqueadas, externas).
- Corpo: 5.511 palavras (meta proativa ≥ 5.500).
- PDF final pendente do template UFRN — bloqueio registrado em `docs/decisoes_orientador.md`.

## 5. Deck e PDF (`apresentacao/`)

- `apresentacao_tcc.pptx`: 10 slides; contém `63,7%`, link do repositório e `22 testes` (sem `12 testes`).
- `apresentacao_tcc.pdf`: 10 páginas, regenerado via LibreOffice após a correção do slide 9.

## Artefatos de entrega

- `apresentacao/apresentacao_tcc.pdf` (10 p.)
- `apresentacao/apresentacao_tcc.pptx` (10 slides)
- `docs/monografia_final.pdf` — pendente (template do curso)
