# Contexto da vantagem de casa — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidar o TCC e aprofundar a análise com os dados existentes: mudança de nível pós-2018, ICs, clássicos, estádio habitual, descanso, força e vantagem por equipe — sem novas fontes de dados e sem alegação causal.

**Architecture:** Manter a separação atual: `context.py` constrói variáveis contextuais; novo `associations.py` calcula comparações, bootstrap e mudança de nível; `scripts/analyze_context.py` orquestra e grava CSV/JSON; `charts.py` só desenha; `app.py` só filtra e exibe. A monografia e o auditor passam a consumir os mesmos números.

**Tech Stack:** Python 3.11, pandas 3.1, numpy (dependência transitiva), Plotly, Streamlit, matplotlib, pytest.

**Spec:** `docs/monografia_v2.md`, `spec_tcc_vantagem_casa_brasileirao.md`, decisão do autor em 19/11/2026 (caminho B).

## Global Constraints

- Toda prosa, rótulo e nome de teste em PT-BR; nomes de clubes sem acento como na fonte.
- Nenhuma conclusão causal: usar “associação”, “diferença descritiva”, “compatível com”.
- Não alterar os números validados existentes (7.219; 49,0/26,8/24,1; 1,49/1,00; 63,66; 12.554/7.166; 58,24/69,51; 19/19; 2.659/2.660).
- Não redistribuir CSV bruto; não criar dependência de rede no fluxo padrão.
- `scripts/check_monografia.py` deve falhar se qualquer número novo divergir.
- Testes rápidos não podem depender de `data/processed/matches_processed.csv`; integração usa o marker existente.
- Não usar “×” para comparar pontos; usar “vs.” ou “−”.

---

## File Structure

- Modify `src/context.py` — estados/regiões, clássico, estádio habitual, faixas de descanso e de posição.
- Create `src/associations.py` — bootstrap, ICs anuais, mudança de nível, grupos, equipe, dentro de equipe-temporada, split-half.
- Create `scripts/analyze_context.py` — gera `figuras/tab5_contexto.csv`, `figuras/tab6_equipes.csv`, `figuras/contexto.json`.
- Modify `scripts/make_figures.py` — gera `fig9_serie_ic.png` e `fig10_contexto.png`.
- Modify `src/charts.py` — gráficos da aba Contexto (barras com IC e ranking de equipes).
- Modify `app.py` — quinta aba “Contexto”, cache do contexto, RF12.
- Modify `tests/test_context.py` — testes das novas variáveis.
- Create `tests/test_associations.py` — testes das funções de análise.
- Modify `tests/test_app.py` — teste da quinta aba.
- Modify `scripts/check_monografia.py` — novos números, ICs, figuras/tabelas, correção do `fillna(99)`.
- Modify `docs/monografia_v2.md` — §1.2, §1.3, §3.2, §3.4, §4.1, §4.3, §5.2–§5.4, §6, resumo, listas.
- Modify `docs/data_dictionary.md`, `docs/resumo_orientador.md`, `docs/decisoes_orientador.md`, `docs/qa_final.md`, `README.md`, `figuras/LEGENDAS.md`, `docs/apresentacao_roteiro.md`.
- Modify `spec_tcc_vantagem_casa_brasileirao.md` — RF12 e nota de escopo descritivo.

## Review Focus

- Grupo vazio ou com n pequeno: Pollard deve retornar `None`/`—` e IC não pode quebrar.
- Clube sem estado/coordenada: falha explícita, nunca `NaN` silencioso.
- Estádio habitual com empate de frequência: escolha determinística (ordem alfabética) e testada.
- Descanso ausente (estreia): não tratar como “descanso máximo”; excluir da comparação.
- Bootstrap: resultado reprodutível com seed; não usar aleatoriedade global do processo.
- Aba nova: não pode quebrar com filtro de uma temporada, recorte vazio ou base antiga sem `stadium`.
- Monografia: cada número novo precisa existir no CSV/JSON e ser conferido pelo auditor.

---

### Task 1: Variáveis contextuais

**Files:**
- Modify: `src/context.py`
- Test: `tests/test_context.py`

