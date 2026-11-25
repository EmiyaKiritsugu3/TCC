# Vantagem de jogar em casa — Brasileirão Série A (2006–2024)

Dashboard interativo + pesquisa quantitativa descritiva (TCC, Sistemas de Informação).
Proposta completa em `spec_tcc_vantagem_casa_brasileirao.md`.

## Resultados principais (base validada, 7.219 partidas)

- Vitórias do mandante **49,0%** · empates **26,8%** · vitórias do visitante **24,1%**
- Gols/partida: casa **1,49** × fora **1,00** (diferença +0,49)
- **Pollard geral: 63,66%** → H1 (> 50%) confirmada no período
- Pollard anual varia de **58,2% (2017)** a **69,5% (2018)**, com **mudança de nível** pós-2018:
  **64,9%** em 2006–2018 vs. **61,0%** em 2019–2024 (diferença 3,9 p.p.; IC 95% 2,1–5,6)
- Contexto: não há associação relevante com a distância (63,4%–63,9%); clássicos sem viagem ficam em **58,2%**;
  estádio habitual **64,1%** vs. outro **59,4%**; mandante zebra ainda fica em **55,6%**
- Matriz de correlação por equipe-temporada: HA × casa **+0,57**, fora **−0,46**, distância **−0,01**,
  estádio habitual **+0,10**, pontos **+0,08**, posição **−0,08**

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
python3 -m pytest tests/ -q          # 117 testes (106 rápidos + 11 de integração)
python3 scripts/validate_cross.py    # validação OpenFootball 2018–2024
python3 scripts/build_deck.py        # gera o deck de defesa (PPTX)
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

Texto vigente em `docs/monografia_v2.md` (Tabelas 1–11, Figuras 1–13, apêndices A–D).
Antes de alterar qualquer número no texto, rode `python3 scripts/check_monografia.py`
— ele acumula as divergências entre texto, base e tabelas e falha (exit 1) ao final da auditoria.
O PDF final de depósito (`docs/monografia_final.pdf`) será adicionado quando existir.
Titularidade e proveniência em `NOTICE.md`.

## Dados externos (opcional)

A avaliação de público e arbitragem está em `docs/fontes_externas.md`,
`docs/analise_publico_arbitragem.md` e `docs/auditoria_dados.md`. Os scripts `fetch_basedosdados.py`,
`parse_fbref.py`, `join_external.py`, `build_external.py` e
`analyze_external.py` geram arquivos locais em `data/external/` (CSVs e JSON);
metadados e resumos derivados são versionados. Requerem `pip install -e .` ou
`PYTHONPATH=src`. A Base dos Dados exige um projeto de billing no BigQuery;
o FBref exige extração manual no navegador por causa do Cloudflare.

Cartões por partida (2013–2024), fonte MIT BrazilianFootball/Data. Requer a
base processada; a análise de faltas é opcional e depende do pipeline externo:

```bash
PYTHONPATH=src python3 scripts/fetch_raw.py
PYTHONPATH=src python3 scripts/build_processed.py
PYTHONPATH=src python3 scripts/fetch_cards.py
PYTHONPATH=src python3 scripts/build_cards.py
PYTHONPATH=src python3 scripts/analyze_cards.py
```

Relatório: `docs/analise_cartoes.md`; figura: `figuras/fig13_cartoes.png`.

### Recorte 2013–2024 (artigo, base MIT)

A versão do artigo usa a base aberta do `BrazilianFootball/Data` (MIT), com
resultados, gols, estádios e cartões de 2013–2024. Requer
`pip install -r requirements-dev.txt` (inclui `python-docx`), LibreOffice para
o PDF e Poppler (`pdfunite`, `pdfinfo`) para o pacote completo. A Figura 2 usa
`data/external/context_clean.csv`, gerado pelo pipeline externo descrito em
`docs/fontes_externas.md`.

