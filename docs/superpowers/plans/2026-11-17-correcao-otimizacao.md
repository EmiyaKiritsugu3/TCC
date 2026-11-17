# Correção e Otimização do TCC_00 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Levar o projeto de um estado tecnicamente saudável, mas documentalmente inconsistente, a um estado de depósito auditável: auditoria que detecta números obsoletos, documentação sincronizada, scripts robustos e CI completo.

**Architecture:** Seis fases incrementais (consolidação, correção do número de testes com guarda anti-regressão, sincronização documental, robustez, qualidade de código, CI/cobertura). Cada tarefa termina com a cadeia de validação verde e um commit atômico; rollback é sempre `git revert`, nunca `reset --hard`.

**Tech Stack:** Python ≥3.11, pandas, pytest, Plotly, Streamlit, GitHub Actions, `python-docx`/reportlab via `build_docx.py`.

**Spec:** `docs/superpowers/specs/2026-11-17-correcao-otimizacao-design.md`

## Global Constraints

- Use `requirements-lock.txt` para o ambiente validado; `requirements.txt` para faixas compatíveis; `requirements-dev.txt` para extras de desenvolvimento.
- Prose de usuário, rótulos e testes em PT-BR; nomes de clubes sem acento em código de dados.
- Importe módulos de `src/` no topo (`from metrics import summarize`) com `PYTHONPATH=src` ou pacote instalado (`pip install -e .`); nunca imports relativos de pacote.
- `docs/monografia_v2.md` é o texto vigente; `docs/arquivo/` é histórico e não deve ser editado.
- Testes de integração devem continuar marcados `@pytest.mark.integration` e dar skip explícito quando `data/processed/matches_processed.csv` estiver ausente.
- Scripts são entry points autônomos, executados da raiz do repositório.
- NUNCA commitar/redistribuir `data/raw/*.csv`, `data/raw/*.txt`, `data/processed/matches_processed.csv` ou PDFs de `books/`.
- Não introduzir alegação causal, previsão, IA ou apostas.
- Indicadores validados não podem mudar: 7.219 partidas; 49,0/26,8/24,1%; 1,49×1,00 gols; Pollard 63,66%; 2.659/2.660; 19/19.

## Review Focus

| # | Entrada / condição não coberta | Comportamento esperado | Tarefa que fixa o teste |
|---|---|---|---|
| 1 | Auditor com número de testes desatualizado na monografia | Deve falhar (exit 1), não validar o número errado | Task 2 — `test_auditor_rejeita_numero_desatualizado` |
| 2 | Auditor com cabeçalho de seção ausente (`# REFERÊNCIAS`) | Deve falhar com mensagem objetiva, sem `IndexError`/traceback | Task 5 — `test_auditor_rejeita_cabecalho_ausente` |
| 3 | Arquivo OpenFootball com linha de jogo antes de qualquer linha de data | Deve levantar `ValueError` com mensagem clara, não `UnboundLocalError` | Task 7 — `test_jogo_antes_da_data_falha_com_mensagem` |
| 4 | `travel_km` com clube ausente em `CLUB_COORDS` | Deve levantar `ValueError` nomeando o clube, não `KeyError` opaco | Task 7 — `test_travel_km_clube_nao_mapeado_falha` |
| 5 | Comparação OpenFootball com 1 exclusivo de cada lado e 0 divergência de placar fora da exceção conhecida | Não deve ser silenciosamente tolerada como "exceção conhecida" | Task 6 — `test_toleranca_excecao_rejeita_fora_do_caso_conhecido` |

---

### Task 1: Consolidar o baseline do working tree

**Files:**
- Modify: `docs/decisoes_orientador.md`, `docs/resumo_orientador.md`, `docs/monografia_v2.md`, `docs/monografia_draft_abnt.docx`, `docs/monografia_draft_abnt.pdf` (já modificados)
- Create: `docs/email_orientador_preparado.txt`, `docs/email_autor_dataset_preparado.txt` (já untracked, versionar)
- Ignore: `.omo/`

**Interfaces:**
- Consumes: nada (primeira tarefa).
- Produces: `working tree` limpo; baseline com os 5 arquivos modificados + 2 e-mails versionados.

- [ ] **Step 1: Inspecionar as mudanças pendentes**

Run: `git diff --stat && git status --short`
Expected: 5 arquivos modificados listados na auditoria + `.omo/` e 2 e-mails untracked.

