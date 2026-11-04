# Correção e Otimização do TCC — Vantagem de Casa (2006–2024)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Corrigir os defeitos de cálculo e de estado vazio do dashboard, fechar as pendências editoriais da monografia e deixar o repositório pronto para depósito e defesa, sem alterar os resultados principais já validados.

**Architecture:** Correções cirúrgicas em `src/metrics.py` e `app.py`, sempre com teste que falha antes; endurecimento do pipeline (`src/clean_data.py`, `scripts/fetch_raw.py`) e fechamento documental em paralelo. Nenhuma fórmula, recorte ou linha válida da base será recalculada. A única mudança esperada na base processada é a remoção de espaços do campo `stadium`.

**Tech Stack:** Python 3.11.15, pandas 3.1.0, Plotly 7.1.0, Streamlit 1.66.1, matplotlib 3.11.2, pytest 9.2.0, Markdown/ABNT.

**Spec:** `spec_tcc_vantagem_casa_brasileirao.md` (RF01–RF11, RNF01–RNF08, §16) + tabela de achados abaixo (delta da auditoria de 04/11/2026).

---

## Contexto e evidências (baseline)

| # | Severidade | Achado | Evidência | Correção |
|---|---|---|---|---|
| P0-1 | Crítica | `team_season` soma pontos do adversário aos da equipe | `src/metrics.py:75`, `:79`; Flamengo 2019 retorna 55/53/108 em vez de 53/37/90 | Task 2 |
| P0-2 | Crítica | Aba Equipes mostra “0 pts / 0 jogos” para time ausente na temporada; Figura 3 expõe o erro | `app.py:87-98`; `figuras/app3_equipes_partidas.png` (América-MG 2006) | Task 3 |
| P0-3 | Alta | Tabela 1 não está no texto e a §5.4 diz que dados por equipe estão nela | `docs/monografia_v1.md:311`, `:324` | Task 6 |
| P0-4 | Alta | Figura 7 (gols) é citada antes da Figura 6 (Pollard) | `docs/monografia_v1.md:289-305`; `figuras/LEGENDAS.md:28-36` | Task 6 |
| P0-5 | Alta | `-->` solto na capa; arquivo “v1” com cabeçalho “versão 2” | `docs/monografia_v1.md:3`, `:18` | Task 6 |
| P1-1 | Alta | `_strip` não funciona no pandas 3 (`dtype == object` é falso para `str`) | `src/clean_data.py:21`; pandas 3.1.0 no `.venv` | Task 5 |
| P1-2 | Alta | Time ausente (`NA`) não é contabilizado como `clube_ausente` | `src/clean_data.py:87-88` | Task 5 |
| P1-3 | Média | Download bruto não verifica SHA-256 | `scripts/fetch_raw.py:18-25` | Task 5 |
| P1-4 | Média | Dashboard usa ponto decimal (“49.0%”, “1.49”) | `app.py:67-74`; `src/charts.py:13` | Task 4 |
| P1-5 | Média | 11 TODOs, referências numeradas e sem Streamlit/Nevill fechados | `docs/monografia_v1.md:348-378` | Task 6 |
| P1-6 | Média | Nota Barueri/Grêmio Prudente exigida pela auditoria está ausente | `docs/auditoria_fase1.md:45` | Task 6 |
| P1-7 | Média | `.playwright-mcp/` versionado; PDFs ignorados; branch padrão desatualizado | `.gitignore:7`, `:10`; `git ls-files` | Task 8 |
| P1-8 | Média | CSV processado completo está público sem licença da fonte | `data/processed/matches_processed.csv` versionado | Task 8 (gate) |
| P2-1 | Alta | Corpo da monografia com ~2.555 palavras; profundidade a confirmar | contagem em 04/11/2026 | Task 7 (gate) |
| P2-2 | Baixa | Deck diz “gerado por script”, mas o gerador não está no repositório | `apresentacao/apresentacao_tcc.pptx` | Task 8 |

**Resultados que não podem mudar** (conferidos em 04/11/2026):

- 7.219 partidas, 19 temporadas; 2016 = 379; 2020 = 380.
- Mandante 49,0%; empates 26,8%; visitante 24,1%.
- Gols/partida: casa 1,49 × fora 1,00; diferença +0,49.
- Pontos: 12.554 (mandantes) × 7.166 (visitantes); Pollard 63,66% (63,7%).
- Pollard anual: 58,24% (2017) a 69,51% (2018).
- Flamengo 2019: 53 pts em casa, 37 fora, 90 no total, 38 jogos.

**Fora deste plano:** incluir Spearman, previsão, IA, apostas, novas fontes, redesenho visual amplo ou recálculo dos indicadores. Qualquer mudança acadêmica de escopo passa pelo orientador (Task 7).

---

## Global Constraints

- Python 3.11; dependências do `requirements-lock.txt` (Task 5). Não atualizar bibliotecas durante as correções.
- `data/raw/` é imutável. Não alterar regras de inclusão/exclusão nem o recorte 2006–2024.
- Toda tarefa de código segue TDD: escrever o teste, rodar e ver falhar, implementar o mínimo, rodar e ver passar, commitar.
- Texto de interface em português, com vírgula decimal e unidade explícita (RNF04).
- Não afirmar causalidade; manter a linguagem observacional e descritiva.
- `figuras/tab1_indicadores_temporada.csv` é a fonte única da Tabela 1.
- Dados brutos não são redistribuídos. O CSV processado só permanece público se houver autorização escrita da fonte (Task 8).
- Alterações na monografia exigem revisão do autor; decisões do orientador são registradas em `docs/decisoes_orientador.md`.
- Commits pequenos, em português, no padrão `tipo(escopo): descrição`.

---

## Review Focus

1. **Ponto de time visitante:** ao consultar uma equipe fora de casa, somar apenas os pontos dela, nunca os do mandante — `tests/test_metrics.py::test_team_season_separa_pontos_de_casa_e_fora` (Task 2).
2. **Equipe/temporada inexistente:** não renderizar cartões de 0 pt; restringir as opções à temporada e, se o guarda for alcançado, avisar — `tests/test_app.py::test_aba_equipes_filtra_temporada_e_flamengo_2019` (Task 3).
3. **Texto com dtype `string`, NBSP ou clube ausente:** aparar espaços e rejeitar clube ausente com contabilização — `tests/test_data_validation.py::test_strip_remove_espacos_em_string_dtype` e `::test_clube_ausente_rejeitado` (Task 5).
4. **Bruto corrompido/truncado:** hash divergente deve abortar antes de gerar a base — `tests/test_integrity.py::test_verify_sha256_aceita_e_rejeita` (Task 5).
5. **Filtro global de temporadas:** todos os cartões, gráficos, tabela e exportação usam o mesmo `base` (RF02/RNF03) — `tests/test_app.py::test_aba_equipes_respeita_filtro_global` (Task 3).