```bash
PYTHONPATH=src python3 scripts/build_mit_base.py
PYTHONPATH=src python3 scripts/fetch_cards.py
PYTHONPATH=src python3 scripts/build_cards.py \
  --base data/processed/matches_processed_2013_2024.csv
PYTHONPATH=src python3 scripts/analyze_cards.py
PYTHONPATH=src python3 scripts/analyze_artigo.py
PYTHONPATH=src python3 scripts/analyze_models.py
PYTHONPATH=src python3 scripts/validate_champions.py \
  --base data/processed/matches_processed_2013_2024.csv
PYTHONPATH=src python3 scripts/build_artigo.py
TCC_PROCESSED=data/processed/matches_processed_2013_2024.csv \
TCC_QUALITY=data/processed/quality_report_2013_2024.json \
python3 -m streamlit run app.py
```

O dashboard continua usando a base 2006–2024 por padrão; as variáveis
`TCC_PROCESSED` e `TCC_QUALITY` selecionam o recorte sem alterar o código.

O artigo é escrito em inglês (2013–2024); `docs/artigo_2013_2024.md` é a fonte
editável e `build_artigo.py` gera `.docx` e `.pdf`. A versão em português usa
`docs/artigo_2013_2024_pt.md`:

```bash
PYTHONPATH=src python3 scripts/build_artigo.py        # inglês
PYTHONPATH=src python3 scripts/build_artigo.py --pt   # português
```

O resumo para o orientador fica em `docs/resumo_artigo_orientador.pdf`.
O guia de estudo para a banca fica em `docs/guia_estudo_banca.md` (e `.pdf`,
gerado por `scripts/build_guia_banca.py`).
A apresentação do artigo (10 slides) fica em
`apresentacao/apresentacao_artigo_2013_2024.pptx` e `.pdf`, gerada por
`scripts/build_deck_artigo.py`; as figuras de projeção vêm de
`scripts/make_deck_figures.py`. A versão de banca (11 slides), com literatura,
contribuições e limitações, fica em
`apresentacao/apresentacao_banca_2013_2024.pptx` e `.pdf`, gerada por
`scripts/build_deck_banca.py`. A versão de 5 minutos (6 slides) fica em
`apresentacao/apresentacao_5min_2013_2024.pptx` e `.pdf`, gerada por
`scripts/build_deck_5min.py`.

Versão ABNT (NBR 6022), com referências NBR 6023:

```bash
PYTHONPATH=src python3 scripts/build_artigo_abnt.py
```

Saídas: `docs/artigo_2013_2024_abnt.docx` e `.pdf`; a fonte editável é
`docs/artigo_2013_2024_abnt.md`.

Para gerar o pacote com capa, folha de rosto e folha de avaliação
(numeração do artigo começando em 4):

```bash
PYTHONPATH=src python3 scripts/build_artigo_abnt.py --inicio 4
PYTHONPATH=src python3 scripts/build_capa_artigo.py
```

Saídas: `docs/capa_folha_rosto_artigo.pdf`, `.docx` e
`docs/artigo_2013_2024_abnt_completo.pdf` (pré-textuais + artigo).

Depois do pipeline externo, a auditoria completa dos dados:

```bash
python3 scripts/audit_data.py
```

## Estrutura

- `app.py` — dashboard (5 abas, incluindo Contexto)
- `pyproject.toml` — empacotamento (`pip install -e .`) e configuração do pytest
- `src/load_data.py`, `src/clean_data.py`, `src/metrics.py`, `src/context.py`, `src/associations.py`, `src/charts.py`
- `scripts/bootstrap.py`, `scripts/build_processed.py`, `scripts/analyze_context.py`, `scripts/audit_data.py`, `scripts/check_monografia.py`, `scripts/build_deck.py`
- `tests/` — testes rápidos com fixtures em `tests/data/`; testes com o CSV real levam o marker `integration`
- `.github/workflows/ci.yml` — cadeia de validação (instalação, base, testes, validações, auditoria)
- `docs/auditoria_fase1.md`, `docs/data_dictionary.md`