**Interfaces:**
- Produces:
  - `CLUB_STATE: dict[str, str]`
  - `same_state(df) -> pd.Series` (bool)
  - `region(df, side: str) -> pd.Series` (`"N"`, `"NE"`, `"CO"`, `"SE"`, `"S"`)
  - `usual_stadium(df) -> pd.Series` (bool; `stadium` == moda da equipe-temporada, desempate alfabético)
  - `rest_bucket(df) -> pd.Series` (`"casa +3"`, `"casa +1-2"`, `"igual"`, `"fora +1-2"`, `"fora +3"`, `None` quando faltar)
  - `table_bucket(df) -> pd.Series` (`"favorito"`, `"equilibrado"`, `"zebra"`; usa `home_pos_before`/`away_pos_before` com margem de 3 posições)

- [ ] **Step 1: Write failing tests** for `same_state`, `region`, `usual_stadium`, `rest_bucket`, `table_bucket` using small synthetic frames, including the tie and missing-rest cases.
- [ ] **Step 2: Run** `pytest tests/test_context.py -q`; expected FAIL for missing names.
- [ ] **Step 3: Implement** the functions in `context.py`, reusing `CLUB_COORDS` style and a `REGIAO` map.
- [ ] **Step 4: Run** `pytest tests/test_context.py -q`; expected PASS.
- [ ] **Step 5: Commit** `feat: adiciona variaveis contextuais de estado, estadio e descanso`.

### Task 2: Módulo de associações

**Files:**
- Create: `src/associations.py`
- Test: `tests/test_associations.py`

**Interfaces:**
- Produces:
  - `bootstrap_pollard_ci(df, n=2000, seed=42) -> tuple[float, float]`
  - `annual_pollard_ci(df, n=2000, seed=42) -> pd.DataFrame` (`season`, `pollard`, `lo`, `hi`)
  - `cluster_bootstrap_diff(df, mask_a, mask_b, n=3000, seed=42) -> dict` (`a`, `b`, `diff`, `lo`, `hi`)
  - `change_point(df) -> dict` (`cut`, `pre`, `post`, `diff`, `sse`)
  - `group_pollard(df, groups: pd.Series, n=2000, seed=42) -> pd.DataFrame` (`grupo`, `n`, `pollard`, `lo`, `hi`)
  - `team_home_advantage(df, n=2000, seed=42) -> pd.DataFrame` (`team`, `n`, `home_ppg`, `away_ppg`, `ha`, `lo`, `hi`)
  - `within_team_season(df, groups: pd.Series, outcome="home_points") -> pd.DataFrame` (`grupo`, `n`, `mean_deviation`)
  - `split_half_reliability(team_df) -> float`

- [ ] **Step 1: Write failing tests** with a synthetic 6-match frame: known Pollard, known bootstrap ordering, level shift, team HA, within-team deviation, split-half on 4 teams.
- [ ] **Step 2: Run** `pytest tests/test_associations.py -q`; expected FAIL.
- [ ] **Step 3: Implement** pure functions; use `numpy.random.default_rng(seed)`; return `None` for empty groups.
- [ ] **Step 4: Run** `pytest tests/test_associations.py -q`; expected PASS.
- [ ] **Step 5: Commit** `feat: adiciona funcoes de associacao e bootstrap`.

### Task 3: Script de análise e artefatos

**Files:**
- Create: `scripts/analyze_context.py`
- Modify: `scripts/make_figures.py`
- Output: `figuras/tab5_contexto.csv`, `figuras/tab6_equipes.csv`, `figuras/contexto.json`, `figuras/fig9_serie_ic.png`, `figuras/fig10_contexto.png`

**Interfaces:**
- Consumes: `context.same_state`, `region`, `usual_stadium`, `rest_bucket`, `table_bucket`; `associations.*`.
- Produces: the five artifacts above, with PT-BR headers and comma decimals in CSV.