---

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `src/metrics.py` | `team_season` correto; novo `teams_in_season` |
| `src/formatting.py` | **novo** — `pct`, `num`, `signed` em pt-BR |
| `src/integrity.py` | **novo** — `sha256_file`, `verify_sha256` |
| `src/clean_data.py` | `_strip` compatível com pandas 3; clube ausente |
| `app.py` | aba Equipes, filtros, formatação e `width="stretch"` |
| `tests/test_metrics.py` | testes de `team_season` e `teams_in_season` |
| `tests/test_data_validation.py` | testes de `_strip` e clube ausente |
| `tests/test_formatting.py` | **novo** — formatação pt-BR |
| `tests/test_integrity.py` | **novo** — SHA-256 |
| `tests/test_app.py` | **novo** — AppTest da aba Equipes |
| `scripts/fetch_raw.py` | download com verificação SHA-256 e `--check` |
| `scripts/export_table1.py` | **novo** — Tabela 1 em Markdown a partir do CSV |
| `requirements.txt` / `requirements-lock.txt` / `requirements-dev.txt` | faixas, versões exatas e ferramentas de QA |
| `docs/monografia_v2.md` | monografia consolidada (renomeada de `monografia_v1.md`) |
| `docs/decisoes_orientador.md` | **novo** — registro das 5 decisões |
| `docs/qa_final.md` | **novo** — evidências do QA final |
| `NOTICE.md` | **novo** — titularidade e proveniência dos dados |

---

## Task 1: Baseline, branch e trava de segurança

**Files:**
- Create: `docs/superpowers/plans/2026-11-04-correcao-tcc-vantagem-casa.md` (este arquivo)
- Nenhum código alterado nesta tarefa.

**Interfaces:**
- Consumes: estado atual do repositório em `main` (`6f8cb1b`).
- Produces: branch `fix/auditoria-final`, baseline registrado em `/tmp/tcc_baseline_sha256.txt`.

- [ ] **Step 1: Criar a branch de trabalho**

```bash
git switch -c fix/auditoria-final main
git status --porcelain
```

Expected: branch criada; `git status` mostra apenas o plano não rastreado.

- [ ] **Step 2: Rodar o baseline de testes**

```bash
.venv/bin/python -m pytest tests/ -q
```

Expected: `12 passed`.

- [ ] **Step 3: Rodar as duas validações externas**

```bash
.venv/bin/python scripts/validate_cross.py
.venv/bin/python scripts/validate_champions.py
```

Expected: `RESULTADO: PASS — bases idênticas` e `RESULTADO: PASS — 19/19 campeões`.

- [ ] **Step 4: Registrar hashes e commit de referência**

```bash
git rev-parse HEAD | tee /tmp/tcc_baseline_sha256.txt
sha256sum data/processed/matches_processed.csv | tee -a /tmp/tcc_baseline_sha256.txt
sha256sum data/raw/campeonato-brasileiro-full.csv data/raw/Legenda.txt | tee -a /tmp/tcc_baseline_sha256.txt
```

Expected: base processada `67b566b2…`, bruto `c09d03d3…`, legenda `dfedf5fb…`; guardar o arquivo até a Task 5.

- [ ] **Step 5: Reproduzir o bug da aba Equipes (baseline que deve falhar)**

```bash
.venv/bin/python - <<'PY'
from streamlit.testing.v1 import AppTest
at = AppTest.from_file("app.py", default_timeout=60).run()
m = {x.label: x.value for x in at.metric}
print("equipe:", at.selectbox[0].value, "temporada:", at.selectbox[1].value)
print("total:", m.get("Total"), "jogos:", m.get("Jogos"))
assert m.get("Total") == "0 pts" and m.get("Jogos") == "0"
print("BUG REPRODUZIDO")
PY
```

Expected: `America-MG`, `2006`, `0 pts`, `0`, `BUG REPRODUZIDO`. Este é o teste que a Task 3 fará passar.

- [ ] **Step 6: Commitar o plano**

```bash
git add docs/superpowers/plans/2026-11-04-correcao-tcc-vantagem-casa.md
git commit -m "docs: adiciona plano de correção e otimização do TCC"
```

---

## Task 2: Corrigir a pontuação de `team_season`

**Files:**
- Modify: `src/metrics.py:64-80` (linhas 75 e 79)
- Test: `tests/test_metrics.py:10` (import) e novo teste ao final

**Interfaces:**
- Consumes: `summarize(df) -> dict` (já existente).
- Produces: `team_season(df: pd.DataFrame, team: str, season: int) -> dict` com `home_points` e `away_points` **int**, contando somente os pontos da equipe.

- [ ] **Step 1: Escrever os testes que falham**

Em `tests/test_metrics.py`, importar `team_season` e adicionar:

```python
from metrics import by_season, pollard, summarize, team_season

PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed" / "matches_processed.csv"


def test_team_season_separa_pontos_de_casa_e_fora():
    casa = _df([(2, 0), (1, 1), (0, 2), (3, 0)])
    casa["season"] = 2019
    casa["home_team"] = "Flamengo"
    casa["away_team"] = ["A", "B", "C", "D"]

    fora = _df([(0, 2), (1, 1), (2, 0)])
    fora["season"] = 2019
    fora["home_team"] = ["A", "B", "C"]
    fora["away_team"] = "Flamengo"

    d = pd.concat([casa, fora], ignore_index=True)
    ts = team_season(d, "Flamengo", 2019)

    assert (ts["home_w"], ts["home_d"], ts["home_l"]) == (2, 1, 1)
    assert ts["home_points"] == 7          # 3 + 1 + 0 + 3
    assert (ts["away_w"], ts["away_d"], ts["away_l"]) == (1, 1, 1)
    assert ts["away_points"] == 4          # 3 + 1 + 0
    assert isinstance(ts["home_points"], int)
    assert isinstance(ts["away_points"], int)


@pytest.mark.skipif(not PROCESSED.exists(), reason="rode scripts/build_processed.py")
def test_flamengo_2019_pontuacao_oficial():
    df = pd.read_csv(PROCESSED)
    ts = team_season(df, "Flamengo", 2019)
    assert (ts["home_points"], ts["away_points"]) == (53, 37)
    assert ts["home_points"] + ts["away_points"] == 90
    assert ts["home_n"] + ts["away_n"] == 38
```

- [ ] **Step 2: Rodar e ver falhar**

```bash
.venv/bin/python -m pytest tests/test_metrics.py -q
```

Expected: falha em `test_team_season_separa_pontos_de_casa_e_fora` com `11 != 7` (e `8 != 4`); o teste do Flamengo falha com `55.0 != 53`.

- [ ] **Step 3: Implementar a correção mínima**

Em `src/metrics.py`, trocar apenas as duas somas:

```python
"home_points": int(sh["home_points"]),
...
"away_points": int(sa["away_points"]),
```

Não alterar `summarize`, `by_season` nem as fórmulas de W/D/L.