- [ ] **Step 2: Confirmar que as mudanças pendentes passam nas validações**

Run: `PYTHONPATH=src python3 -m pytest tests/ -q && PYTHONPATH=src python3 scripts/check_monografia.py`
Expected: `52 passed` e `AUDITORIA NUMÉRICA: tudo confere`.

- [ ] **Step 3: Versionar baseline e artefatos de entrega**

Adicionar ao `.gitignore` a entrada `.omo/` (ferramenta local, não artefato do projeto). Fazer `git add` **apenas** dos 5 arquivos modificados, dos 2 e-mails e do `.gitignore`. Não usar `git add -A`.

```bash
git add .gitignore docs/decisoes_orientador.md docs/resumo_orientador.md \
  docs/monografia_v2.md docs/monografia_draft_abnt.docx docs/monografia_draft_abnt.pdf \
  docs/email_orientador_preparado.txt docs/email_autor_dataset_preparado.txt
git commit -m "docs: consolida baseline de entrega e comunicacoes preparadas"
```

- [ ] **Step 4: Verificar o gate**

Run: `git status --short`
Expected: nenhuma saída (working tree limpo).

---

### Task 2: Tornar o auditor testável e criar a guarda anti-número-obsoleto

**Files:**
- Modify: `scripts/check_monografia.py:1-35` (e encapsular o corpo em funções)
- Test: `tests/test_check_monografia_guard.py` (novo)

**Interfaces:**
- Consumes: `scripts/check_monografia.py` atual (corpo no import, `RAIZ` em `:11`).
- Produces:
  - `conferir(texto: str, df: pd.DataFrame, tab1: pd.DataFrame) -> list[str]` — executa todas as conferências e devolve mensagens de divergência.
  - `main(argv: list[str] | None = None) -> int` — CLI com `--monografia PATH` (padrão `RAIZ/docs/monografia_v2.md`); retorna 0 se sem erros, 1 caso contrário.
  - Teste `test_auditor_rejeita_numero_desatualizado` — fixa o Review Focus #1.

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_check_monografia_guard.py
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _auditar_com_texto(tmp_path, texto):
    alvo = tmp_path / "monografia.md"
    alvo.write_text(texto, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(RAIZ / "scripts" / "check_monografia.py"),
         "--monografia", str(alvo)],
        cwd=RAIZ, capture_output=True, text=True,
        env={"PYTHONPATH": "src", "PATH": "/usr/bin:/bin"},
    )


def test_auditor_rejeita_numero_desatualizado(tmp_path):
    texto = (RAIZ / "docs" / "monografia_v2.md").read_text(encoding="utf-8")
    resultado = _auditar_com_texto(tmp_path, texto.replace("31 testes", "99 testes"))
    assert resultado.returncode == 1
    assert "DIVERGÊNCIA" in resultado.stdout