- [ ] **Step 1: Write a smoke test** (in `tests/test_associations.py` or a new `tests/test_analyze_context.py`) that runs `scripts/analyze_context.py` against the real base and asserts the files exist and the total n in Table 5 sums to 7.219.
- [ ] **Step 2: Run** the test; expected FAIL (script missing).
- [ ] **Step 3: Implement** `analyze_context.py`: load base, compute context, write tables/JSON, print summary.
- [ ] **Step 4: Add** `fig9` (annual Pollard with IC ribbon + pre/post means) and `fig10` (grouped Pollard with IC) to `make_figures.py`.
- [ ] **Step 5: Run** `python3 scripts/analyze_context.py` and `python3 scripts/make_figures.py`; expected output files.
- [ ] **Step 6: Commit** `feat: gera tabelas e figuras de contexto`.

### Task 4: Dashboard — aba Contexto

**Files:**
- Modify: `src/charts.py`
- Modify: `app.py`
- Test: `tests/test_app.py`

**Interfaces:**
- Produces:
  - `charts.pollard_by_group(effects: pd.DataFrame)` — barras horizontais com IC e linha de 50%.
  - `charts.team_home_advantage(team_df: pd.DataFrame)` — barras horizontais ordenadas.
  - `app.py` — `st.tabs([... "Contexto"])`; cache `contexto_base()`; RF12.

- [ ] **Step 1: Write failing AppTest** asserting five tabs and that the Contexto tab shows a Pollard card for the full period.
- [ ] **Step 2: Run** `pytest tests/test_app.py -q`; expected FAIL.
- [ ] **Step 3: Implement** the charts and the fifth tab with global season filter, group selector (clássico, distância, estádio, descanso, força, era), cards and two charts.
- [ ] **Step 4: Run** `pytest tests/test_app.py -q`; expected PASS.
- [ ] **Step 5: Commit** `feat: adiciona aba de contexto ao dashboard`.

### Task 5: Monografia e auditor

**Files:**
- Modify: `docs/monografia_v2.md`
- Modify: `scripts/check_monografia.py`
- Modify: `tests/test_check_monografia_guard.py` (if the obsolete-number guard needs the new count)

**Interfaces:**
- Consumes: `figuras/tab5_contexto.csv`, `tab6_equipes.csv`, `contexto.json`.
- Produces: new §5.4, Figure 9/10, Tables 5/6, updated abstract, conclusion, lists.

- [ ] **Step 1: Update the outline** in §1.2/§1.3 and the sumário: add H3–H5 and §5.4.
- [ ] **Step 2: Add the new results** using the exact numbers from `contexto.json` and the tables; label all as descriptive.
- [ ] **Step 3: Add Figure 9** (annual series with IC + level shift) and **Figure 10** (context effects); update the list of figures.
- [ ] **Step 4: Expand Table 5** with ICs and add Table 6 (team HA top/bottom); update the list of tables.
- [ ] **Step 5: Rewrite** the rest passage, the “2020 piso” sentence, and the “12.554 × 7.166” typo.
- [ ] **Step 6: Extend `check_monografia.py`** to verify the new numbers, the new table rows, the figure order, and the corrected rest comparison (without `fillna(99)`).
- [ ] **Step 7: Run** `python3 scripts/check_monografia.py`; expected “AUDITORIA NUMÉRICA: tudo confere”.
- [ ] **Step 8: Commit** `docs: incorpora analise de contexto e mudanca de nivel`.

### Task 6: Consistência documental e validação final

**Files:**
- Modify: `README.md`, `docs/resumo_orientador.md`, `docs/decisoes_orientador.md`, `docs/qa_final.md`, `docs/apresentacao_roteiro.md`, `figuras/LEGENDAS.md`, `spec_tcc_vantagem_casa_brasileirao.md`.

- [ ] **Step 1: Update counts** (tests, tabs) and the “9 testes” → actual count.
- [ ] **Step 2: Update the app methodology text** (remove “sem viagens”; explain context tab).
- [ ] **Step 3: Add RF12 to the spec and Table 3**; note that it is descriptive.
- [ ] **Step 4: Run the full chain:** `pytest tests/ -q`, `validate_cross.py`, `validate_champions.py`, `check_monografia.py`, `make_figures.py`, `build_docx.py`.
- [ ] **Step 5: Commit** `docs: alinha documentacao e contagens`.