- [ ] **Step 4: Rodar e ver passar**

```bash
.venv/bin/python -m pytest tests/ -q
```

Expected: `14 passed` (12 anteriores + 2 novos).

- [ ] **Step 5: Commit**

```bash
git add src/metrics.py tests/test_metrics.py
git commit -m "fix(metrics): corrige pontos de casa e fora em team_season"
```

---

## Task 3: Corrigir o estado vazio da aba Equipes e regenerar a Figura 3

**Files:**
- Modify: `src/metrics.py:64-80` (adicionar `teams_in_season`)
- Modify: `app.py:86-105`
- Test: `tests/test_metrics.py`, `tests/test_app.py` (novo)
- Asset: `figuras/app3_equipes_partidas.png`, `figuras/LEGENDAS.md:13-15`

**Interfaces:**
- Consumes: `team_season` da Task 2.
- Produces: `teams_in_season(df: pd.DataFrame, season: int) -> list[str]`; widgets com `key="temporada"` e `key="equipe"`; aba Equipes usando `base` (filtro global).

- [ ] **Step 1: Escrever o teste unitário de `teams_in_season`**

Em `tests/test_metrics.py`:

```python
from metrics import ..., teams_in_season


def test_teams_in_season_respeita_temporada():
    d = _df([(1, 0), (1, 0), (1, 0)])
    d["season"] = [2006, 2006, 2019]
    d["home_team"] = ["America-MG", "Flamengo", "Flamengo"]
    d["away_team"] = ["A", "B", "C"]

    assert teams_in_season(d, 2006) == ["America-MG", "Flamengo"]
    assert teams_in_season(d, 2019) == ["Flamengo"]
    assert teams_in_season(d, 2020) == []
```

- [ ] **Step 2: Rodar e ver falhar**

```bash
.venv/bin/python -m pytest tests/test_metrics.py::test_teams_in_season_respeita_temporada -q
```

Expected: `ImportError`/`NameError` para `teams_in_season`.

- [ ] **Step 3: Implementar `teams_in_season`**

Em `src/metrics.py`, após `team_season`:

```python
def teams_in_season(df: pd.DataFrame, season: int) -> list[str]:
    """Equipes que disputaram a temporada, em ordem alfabética."""
    g = df[df["season"] == season]
    return sorted(set(g["home_team"]) | set(g["away_team"]))
```

- [ ] **Step 4: Escrever o teste de UI que falha**

Criar `tests/test_app.py`:

```python
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

RAIZ = Path(__file__).resolve().parent.parent
PROCESSED = RAIZ / "data" / "processed" / "matches_processed.csv"

pytestmark = pytest.mark.skipif(
    not PROCESSED.exists(), reason="rode scripts/build_processed.py"
)


def test_aba_equipes_filtra_temporada_e_flamengo_2019():
    at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=60).run()
    assert not at.exception

    at.selectbox(key="temporada").select(2006).run()
    assert "America-MG" not in at.selectbox(key="equipe").options

    at.selectbox(key="temporada").select(2019).run()
    at.selectbox(key="equipe").select("Flamengo").run()
    m = {x.label: x.value for x in at.metric}
    assert m["Flamengo em casa"] == "53 pts"
    assert m["Flamengo fora"] == "37 pts"
    assert m["Total"] == "90 pts"
    assert m["Jogos"] == "38"


def test_aba_equipes_respeita_filtro_global():
    at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=60).run()
    at.sidebar.multiselect[0].set_value([2019]).run()
    assert at.selectbox(key="temporada").options == [2019]
    assert "America-MG" not in at.selectbox(key="equipe").options
    assert not at.exception
```

- [ ] **Step 5: Rodar e ver falhar**

```bash
.venv/bin/python -m pytest tests/test_app.py -q
```

Expected: `KeyError: 'temporada'` (os widgets ainda não têm `key`).

- [ ] **Step 6: Corrigir a aba Equipes em `app.py`**

Substituir o bloco `with t3:` (linhas 86–105) pela estrutura abaixo, mantendo a tabela e o download dentro do `else`:

```python
with t3:  # RF06 + RF07 + RF10
    col1, col2 = st.columns(2)
    temp = col1.selectbox(
        "Temporada", sorted(base["season"].unique().tolist()), key="temporada"
    )
    equipes = teams_in_season(base, int(temp))
    if not equipes:
        st.warning("Nenhuma equipe para a temporada selecionada. (RF10)")
        st.stop()
    if st.session_state.get("equipe") not in equipes:
        st.session_state["equipe"] = equipes[0]
    equipe = col2.selectbox("Equipe", equipes, key="equipe")

    ts = team_season(base, equipe, int(temp))
    if ts["home_n"] + ts["away_n"] == 0:
        st.warning(
            f"{equipe} não disputou a Série A em {temp}. "
            "Selecione outra temporada ou equipe. (RF10)"
        )
    else:
        c = st.columns(4)
        c[0].metric(...)  # manter os cartões atuais
        ...
        jogos = base[...].sort_values("date")
        st.dataframe(...)
        st.download_button(...)
```

Importar `teams_in_season` na linha 11: `from metrics import by_season, summarize, team_season, teams_in_season`.

- [ ] **Step 7: Rodar e ver passar**

```bash
.venv/bin/python -m pytest tests/ -q
```

Expected: `17 passed` (14 + 3 novos).

- [ ] **Step 8: Regenerar a Figura 3**

Com a aplicação aberta:

```bash
.venv/bin/python -m streamlit run app.py
```

Selecionar **Temporada 2019** e **Equipe Flamengo**; conferir os cartões `53 pts`, `37 pts`, `90 pts`, `38 jogos` e a tabela com 38 partidas; capturar a aba em `figuras/app3_equipes_partidas.png`. Atualizar a legenda em `figuras/LEGENDAS.md` para registrar o recorte usado. Não usar a captura antiga da América-MG 2006.

- [ ] **Step 9: Commit**

```bash
git add src/metrics.py app.py tests/test_metrics.py tests/test_app.py figuras/app3_equipes_partidas.png figuras/LEGENDAS.md
git commit -m "fix(app): corrige estado vazio e pontuação da aba Equipes"
```

---

## Task 4: Localização pt-BR e remoção de APIs depreciadas

**Files:**
- Create: `src/formatting.py`, `tests/test_formatting.py`
- Modify: `app.py:66-75`, `src/charts.py:13`, `:16`, `:25-26`, `:39`, `:50`

**Interfaces:**
- Produces: `pct(value: float | None, decimals: int = 1) -> str`, `num(value: float | None, decimals: int = 2) -> str`, `signed(value: float | None, decimals: int = 2) -> str`; todos usam vírgula decimal e `—` para `None`.

- [ ] **Step 1: Escrever o teste que falha**