```

Nota: o teste troca apenas a ocorrência já presente no texto atual (`31 testes`); na Task 3 o texto passará a conter `52 testes` e o teste deve ser ajustado para `.replace("52 testes", "99 testes")`.

- [ ] **Step 2: Rodar o teste e confirmar a falha**

Run: `PYTHONPATH=src python3 -m pytest tests/test_check_monografia_guard.py -v`
Expected: FAIL — `argparse: unrecognized arguments: --monografia` (ou equivalente).

- [ ] **Step 3: Refatorar `check_monografia.py` para expor `conferir` e `main`**

Mover todo o código de leitura e conferência de `scripts/check_monografia.py:26` em diante para dentro de `conferir(texto, df, tab1) -> list[str]`, usando `texto` no lugar da variável global `T`. Manter `confere()` como auxiliar que acumula erros. Acrescentar `argparse` em `main(argv)`, com `--monografia` do tipo `Path`. Manter as mensagens `DIVERGÊNCIA: ...` e o "AUDITORIA NUMÉRICA: tudo confere" finais. Adicionar `if __name__ == "__main__": raise SystemExit(main())`. Não alterar nenhum número conferido nesta tarefa.

- [ ] **Step 4: Rodar o teste e confirmar a passagem**

Run: `PYTHONPATH=src python3 -m pytest tests/test_check_monografia_guard.py -v`
Expected: PASS.

- [ ] **Step 5: Rodar a cadeia completa**

Run: `PYTHONPATH=src python3 -m pytest tests/ -q && PYTHONPATH=src python3 scripts/check_monografia.py`
Expected: `53 passed` e auditoria confere.

- [ ] **Step 6: Commit**

```bash
git add scripts/check_monografia.py tests/test_check_monografia_guard.py
git commit -m "test: auditor expose conferir e rejeita numero desatualizado"
```

---

### Task 3: Corrigir 31 → 52 em todos os artefatos

**Files:**
- Modify: `docs/monografia_v2.md:218,353,557,573`, `:359-364` (Tabela 4), `:8`
- Modify: `scripts/check_monografia.py:53` (string exigida)
- Modify: `tests/test_check_monografia_guard.py` (ajuste do `.replace`)
- Modify: `apresentacao/apresentacao_tcc.pptx` (slide 9)
- Regenerate: `docs/monografia_draft_abnt.docx`, `docs/monografia_draft_abnt.pdf`

**Interfaces:**
- Consumes: `conferir`, `main --monografia` da Task 2.
- Produces: número real 52 (48 rápidos + 4 integração) em monografia, deck e auditor; Tabela 4 com os 12 arquivos de teste.

- [ ] **Step 1: Atualizar o teste de guarda para o número novo**

Trocar `.replace("31 testes", "99 testes")` por `.replace("52 testes", "99 testes")` em `tests/test_check_monografia_guard.py`. Rodar o teste isolado: Expected FAIL (ainda não há 52 no texto).

- [ ] **Step 2: Substituir as ocorrências**

Em `docs/monografia_v2.md`: `31 testes` → `52 testes` (`:218`, `:573`), `Trinta e um testes automatizados` → `Cinquenta e dois testes automatizados` (`:353`), `31 passed` → `52 passed` (`:353`, `:557`). Em `:353` e `:573`, detalhar `48 rápidos + 4 de integração`.

Em `scripts/check_monografia.py:53`: trocar `"31 testes", "31 passed"` por `"52 testes", "52 passed"`.

- [ ] **Step 3: Reconstruir a Tabela 4**

Em `docs/monografia_v2.md:359-364`, substituir as 6 linhas atuais (9+9+8+2+2+1 = 31) pelas 12 linhas reais, com contagens: `test_metrics.py` 9, `test_context.py` 9, `test_data_validation.py` 8, `test_load_data.py` 5, `test_openfootball.py` 4, `test_charts_composicao.py` 3, `test_clean_data_pipeline.py` 3, `test_context_tabela.py` 3, `test_metrics_indicadores.py` 3, `test_app.py` 2, `test_formatting.py` 2, `test_integrity.py` 1. Total 48 rápidos; acrescentar linha `integração (AppTest + base real)` = 4. Total 52.

- [ ] **Step 4: Atualizar a nota introdutória**

Em `docs/monografia_v2.md:8`, trocar a referência a `[TODO-BANCA]/[TODO-CBF]/[TODO-ORIENTADOR]` por `[PENDENTE - ORIENTADOR]`, refletindo as substituições já feitas em `:70,72,130,279`.

- [ ] **Step 5: Regenerar artefatos**

Run: `PYTHONPATH=src python3 scripts/build_docx.py`
Expected: `.docx` e `.pdf` regenerados sem erro. Para o PPTX, editar o slide 9 de `apresentacao/apresentacao_tcc.pptx`: `31 testes` → `52 testes`.

- [ ] **Step 6: Verificar**

Run: `PYTHONPATH=src python3 -m pytest tests/ -q && PYTHONPATH=src python3 scripts/check_monografia.py`
Expected: `53 passed` e auditoria confere. Conferir manualmente: `grep -n "31 testes\|31 passed\|Trinta e um" docs/monografia_v2.md` → sem saída.

- [ ] **Step 7: Commit**

```bash
git add docs/monografia_v2.md docs/monografia_draft_abnt.docx \
  docs/monografia_draft_abnt.pdf apresentacao/apresentacao_tcc.pptx \
  scripts/check_monografia.py tests/test_check_monografia_guard.py
git commit -m "fix: corrige contagem de testes de 31 para 52 na monografia e auditoria"
```

---

### Task 4: Sincronizar documentação stale

**Files:**
- Modify: `docs/qa_final.md:7,18,26,27,28,32,39`
- Modify: `docs/comunicacoes_pendentes.md:1,16,18`
- Modify: `docs/resumo_orientador.md` (conferência final)
- Modify: `AGENTS.md:4` (commit de origem do knowledge base)

**Interfaces:**
- Consumes: texto corrigido da Task 3.
- Produces: nenhum número obsoleto em docs vigentes (critério S3).

- [ ] **Step 1: Localizar todos os valores obsoletos**

Run: `grep -R -n "22 testes\|31 testes\|31 passed\|Trinta e um\|5\.511\|v1\.0-banca\|9b9540c" docs/ AGENTS.md --exclude-dir=arquivo`
Expected: lista de ocorrências em `qa_final.md`, `comunicacoes_pendentes.md` e `AGENTS.md`.

- [ ] **Step 2: Atualizar os valores**

Em `docs/qa_final.md`: `22 testes` → `52 testes` (`:7,:18,:32`), `5.511 palavras` → `5.994 palavras` (`:27`), e a menção a tags `[TODO-...]` (`:26`) → `[PENDENTE - ORIENTADOR]`. Em `:32`, corrigir também a contagem atribuída ao PPTX (22 → 52).

Em `docs/comunicacoes_pendentes.md`: `22 testes` → `52 testes` (`:18`); atualizar referência de release/commit para o HEAD vigente.

Em `AGENTS.md:4`: atualizar `Commit:` para `5ee7bb1` ou HEAD vigente após os commits deste plano.

- [ ] **Step 3: Verificar o gate**

Run: `grep -R -n "22 testes\|31 testes\|31 passed\|5\.511" docs/ --exclude-dir=arquivo`
Expected: nenhuma saída.

- [ ] **Step 4: Commit**

```bash
git add docs/qa_final.md docs/comunicacoes_pendentes.md docs/resumo_orientador.md AGENTS.md
git commit -m "docs: sincroniza contagens e referencias de versao"
```

---

### Task 5: Proteger o auditor contra cabeçalhos ausentes

**Files:**
- Modify: `scripts/check_monografia.py` (código de extração de seções, antes das splits de Tabela 1 e referências)
- Test: `tests/test_check_monografia_guard.py` (acrescentar teste)

**Interfaces:**
- Consumes: `conferir(texto, df, tab1) -> list[str]` da Task 2.
- Produces: `test_auditor_rejeita_cabecalho_ausente` — fixa o Review Focus #2.

- [ ] **Step 1: Escrever o teste que falha**

Acrescentar ao arquivo de teste:

```python
def test_auditor_rejeita_cabecalho_ausente(tmp_path):
    texto = (RAIZ / "docs" / "monografia_v2.md").read_text(encoding="utf-8")
    sem_referencias = texto.replace("# REFERÊNCIAS", "# REFERENCIAS")
    resultado = _auditar_com_texto(tmp_path, sem_referencias)
    assert resultado.returncode == 1
    assert "DIVERGÊNCIA" in resultado.stdout
    assert "Traceback" not in resultado.stderr
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run: `PYTHONPATH=src python3 -m pytest tests/test_check_monografia_guard.py -v`
Expected: FAIL — o código atual levanta `IndexError` (traceback no stderr).

- [ ] **Step 3: Implementar o guarda**

Antes de cada `split("...", 1)[1]` em `conferir`, verificar se o marcador existe; se faltar, chamar `confere(False, f"cabeçalho ausente: {marcador!r}")` e usar `""` como fallback. Aplicar aos marcadores `**Tabela 1` e `# REFERÊNCIAS`. Nenhuma outra conferência muda.

- [ ] **Step 4: Rodar e confirmar a passagem**

Run: `PYTHONPATH=src python3 -m pytest tests/test_check_monografia_guard.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/check_monografia.py tests/test_check_monografia_guard.py
git commit -m "fix: auditor falha com mensagem clara se cabecalho ausente"
```

---

### Task 6: Robustez de `fetch_raw.py` e `validate_cross.py`

**Files:**
- Modify: `scripts/fetch_raw.py:28,45` e timeout em `urlretrieve`
- Modify: `scripts/validate_cross.py:13-22,37-39`
- Create: `scripts/validacao_excecoes.py` (função pura da regra de exceção)
- Test: `tests/test_validate_cross_excecao.py` (novo)

**Interfaces:**
- Consumes: `KNOWN_DATE_EXCEPTIONS` e `comparar` atuais.
- Produces:
  - `excecao_conhecida(ano: int, so_base: pd.DataFrame, so_of: pd.DataFrame, placar_divergente: int) -> bool` em `scripts/validacao_excecoes.py`.
  - `test_toleranca_excecao_rejeita_fora_do_caso_conhecido` — fixa o Review Focus #5.