Criar `tests/test_formatting.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from charts import outcome_distribution
from formatting import num, pct, signed


def test_formatacao_pt_br():
    assert pct(49.0) == "49,0%"
    assert pct(63.66, 2) == "63,66%"
    assert pct(None) == "—"
    assert num(1.49) == "1,49"
    assert num(None) == "—"
    assert signed(0.49) == "+0,49"
    assert signed(-2) == "-2,00"


def test_grafico_usa_separador_pt_br():
    fig = outcome_distribution({"p_home": 49.0, "p_draw": 26.8, "p_away": 24.1})
    assert fig.layout.separators == ",."
```

- [ ] **Step 2: Rodar e ver falhar**

```bash
.venv/bin/python -m pytest tests/test_formatting.py -q
```

Expected: `ModuleNotFoundError: No module named 'formatting'`.

- [ ] **Step 3: Implementar `src/formatting.py`**

```python
"""Formatação numérica pt-BR para a interface (RNF04)."""
from __future__ import annotations


def _fmt(value: float | None, decimals: int, sign: bool = False) -> str:
    if value is None:
        return "—"
    spec = f"+.{decimals}f" if sign else f".{decimals}f"
    return format(value, spec).replace(".", ",")


def pct(value: float | None, decimals: int = 1) -> str:
    if value is None:
        return "—"
    return f"{_fmt(value, decimals)}%"


def num(value: float | None, decimals: int = 2) -> str:
    return _fmt(value, decimals)


def signed(value: float | None, decimals: int = 2) -> str:
    return _fmt(value, decimals, sign=True)
```

- [ ] **Step 4: Usar a formatação no app e nos gráficos**

Em `app.py`, importar `from formatting import num, pct, signed` e trocar as linhas 67–74:

```python
c[1].metric("Vit. mandante", pct(resumo["p_home"]))
c[2].metric("Empates", pct(resumo["p_draw"]))
c[3].metric("Vit. visitante", pct(resumo["p_away"]))
...
c[0].metric("Gols/partida (casa)", num(resumo["avg_home_goals"]))
c[1].metric("Gols/partida (fora)", num(resumo["avg_away_goals"]))
c[2].metric("Diferença média", signed(resumo["goal_diff"]))
c[3].metric("Pollard", pct(resumo["pollard"], 2), help=...)
```

Em `src/charts.py`, importar `from formatting import pct`, usar `pct(v)` no texto das barras e adicionar `fig.update_layout(separators=",.")` em cada uma das quatro funções (ou criar `_pt_br(fig)` e retornar `_pt_br(fig)`).

- [ ] **Step 5: Remover `use_container_width`**

Em `app.py`, substituir todas as ocorrências de `use_container_width=True` por `width="stretch"` (Streamlit 1.66 já aceita). Rodar o AppTest e conferir que o aviso “Please replace `use_container_width`” não aparece mais.

- [ ] **Step 6: Rodar e ver passar**

```bash
.venv/bin/python -m pytest tests/test_formatting.py tests/test_app.py -q
.venv/bin/python -m pytest tests/ -q
```

Expected: `19 passed` (17 + 2 novos) e nenhum aviso de depreciação.

- [ ] **Step 7: Commit**

```bash
git add src/formatting.py src/charts.py app.py tests/test_formatting.py
git commit -m "feat(ui): formata números em pt-BR e remove APIs depreciadas"
```

---

## Task 5: Pipeline compatível com pandas 3 e download verificado

**Files:**
- Modify: `src/clean_data.py:18-23`, `:87-88`
- Create: `src/integrity.py`
- Modify: `scripts/fetch_raw.py:7-25`
- Test: `tests/test_data_validation.py`, `tests/test_integrity.py`
- Docs/config: `data/raw/FONTE.md`, `docs/data_dictionary.md:20`, `requirements.txt`, `requirements-lock.txt`, `requirements-dev.txt`, `README.md`

**Interfaces:**
- Produces: `_strip(df) -> pd.DataFrame` que apara colunas `object`/`string` e preserva `NA`; `sha256_file(path: Path) -> str`; `verify_sha256(path: Path, expected: str) -> None` (levanta `ValueError`).

- [ ] **Step 1: Escrever os testes que falham**

Em `tests/test_data_validation.py`, importar `_strip` e adicionar:

```python
from clean_data import _strip, clean_matches


def test_strip_remove_espacos_em_string_dtype():
    df = pd.DataFrame({"team": pd.Series([" Flamengo ", "São Paulo"], dtype="string")})
    out = _strip(df)
    assert out["team"].tolist() == ["Flamengo", "São Paulo"]


def test_clube_ausente_rejeitado():
    raw = _raw([{"mandante": "A", "visitante": "B", "hg": "1", "ag": "0"}])
    raw.loc[0, "mandante"] = None
    df, rep = clean_matches(raw)
    assert len(df) == 0
    assert rep["excluded"].get("clube_ausente", 0) == 1
```

Criar `tests/test_integrity.py`:

```python
import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from integrity import verify_sha256


def test_verify_sha256_aceita_e_rejeita(tmp_path):
    p = tmp_path / "arquivo.txt"
    p.write_bytes(b"abc")
    verify_sha256(p, hashlib.sha256(b"abc").hexdigest())
    with pytest.raises(ValueError, match="SHA-256"):
        verify_sha256(p, "0" * 64)
```

- [ ] **Step 2: Rodar e ver falhar**

```bash
.venv/bin/python -m pytest tests/test_data_validation.py tests/test_integrity.py -q
```

Expected: `_strip` não apara o dtype `string`; `clube_ausente` não é contabilizado; `ModuleNotFoundError` para `integrity`.

- [ ] **Step 3: Corrigir `_strip` e a ordem dos filtros**

Em `src/clean_data.py`:

```python
def _strip(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_string_dtype(df[c]) or df[c].dtype == object:
            df[c] = df[c].astype("string").str.strip()
    return df
```

Antes da comparação mandante × visitante, trocar as linhas 87–88 por:

```python
vazio = (
    df["home_team"].isna() | df["away_team"].isna()
    | df["home_team"].eq("") | df["away_team"].eq("")
)
df = drop(vazio.fillna(False), "clube_ausente", df)
df = drop(df["home_team"] == df["away_team"], "mandante_igual_visitante", df)
```

A ordem importa: sem remover `NA` antes, a comparação devolve `pd.NA` e o `drop` deixa de contar a exclusão.

- [ ] **Step 4: Implementar `src/integrity.py` e ligar no download**

```python
"""Verificação de integridade dos arquivos baixados."""
from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_sha256(path: Path, expected: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise ValueError(
            f"hash SHA-256 divergente para {path.name}: "
            f"esperado {expected}, obtido {actual}"
        )
```

Em `scripts/fetch_raw.py`, adicionar `sys.path` para `src`, importar `verify_sha256`, definir:

```python
SHA256 = {
    "campeonato-brasileiro-full.csv": "c09d03d36debfd7d7aee71da9a9f0909b5e420fc80a1705f215efc93c76e83fc",
    "Legenda.txt": "dfedf5fb55d9d7b178bce0e0e0b639c380d42d27af76a7d3ef1f1d6db6d1de1f",
}
```