- [ ] **Step 1: Escrever o teste da regra de exceção**

```python
import pandas as pd
from validacao_excecoes import excecao_conhecida

def test_toleranca_excecao_aceita_caso_conhecido():
    base = pd.DataFrame([{"date": "2023-10-22", "home_team": "Botafogo-RJ", "away_team": "Athletico-PR"}])
    of = pd.DataFrame([{"date": "2023-10-21", "home_team": "Botafogo-RJ", "away_team": "Athletico-PR"}])
    assert excecao_conhecida(2023, base, of, 0) is True

def test_toleranca_excecao_rejeita_fora_do_caso_conhecido():
    base = pd.DataFrame([{"date": "2022-05-10", "home_team": "Flamengo", "away_team": "Vasco"}])
    of = pd.DataFrame([{"date": "2022-05-09", "home_team": "Flamengo", "away_team": "Vasco"}])
    assert excecao_conhecida(2022, base, of, 0) is False
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run: `PYTHONPATH=src:scripts python3 -m pytest tests/test_validate_cross_excecao.py -v`
Expected: FAIL — módulo `validacao_excecoes` não existe.

- [ ] **Step 3: Implementar a função**

Criar `scripts/validacao_excecoes.py` com `excecao_conhecida(...)` encapsulando a lógica exata hoje em `validate_cross.py:37-39`: exige `len(so_base)==1`, `len(so_of)==1`, ambos na tupla `KNOWN_DATE_EXCEPTIONS` e `placar_divergente == 0`. Mover `KNOWN_DATE_EXCEPTIONS` para este módulo. Importar em `validate_cross.py` e substituir o bloco inline pela chamada.

- [ ] **Step 4: Rodar e confirmar a passagem**

Run: `PYTHONPATH=src:scripts python3 -m pytest tests/test_validate_cross_excecao.py -v && PYTHONPATH=src python3 scripts/validate_cross.py`
Expected: 2 testes PASS + `RESULTADO: PASS — bases idênticas`.

- [ ] **Step 5: Endurecer `fetch_raw.py`**

Trocar `sys.argv` por `argparse` com flag `--check`; trocar `except BaseException` por `except (OSError, ValueError)`; passar `timeout=60` ao `urlretrieve`. Manter idempotência via `.tmp` + `replace`.

- [ ] **Step 6: Verificar e commitar**

Run: `PYTHONPATH=src python3 scripts/fetch_raw.py --check`
Expected: `OK. Arquivos conferidos.`

```bash
git add scripts/fetch_raw.py scripts/validate_cross.py scripts/validacao_excecoes.py tests/test_validate_cross_excecao.py
git commit -m "refactor: isola regra de excecao e endurece fetch_raw"
```

---

### Task 7: Proteger parser OpenFootball e `travel_km`

**Files:**
- Modify: `src/openfootball.py:63-109`
- Modify: `src/context.py:72-82`
- Test: `tests/test_openfootball.py` (acrescentar teste)
- Test: `tests/test_context.py` (acrescentar teste)

**Interfaces:**
- Consumes: `parse_arquivo(path: str | Path, temporada: int) -> pd.DataFrame`, `travel_km(df: pd.DataFrame) -> pd.Series`, `CLUB_COORDS`.
- Produces:
  - `test_jogo_antes_da_data_falha_com_mensagem` — fixa o Review Focus #3.
  - `test_travel_km_clube_nao_mapeado_falha` — fixa o Review Focus #4.

- [ ] **Step 1: Escrever os testes que falham**

```python
# em tests/test_openfootball.py
def test_jogo_antes_da_data_falha_com_mensagem(tmp_path):
    arquivo = tmp_path / "2024_br1.txt"
    arquivo.write_text("Flamengo 2 v 1 Vasco\n", encoding="utf-8")
    import pytest
    with pytest.raises(ValueError, match="data"):
        parse_arquivo(arquivo, 2024)

# em tests/test_context.py
def test_travel_km_clube_nao_mapeado_falha():
    import pytest
    df = pd.DataFrame([{"home_team": "Flamengo", "away_team": "Clube Inexistente"}])
    with pytest.raises(ValueError, match="Clube Inexistente"):
        travel_km(df)
```

- [ ] **Step 2: Rodar e confirmar as falhas**

Run: `PYTHONPATH=src python3 -m pytest tests/test_openfootball.py::test_jogo_antes_da_data_falha_com_mensagem tests/test_context.py::test_travel_km_clube_nao_mapeado_falha -v`
Expected: FAIL (respectivamente `UnboundLocalError` e `KeyError`).

- [ ] **Step 3: Implementar os guardas**

Em `parse_arquivo`, inicializar `data_iso: str | None = None` antes do loop e, no branch de jogo, levantar `ValueError(f"Jogo sem data anterior em {path}")` se `data_iso is None`. Em `travel_km`, antes do cálculo, validar `h in CLUB_COORDS` e `a in CLUB_COORDS`, levantando `ValueError(f"Clube sem coordenadas: {clube!r}")`.

- [ ] **Step 4: Rodar e confirmar a passagem**

Run: `PYTHONPATH=src python3 -m pytest tests/test_openfootball.py tests/test_context.py -v`
Expected: todos PASS.

- [ ] **Step 5: Verificar cadeia e commitar**

Run: `PYTHONPATH=src python3 -m pytest tests/ -q && PYTHONPATH=src python3 scripts/check_monografia.py`
Expected: `58 passed` e auditoria confere.

```bash
git add src/openfootball.py src/context.py tests/test_openfootball.py tests/test_context.py
git commit -m "fix: guardas explicitas para data ausente e clube sem coordenadas"
```

---

### Task 8: Decompor funções longas

**Files:**
- Modify: `scripts/audit_fase1.py:24-208` (`main` 185 linhas), `:189` (`norm` morta)
- Modify: `scripts/build_docx.py:112-232` (`main` 121 linhas), `:21,39` (`import re` duplicado), `:193` (`pass` intencional — documentar com comentário)
- Modify: `src/clean_data.py:54-157` (`clean_matches` 103 linhas)

**Interfaces:**
- Consumes: comportamento atual das três funções.
- Produces: mesmas assinaturas públicas; helpers privados com nomes descritivos; nenhuma mudança de resultado.

- [ ] **Step 1: Capturar o comportamento atual como referência**

Run: `PYTHONPATH=src python3 scripts/audit_fase1.py data/raw/campeonato-brasileiro-full.csv > /tmp/audit_antes.txt && PYTHONPATH=src python3 scripts/build_docx.py && sha256sum docs/monografia_draft_abnt.docx`
Expected: arquivos gerados e hash registrado.

- [ ] **Step 2: Decompor `audit_fase1.main`**

Extrair helpers privados (por exemplo `_carregar`, `_normalizar`, `_resumo_duplicatas`, `_resumo_placares`, `_imprimir`) mantendo a ordem de execução e as mensagens. Remover `prev_r` (`:78,:89`) e a função `norm` não chamada (`:189`).

- [ ] **Step 3: Decompor `build_docx.main`**

Extrair helpers para parsing de blocos Markdown, renderização de figuras e montagem do documento. Remover `import re` duplicado (manter apenas o do topo). Manter o `pass` de `:193` com comentário `# branch intencionalmente vazia: PRE_CENTRALIZAR`.

- [ ] **Step 4: Decompor `clean_matches`**

Extrair helpers para normalização, deduplicação, derivação de resultado e montagem do relatório de exclusões. Remover `prev_r` (`:37,:49`) e `winner_raw` (`:74`, campo audit-only que não entra no schema). Preservar o contrato do `quality_report.json`.

- [ ] **Step 5: Verificar equivalência**

Run: `PYTHONPATH=src python3 scripts/audit_fase1.py data/raw/campeonato-brasileiro-full.csv > /tmp/audit_depois.txt && diff /tmp/audit_antes.txt /tmp/audit_depois.txt && PYTHONPATH=src python3 scripts/build_processed.py && PYTHONPATH=src python3 -m pytest tests/ -q && PYTHONPATH=src python3 scripts/check_monografia.py`
Expected: `diff` sem saída; `58 passed`; auditoria confere.

- [ ] **Step 6: Commit**

```bash
git add scripts/audit_fase1.py scripts/build_docx.py src/clean_data.py
git commit -m "refactor: decompoe funcoes longas e remove codigo morto"
```

---

### Task 9: Remover código morto restante e medir cobertura