Baixar para `.tmp`, chamar `verify_sha256(tmp, SHA256[nome])`, remover o `.tmp` em caso de erro e só então `tmp.replace(out)`. Adicionar `--check` para verificar os arquivos existentes sem baixar.

- [ ] **Step 5: Rodar e ver passar**

```bash
.venv/bin/python -m pytest tests/test_data_validation.py tests/test_integrity.py -q
```

Expected: todos passam.

- [ ] **Step 6: Regenerar a base e provar que só `stadium` mudou**

```bash
cp data/processed/matches_processed.csv /tmp/matches_before.csv
.venv/bin/python scripts/build_processed.py
.venv/bin/python - <<'PY'
import pandas as pd
a = pd.read_csv("/tmp/matches_before.csv")
b = pd.read_csv("data/processed/matches_processed.csv")
assert len(a) == len(b) == 7219
assert a.drop(columns=["stadium"]).equals(b.drop(columns=["stadium"]))
assert a["stadium"].str.strip().equals(b["stadium"])
print("ok: apenas stadium mudou (whitespace)")
PY
```

Expected: `lidas: 8785  mantidas: 7219`, exclusão única `fora_do_recorde_2006_2024: 1566`, e a mensagem `ok: apenas stadium mudou (whitespace)`. Se qualquer outro campo divergir, **parar** e investigar.

- [ ] **Step 7: Conferir os números principais**

```bash
.venv/bin/python - <<'PY'
import sys
import pandas as pd
sys.path.insert(0, "src")
from metrics import by_season, summarize
df = pd.read_csv("data/processed/matches_processed.csv")
s = summarize(df)
t = by_season(df)
assert s["n"] == 7219
assert round(s["p_home"], 1) == 49.0
assert round(s["p_draw"], 1) == 26.8
assert round(s["p_away"], 1) == 24.1
assert round(s["avg_home_goals"], 2) == 1.49
assert round(s["avg_away_goals"], 2) == 1.00
assert round(s["pollard"], 2) == 63.66
assert round(t.loc[t.season == 2017, "pollard"].iloc[0], 2) == 58.24
assert round(t.loc[t.season == 2018, "pollard"].iloc[0], 2) == 69.51
print("números principais preservados")
PY
```

Expected: `números principais preservados`.

- [ ] **Step 8: Atualizar dependências e documentação**

`requirements.txt`:

```text
pandas>=2.2,<4.0
plotly>=5.0,<8.0
streamlit>=1.30,<2.0
matplotlib>=3.0,<4.0
pytest>=8.0,<10.0
```

`requirements-lock.txt` (versões do `.venv` atual):

```text
pandas==3.1.0
plotly==7.1.0
streamlit==1.66.1
matplotlib==3.11.2
pytest==9.2.0
```

`requirements-dev.txt`:

```text
-r requirements-lock.txt
python-pptx==1.0.2
```

Atualizar `data/raw/FONTE.md` com os dois SHA-256 e tamanhos (1.187.343 e 2.113 bytes); atualizar `docs/data_dictionary.md:20` para “espaços removidos na limpeza”; no `README.md`, documentar `requirements-lock.txt` e o comando `python3 scripts/fetch_raw.py --check`.

- [ ] **Step 9: Rodar a suíte e o `pip check`**

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/pip check
```

Expected: `22 passed` (19 + 3 novos) e `No broken requirements found.`

- [ ] **Step 10: Commit**

```bash
git add src/clean_data.py src/integrity.py scripts/fetch_raw.py tests/test_data_validation.py tests/test_integrity.py data/raw/FONTE.md docs/data_dictionary.md requirements.txt requirements-lock.txt requirements-dev.txt README.md data/processed/matches_processed.csv data/processed/quality_report.json
git commit -m "fix(data): suporta pandas 3 e verifica integridade do download"
```

---

## Task 6: Fechar a monografia (correções editoriais e estruturais)

**Files:**
- Rename: `docs/monografia_v1.md` → `docs/monografia_v2.md`
- Modify: `docs/monografia_v2.md`, `figuras/LEGENDAS.md`, `docs/apresentacao_roteiro.md`
- Create: `scripts/export_table1.py`
- Test: comandos de verificação (sem teste unitário)

**Interfaces:**
- Consumes: números da Task 5, total de testes da Task 5.
- Produces: monografia sem TODO acionável, Tabela 1 no texto, figuras 1–8 em ordem, referências ABNT alfabéticas, apêndices A–D preenchidos.

- [ ] **Step 1: Renomear e limpar o cabeçalho**

```bash
git mv docs/monografia_v1.md docs/monografia_v2.md
```

Trocar a linha 3 para `> **Documento consolidado — versão 2 (04/11/2026).**` e transformar a linha 18 em comentário válido:

```markdown
<!-- Departamento confirmado: "Departamento de Computação e Tecnologia" (DCT), como nos TCCs do curso na BDM. -->
```

Verificar:

```bash
grep -n '^\s*-->' docs/monografia_v2.md
```

Expected: nenhuma saída.

- [ ] **Step 2: Explicitar H1 e H2**

Inserir ao final da §1.2:

```markdown
A pesquisa parte de duas hipóteses, formuladas antes da análise. **H1:** o índice de Pollard do período 2006–2024 será superior a 50%, indicando que os mandantes somaram mais pontos que os visitantes. **H2:** o índice não permanecerá constante entre as temporadas, com variação observável na série anual.
```

Inserir ao final da §3.4:

```markdown
H1 é avaliada pelo índice agregado do período; H2, pela comparação descritiva das 19 temporadas, sem teste inferencial. A escala adotada é a de Pollard (1986), conforme Almeida et al. (2011) e Matos, Amaro e Pollard (2020).
```

- [ ] **Step 3: Adicionar a nota Barueri/Grêmio Prudente**

Ao final da §3.3:

```markdown
A franquia Barueri (2009) e Grêmio Prudente (2010) é a mesma entidade renomeada entre temporadas; os nomes são mantidos separados e a comparação por equipe é sempre contextualizada pela temporada, sem fusão de identidades no pipeline.
```

- [ ] **Step 4: Gerar e inserir a Tabela 1**

Criar `scripts/export_table1.py` que lê `figuras/tab1_indicadores_temporada.csv` e imprime uma tabela Markdown com 11 colunas (Temporada, n, % V mandante, % Empates, % V visitante, Gols casa, Gols fora, Dif. gols, Pontos casa, Pontos fora, Pollard), usando vírgula decimal e duas casas.

Rodar:

```bash
.venv/bin/python scripts/export_table1.py > figuras/tab1_indicadores_temporada.md
```

Expected: 19 linhas de dados (2006–2024), primeira `| 2006 | 380 | 50,26 | ...` e última `| 2024 | 380 | 47,37 | ...`.

Inserir a tabela na §5.2, imediatamente após o parágrafo que cita a Figura 7 e antes da nota de 2016/2020. Adicionar a chamada `(Tabela 1)` no texto. Remover a linha `(Tabela 1 — indicadores por temporada, ...)`.

- [ ] **Step 5: Corrigir a §5.4**

No item 4, trocar “por equipe, ver Tabela 1 e aba ‘Equipes’ do dashboard” por:

```markdown
por equipe, ver a aba “Equipes e partidas” do dashboard (Figura 3); a Tabela 1 apresenta os indicadores por temporada, não por equipe.
```

- [ ] **Step 6: Renumerar as figuras 6 e 7**

Em `figuras/LEGENDAS.md`, inverter os blocos:

- **Figura 6** → `fig4_gols_temporadas.png` (média de gols).
- **Figura 7** → `fig2_pollard_temporadas.png` (Pollard por temporada).

Na monografia, atualizar a Lista de Figuras (linhas 82–85), a citação e o rótulo da §5.1 para **Figura 6** (gols) e a citação e o rótulo da §5.2 para **Figura 7** (Pollard). Manter os blocos na ordem física atual (5, 6, 7, 8). Atualizar a legenda da Figura 3 para “recorte: temporada 2019, equipe Flamengo”.

Verificar a ordem de primeira citação:

```bash
.venv/bin/python - <<'PY'
import re
t = open("docs/monografia_v2.md", encoding="utf-8").read()
body = t.split("# 1 INTRODUÇÃO", 1)[1]
nums = [int(n) for n in re.findall(r"Figura (\d)", body)]
first = []
for n in nums:
    if n not in first:
        first.append(n)
assert first == list(range(1, 9)), first
print("ordem das figuras:", first)
PY
```

Expected: `ordem das figuras: [1, 2, 3, 4, 5, 6, 7, 8]` (a lista pré-textual não conta).

- [ ] **Step 7: Fechar as referências**

Converter a lista numerada em lista alfabética ABNT (sem números), na ordem: ALMEIDA et al.; DUQUE; FEW; MATOS; NEVILL; OPENFOOTBALL; POLLARD; RIBEIRO et al.; SHARDA; SILVA; STREAMLIT. Preencher:

- STREAMLIT: `Acesso em: 4 nov. 2026.`
- NEVILL; HOLDER: decidir entre manter a entrada completa (`Sports Medicine, v. 28, n. 4, p. 221–236, 1999, DOI: 10.2165/00007256-199928040-00001`) ou remover a entrada e manter apenas o `apud` no texto. **Recomendação:** remover a entrada se o original não foi consultado; registrar a decisão no rodapé da lista.
- Remover todos os `[TODO]` de referências.

Conferir que cada citação autor-data do texto tem entrada correspondente e vice-versa:

```bash
grep -nE '\([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-Za-zÁÉÍÓÚÂÊÔÃÕÇ]+.*(19|20)[0-9]{2}' docs/monografia_v2.md
```

Expected: revisão manual; nenhuma citação órfã.

- [ ] **Step 8: Preencher os apêndices A–D**

- **A:** transcrever o dicionário de `docs/data_dictionary.md` (tabela de 13 colunas + regras + casos conhecidos).
- **B:** resumir `docs/auditoria_fase1.md` e o `quality_report.json`: 8.785 lidas, 1.566 fora do recorte, 7.219 mantidas, 2016 = 379.
- **C:** transcrever a tabela de `docs/validacao_cruzada.md` e o resultado `PASS — 19/19` de `docs/validacao_campeoes.md`.
- **D:** listar os testes de `tests/` e os comandos do `README.md`; usar o total obtido na Task 5.

- [ ] **Step 9: Marcar os TODOs bloqueados**

Trocar os TODOs acionáveis por tags explícitas: `[TODO-BANCA]` (2º/3º membros e data da defesa), `[TODO-SIGLAS]` (lista final), `[TODO-CBF]` (se o orientador exigir) e `[TODO-ORIENTADOR]` (revisão do Resumo/Abstract). Verificar:

```bash
grep -n 'TODO' docs/monografia_v2.md | grep -vE 'TODO-(BANCA|SIGLAS|CBF|ORIENTADOR)' || true
```

Expected: nenhuma saída (só as tags permitidas permanecem).

- [ ] **Step 10: Atualizar o roteiro da apresentação**

Em `docs/apresentacao_roteiro.md`, trocar as referências ambíguas “Fig. 1/2/4” por nomes de arquivo e figura da monografia:

- Slide 3: `fig1_distribuicao_geral.png` (Figura 5).
- Slide 4: `fig2_pollard_temporadas.png` (Figura 7).
- Slide 5: `fig4_gols_temporadas.png` (Figura 6).

Ajustar “sugestão: 8 slides” para “10 slides” e conferir a ordem com o deck real.

- [ ] **Step 11: Commit**

```bash
git add docs/monografia_v2.md figuras/LEGENDAS.md figuras/tab1_indicadores_temporada.md scripts/export_table1.py docs/apresentacao_roteiro.md
git commit -m "docs(monografia): corrige tabela, figuras, referências e pendências"
```

---

## Task 7: Gate de profundidade acadêmica

**Files:**
- Create: `docs/decisoes_orientador.md`
- Modify: `docs/monografia_v2.md`, `docs/resumo_orientador.md`

**Interfaces:**
- Consumes: monografia da Task 6.
- Produces: decisão registrada das 5 pendências do orientador; se aprovada a ampliação, corpo com meta mínima acordada.

> **Gate:** não iniciar os passos 7.3–7.5 sem resposta do orientador. Se a resposta for “profundidade suficiente”, registrar e pular para 7.6.

- [ ] **Step 1: Enviar o resumo e registrar as 5 decisões**

Criar `docs/decisoes_orientador.md` com uma tabela:

| # | Decisão | Resposta | Data | Impacto |
|---|---|---|---|---|
| 1 | Recorte 2006–2024 e título | | | |
| 2 | Dashboard como artefato de SI | | | |
| 3 | Fonte e plano B de licença | | | |
| 4 | Spearman/tendência | | | |
| 5 | Formato do curso e avaliação do software | | | |

Expected: as 5 linhas preenchidas; nenhuma célula “pendente”.

- [ ] **Step 2: Decidir se há ampliação**

Se o orientador exigir mais profundidade, seguir para 7.3. Caso contrário, registrar “mantido o escopo atual” e ir para 7.6.

- [ ] **Step 3: Aplicar o mapa de ampliação (condicional)**

| Seção | Atual (palavras) | Meta | Conteúdo novo | Fontes |
|---|---:|---:|---|---|
| 1.2/1.5 | ~331 | 700 | problema, hipóteses, contribuição | spec, Almeida, Ribeiro |
| 2.1 | 96 | 500 | mecanismos (torcida, viagem, arbitragem, familiaridade) | Pollard, Nevill, Matos |
| 2.2 | 137 | 600 | tabela de evidências brasileiras | Silva; Moreira, Almeida, Ribeiro |
| 2.3 | 108 | 450 | dashboard, análise descritiva, visualização | Few, Sharda |
| 3.1–3.4 | 332 | 900 | desenho, validação, ameaças à validade | spec, auditoria |
| 4.1–4.4 | 387 | 1.100 | arquitetura, rastreabilidade RF→tela→teste | código, testes |
| 5.3 | 80 | 500 | comparação com a literatura e 2020 | Almeida, Ribeiro, Matos |
| 6 | 181 | 500 | resposta, contribuição, limitações, futuros | resultados |

Expected: corpo total ≥ 5.500 palavras; se o orientador exigir 8.000+, ampliar 2.2 e 5.3 com novas fontes, não com repetição.

- [ ] **Step 4: Adicionar os artefatos estruturais**

Inserir, conforme o mapa:

- **Tabela 2 — Evidências da literatura** (estudo, período, amostra, métrica, resultado) na §2.2.
- **Tabela 3 — Matriz de rastreabilidade** (RF01–RF11, tela, evidência/teste) na §4.3.
- **Tabela 4 — Síntese dos testes** (teste, o que verifica, resultado) na §4.4 ou Apêndice D.

Atualizar a Lista de Tabelas e a numeração.

- [ ] **Step 5: Verificar a contagem de palavras**

```bash
.venv/bin/python - <<'PY'
import re
t = open("docs/monografia_v2.md", encoding="utf-8").read()
body = t.split("# 1 INTRODUÇÃO", 1)[1].split("# REFERÊNCIAS", 1)[0]
print("palavras do corpo:", len(re.findall(r"\b\w+\b", body)))
PY
```

Expected: valor ≥ meta acordada (referência: 5.500; ideal: 7.500).

- [ ] **Step 6: Revisão do orientador e commit**

```bash
git add docs/decisoes_orientador.md docs/monografia_v2.md docs/resumo_orientador.md
git commit -m "docs(monografia): registra decisões e amplia a fundamentação"
```

Se não houve ampliação: `git commit -m "docs: registra decisão de escopo do orientador"`.

---

## Task 8: Repositório, licença e release

**Files:**
- Modify: `.gitignore`, `README.md`, `data/raw/FONTE.md`
- Create: `NOTICE.md`, `data/processed/README.md`, `docs/arquivo/README.md`
- Move: `docs/cap*_rascunho.md`, `docs/monografia_esqueleto.md`, `docs/referencial_fichamentos.md` → `docs/arquivo/`
- Git index: remover `.playwright-mcp/`; decidir o CSV processado

**Interfaces:**
- Consumes: Tasks 1–7.
- Produces: repositório público sem dados brutos, sem logs e com PDFs de entrega rastreáveis; branch padrão atualizada.

- [ ] **Step 1: Remover os logs do Playwright do versionamento**

```bash
git rm -r --cached .playwright-mcp
git status --short
```

Expected: os dois arquivos aparecem como `D` no index; continuam no disco e ignorados.

- [ ] **Step 2: Gate de licença do CSV processado**

**Padrão recomendado (sem autorização escrita):**

```bash
git rm --cached data/processed/matches_processed.csv
```

Adicionar `data/processed/*.csv` ao `.gitignore`, criar `data/processed/README.md` explicando que o CSV é gerado por `scripts/build_processed.py` e não é redistribuído, e manter `quality_report.json` versionado.

**Se houver autorização:** manter o CSV, criar `data/raw/AUTORIZACAO.md` com data e escopo (sem dados pessoais) e atualizar `data/raw/FONTE.md`.

Verificar:

```bash
git ls-files data/raw/*.csv data/processed/*.csv
```

Expected (padrão): nenhuma saída.

- [ ] **Step 3: Versionar os PDFs de entrega**

No `.gitignore`, manter `*.pdf` e adicionar as exceções:

```gitignore
*.pdf
!apresentacao/apresentacao_tcc.pdf
!docs/monografia_final.pdf
```

Verificar e adicionar:

```bash
git check-ignore -v apresentacao/apresentacao_tcc.pdf || true
git add apresentacao/apresentacao_tcc.pdf
```

Expected: `git check-ignore` sem saída (arquivo não ignorado) e o PDF no index. O PDF da monografia entra quando existir.

- [ ] **Step 4: Criar o `NOTICE.md`**

```markdown
# Titularidade e proveniência

Código, dashboard e texto da monografia: © 2026 José Inamar de Medeiros Júnior.
Todos os direitos reservados. Não há concessão de licença aberta sem decisão expressa do autor.

Dados de partidas: fonte `adaoduque/Brasileirao_Dataset` (commit 15f027c), sem arquivo
LICENSE. O CSV bruto e o CSV processado completo não são redistribuídos neste
repositório; a reprodução ocorre por download pinado e script de construção.
OpenFootball (CC0-1.0) é usado apenas para validação cruzada.
```

Não adicionar licença MIT/CC sem decisão do autor e do orientador.

- [ ] **Step 5: Arquivar os rascunhos**

```bash
mkdir -p docs/arquivo
git mv docs/cap1_rascunho.md docs/cap2_rascunho.md docs/cap3_rascunho.md \
       docs/cap4_rascunho.md docs/cap5_rascunho.md docs/cap6_rascunho.md \
       docs/cap7_rascunho.md docs/monografia_esqueleto.md \
       docs/referencial_fichamentos.md docs/arquivo/
```

Criar `docs/arquivo/README.md` explicando que são materiais históricos, não a versão vigente. Atualizar as duas referências internas a `docs/referencial_fichamentos.md` para `docs/arquivo/referencial_fichamentos.md`.

- [ ] **Step 6: Atualizar o README**

Incluir:

- instalação com `requirements-lock.txt`;
- `python3 scripts/fetch_raw.py --check` e o fluxo completo;
- aviso de que `data/processed/matches_processed.csv` é gerado localmente;
- contagem final de testes (a da Task 5);
- link para `docs/monografia_v2.md` e para o PDF final quando existir.

- [ ] **Step 7: Atualizar a branch padrão**

```bash
git push origin main
gh auth status
gh api -X PATCH repos/EmiyaKiritsugu3/TCC -f default_branch=main
```

Fallback se `gh` não estiver autenticado:

```bash
git push origin main:master
```

Verificar:

```bash
git ls-remote --symref origin HEAD
```

Expected: `refs/heads/main` (ou `master` apontando para o mesmo commit de `main`).

- [ ] **Step 8: Commit**

```bash
git add .gitignore README.md NOTICE.md data/raw/FONTE.md data/processed/README.md docs/arquivo
git commit -m "chore(repo): prepara versão de depósito e defesa"
```

---

## Task 9: QA final e release

**Files:**
- Create: `docs/qa_final.md`
- Tag: `v1.0-banca`

**Interfaces:**
- Consumes: todas as tarefas anteriores.
- Produces: evidência de reprodutibilidade em worktree limpo, PDFs conferidos, tag e release.

- [ ] **Step 1: Simular um clone limpo**

```bash
git worktree remove --force /tmp/opencode/tcc-qa 2>/dev/null || true
git worktree add /tmp/opencode/tcc-qa HEAD
cd /tmp/opencode/tcc-qa
python3 -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
.venv/bin/python scripts/fetch_raw.py
.venv/bin/python scripts/build_processed.py
.venv/bin/python -m pytest tests/ -q
.venv/bin/python scripts/validate_cross.py
.venv/bin/python scripts/validate_champions.py
```

Expected: hash verificado; `mantidas: 7219`; `22 passed`; `PASS — bases idênticas`; `PASS — 19/19 campeões`.

- [ ] **Step 2: Smoke test da aplicação (de volta ao repositório principal)**

```bash
cd /home/emiyakiritsugu/Projetos_Antigravity/TCC_00
.venv/bin/python -m pytest tests/test_app.py -q
.venv/bin/python -m streamlit run app.py
```

Conferir manualmente: 4 abas; filtro 2020 mostra Pollard `60,17%`; Flamengo 2019 mostra `53/37/90/38`; nenhuma equipe fora da temporada aparece; aba Metodologia exibe o relatório de qualidade; download CSV funciona.

- [ ] **Step 3: Consistência numérica e de contagem**

```bash
.venv/bin/python -m pytest tests/ -q
grep -RIn --exclude-dir=superpowers '12 testes\|Doze testes\|0 pts\|55 pts\|108 pts' README.md docs apresentacao || true
```

Expected: `22 passed`; nenhuma ocorrência obsoleta. Atualizar README, monografia, resumo do orientador e deck para a contagem final.

- [ ] **Step 4: Checagens da monografia**

```bash
.venv/bin/python - <<'PY'
import re
t = open("docs/monografia_v2.md", encoding="utf-8").read()
body = t.split("# 1 INTRODUÇÃO", 1)[1]
nums = [int(n) for n in re.findall(r"Figura (\d)", body)]
first = []
for n in nums:
    if n not in first:
        first.append(n)
assert first == list(range(1, 9)), first
assert len(re.findall(r"^\| 20\d\d \|", t, re.M)) == 19
print("figuras e tabela ok")
PY
grep -n 'TODO' docs/monografia_v2.md | grep -vE 'TODO-(BANCA|SIGLAS|CBF|ORIENTADOR)' || true
```

Expected: `figuras e tabela ok`; nenhuma saída no segundo comando.

- [ ] **Step 5: Checagens do deck e exportação do PDF**

```bash
.venv/bin/python - <<'PY'
from pptx import Presentation
p = Presentation("apresentacao/apresentacao_tcc.pptx")
assert len(p.slides) == 10
text = "\n".join(
    shape.text for slide in p.slides for shape in slide.shapes if shape.has_text_frame
)
assert "63,7%" in text
assert "github.com/EmiyaKiritsugu3/TCC" in text
assert "22 testes" in text
assert "12 testes" not in text
print("deck ok: 10 slides e números atualizados")
PY
libreoffice --headless --convert-to pdf --outdir apresentacao apresentacao/apresentacao_tcc.pptx
pdfinfo apresentacao/apresentacao_tcc.pdf | grep Pages
```

Expected: `deck ok: 10 slides e números atualizados` e `Pages: 10`.

- [ ] **Step 6: Gerar/verificar o PDF da monografia**

Converter `docs/monografia_v2.md` para o template UFRN (DOCX) e exportar `docs/monografia_final.pdf`. Conferir: capa, folha de rosto, folha de avaliação, listas, sumário, figuras 1–8 na ordem, Tabela 1 com 19 linhas, referências alfabéticas, apêndices A–D, paginação e margens (3 cm esq. / 2 cm dir., A4, 1,5).

Se o template do curso não estiver disponível, registrar o bloqueio em `docs/decisoes_orientador.md` e usar o modelo da Resolução 001/2016-CSI como referência.

- [ ] **Step 7: Registrar o QA**

Criar `docs/qa_final.md` com data, comandos executados, saídas e links para os PDFs. Commitar:

```bash
git add docs/qa_final.md apresentacao/apresentacao_tcc.pdf
[ -f docs/monografia_final.pdf ] && git add docs/monografia_final.pdf || true
git commit -m "docs: registra QA final e artefatos de entrega"
```

- [ ] **Step 8: Tag e release**

```bash
git tag -a v1.0-banca -m "Versão de defesa"
git push origin v1.0-banca
ASSETS="apresentacao/apresentacao_tcc.pdf apresentacao/apresentacao_tcc.pptx"
[ -f docs/monografia_final.pdf ] && ASSETS="docs/monografia_final.pdf $ASSETS"
gh release create v1.0-banca $ASSETS \
  --title "TCC — versão de defesa" \
  --notes "Dashboard, monografia e apresentação da defesa. Ver docs/qa_final.md."
```

Expected: tag e release publicados; `git status --porcelain` vazio; `git log --oneline -12` com todos os commits.

---

## Cobertura dos requisitos da spec

| Requisito | Onde é tratado |
|---|---|
| RF01 — carregar base validada | Task 5 (build + hash) e README |
| RF02 — filtrar temporadas | Task 3 (filtro global) e AppTest |
| RF03 — indicadores gerais | Task 4 (formatação) e Task 9 (números) |
| RF04 — comparar temporadas | Task 6 (Tabela 1) e Task 9 |
| RF05 — comparar gols | Task 6 (Figura 6) |
| RF06 — consultar equipe | Tasks 2 e 3 |
| RF07 — tabela de partidas | Task 3 |
| RF08 — explicar indicadores | app.py (já existente) e Task 4 |
| RF09 — informações dos dados | app.py e Task 8 (licença/proveniência) |
| RF10 — filtros sem resultado | Task 3 (opções filtradas + warning) |
| RF11 — exportar CSV | app.py (já existente); conferir no QA |
| RNF01–RNF08 | Global Constraints + Tasks 4, 5 e 8 |

---

## Self-review do plano

- **Cobertura:** os 8 achados P0/P1 e os 2 P2 têm tarefa; RF01–RF11 estão mapeados; as 5 decisões do orientador têm gate.
- **Testes:** cada correção de código tem teste que falha antes; a contagem esperada sobe de 12 → 14 → 17 → 19 → 22.
- **Tipos:** `team_season` devolve pontos `int`; `teams_in_season` devolve `list[str]`; `pct`/`num`/`signed` devolvem `str`; `verify_sha256` devolve `None` ou levanta `ValueError`.
- **Riscos:** a única mudança de dados é `stadium` (whitespace); qualquer outra divergência para a Task 5.
- **Fora de escopo:** Spearman, previsão, novas fontes e redesenho amplo.