**Files:**
- Modify: `scripts/make_figures.py:49` (`n = len(t)`), `:81` (`mkdir` com `parents=True`)
- Modify: `src/load_data.py:21` (`OPTIONAL_COLUMNS`)
- Modify: `tests/test_formatting.py:1`, `tests/test_integrity.py:2` (`Path` não usado)
- Modify: `requirements-dev.txt` (adicionar `pytest-cov`)
- Modify: `docs/qa_final.md` (registrar baseline de cobertura)

**Interfaces:**
- Consumes: suíte verde da Task 8.
- Produces: cobertura medida com baseline documentado (critério S7).

- [ ] **Step 1: Remover os itens mortos**

Apagar `n = len(t)` (`make_figures.py:49`), `OPTIONAL_COLUMNS` (`load_data.py:21`), os imports `from pathlib import Path` não usados nos dois testes. Trocar `FIG.mkdir(exist_ok=True)` por `FIG.mkdir(parents=True, exist_ok=True)`.

- [ ] **Step 2: Adicionar `pytest-cov`**

Acrescentar `pytest-cov` a `requirements-dev.txt`. Instalar no ambiente ativo.

- [ ] **Step 3: Medir cobertura**

Run: `PYTHONPATH=src python3 -m pytest tests/ -q --cov=src --cov-report=term-missing -m "not integration"`
Expected: relatório com percentual por módulo; registrar o número em `docs/qa_final.md` como baseline.

- [ ] **Step 4: Verificar e commitar**

Run: `PYTHONPATH=src python3 -m pytest tests/ -q && PYTHONPATH=src python3 scripts/check_monografia.py`
Expected: `58 passed` e auditoria confere.

```bash
git add scripts/make_figures.py src/load_data.py tests/test_formatting.py \
  tests/test_integrity.py requirements-dev.txt docs/qa_final.md
git commit -m "chore: remove codigo morto e estabelece baseline de cobertura"
```

---

### Task 10: Completar o CI

**Files:**
- Modify: `.github/workflows/ci.yml:17-52`

**Interfaces:**
- Consumes: tudo das tarefas anteriores.
- Produces: CI validando empacotamento, artefatos e cobertura (critério S6).

- [ ] **Step 1: Confirmar versões das actions**

Verificar se `actions/checkout@v7` e `actions/setup-python@v7` existem na forge. Se não existirem, fixar `@v4`.

- [ ] **Step 2: Adicionar etapas ao workflow**

Inserir após a instalação de dependências:

```yaml
      - name: Validar empacotamento
        run: |
          python3 -m pip install -e .
          python3 -c "import metrics, context, openfootball"

      - name: Smoke tests de artefatos
        run: |
          python3 scripts/bootstrap.py --check
          python3 scripts/make_figures.py
          python3 scripts/export_table1.py > /dev/null
          python3 scripts/build_docx.py
```

Manter `PYTHONPATH: src` (necessário para os imports no topo) e `permissions: contents: read`.

- [ ] **Step 3: Verificar localmente**

Run: `python3 -m pip install -e . && PYTHONPATH=src python3 scripts/bootstrap.py --check && PYTHONPATH=src python3 scripts/make_figures.py && PYTHONPATH=src python3 scripts/export_table1.py > /dev/null && PYTHONPATH=src python3 scripts/build_docx.py`
Expected: todas as etapas sem erro; `git status --short` sem novas mudanças indesejadas em arquivos tracked (figuras e PDFs são regenerados de forma determinística — conferir `git diff --stat`).

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: valida empacotamento e artefatos na cadeia"
```

---

## Self-Review

- [x] **Spec coverage:** G1→Task 2; G2→Tasks 3,4; G3→Task 1; G4→Tasks 6,7,8; G5→Tasks 9,10. Apêndice de bloqueios externos registrado como fora do escopo técnico.
- [x] **Step scan:** cada passo tem comando/resultado verificável; nenhum "handle edge cases" genérico.
- [x] **Type consistency:** `conferir(texto, df, tab1) -> list[str]`, `main(argv) -> int`, `excecao_conhecida(ano, so_base, so_of, placar_divergente) -> bool`, `parse_arquivo(path, temporada) -> DataFrame`, `travel_km(df) -> Series` — nomes idênticos em todos os usos.
- [x] **Review Focus:** 5 entradas listadas, cada uma com teste em tarefa nomeada (Tasks 2, 5, 7, 7, 6 respectivamente — ver tabela no topo).
- [x] **Proportion:** plano proporcional à spec; blocos de código aparecem só onde fixam testes ou CLI, não como transcrição de implementação.
