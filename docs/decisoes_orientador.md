# Decisões do orientador — TCC vantagem de jogar em casa

**Aluno:** José Inamar de Medeiros Júnior · **Curso:** Sistemas de Informação
**Última atualização:** 20/11/2026 (auditoria de dados e seção 5.6; sem resposta do orientador ainda)

> Em 04/11/2026 o orientador ainda não havia respondido às 5 pendências. Por
> decisão do autor, a monografia foi ampliada proativamente à meta de 5.500
> palavras do corpo (ver Task 7 do plano de correção), sem alterar nenhum
> resultado validado. Quando as respostas chegarem, esta tabela será preenchida
> e o texto ajustado no que for determinado.

| # | Decisão | Resposta | Data | Impacto |
|---|---|---|---|---|
| 1 | Recorte 2006–2024 e título | pendente | — | escopo e capa |
| 2 | Dashboard como artefato de SI | pendente | — | cap. 4 e defesa |
| 3 | Fonte e plano B de licença | pendente | — | §3.2 e repositório |
| 4 | Spearman/tendência | pendente (texto mantém só descritivo) | — | §5.2 e cap. 6 |
| 5 | Formato do curso e avaliação do software | pendente | — | conversão ao template |

Ampliação aplicada em 04/11/2026 (proativa): §§1.2, 1.5, 2.1, 2.2, 2.3, 3.1–3.4,
4.1–4.4, 5.3 e 6 expandidas; Tabelas 2 (literatura), 3 (rastreabilidade RF) e 4
(síntese dos testes) criadas; corpo ≥ 5.500 palavras.

Fase 1 (variáveis contextuais) implementada em 06/11/2026 por decisão do
aluno, pendente de validação do orientador: `src/context.py` + 20 testes,
achado principal de que a distância não move o índice (Tabela 5 da monografia).

## Edição normativa adotada (05/11/2026)

Por decisão do autor, a formatação segue as edições **vigentes** (não as
contemporâneas à Resolução 001/2016-CSI): **NBR 14724:2024** (4ª ed.,
apresentação), **NBR 6023:2018** (referências), **NBR 10520:2023** (citações)
e **NBR 6028:2021** (resumo). A 14724:2024 revogou a de 2011; as bibliotecas
universitárias (incl. SISBI/UFRN) trabalham com a edição vigente.

Delta aplicado da 2024: crédito de figura/tabela própria como
"Fonte: Elaboração própria" (antes "Fonte: elaborado pelo autor").
Rascunho gerado em `docs/monografia_draft_abnt.docx` (+ PDF) via
`scripts/build_docx.py`: A4, margens 3/2, Times 12, 1,5, justificado.
Placeholders mantidos: ficha catalográfica (SISBI), folha de avaliação
assinada, numeração do sumário (passe final no template do curso).

## Bloqueios externos (04/11/2026, QA final)

- **PDF da monografia (`docs/monografia_final.pdf`):** depende do template
  oficial do curso (UFRN/CERES-BSI, Resolução 001/2016-CSI). Nenhum modelo
  `.dotx`/`.ott` foi localizado no repositório; a conversão Markdown → DOCX
  sem o template arriscaria margens, capa e paginação fora da norma. Texto
  vigente e fechado em `docs/monografia_v2.md`; gerar o DOCX/PDF final quando
  o modelo for fornecido.
- **Respostas do orientador (decisões 1–5):** ainda pendentes; texto mantém
  apenas o descritivo (sem Spearman) e as tags `[TODO-BANCA/SIGLAS/CBF/ORIENTADOR]`.


## Atualização 2026-11-12 22:33:33 — Sprint 1 (mass-ulw)

**Comunicações preparadas/enviadas (tentativa):**
- E-mail ao orientador (5 decisões + resumo + pedido de template): preparado em `docs/email_orientador_preparado.txt`. Tentativa via `mail` falhou (sem SMTP configurado) — precisa ser enviado manualmente.
- E-mail ao autor do dataset (adaoduquesn@gmail.com, autorização escrita): preparado em `docs/email_autor_dataset_preparado.txt`. Tentativa via `mail` falhou — precisa ser enviado manualmente.

**Evidências:** rascunhos em `docs/comunicacoes_pendentes.md`, notepad `/tmp/ulw-20261112-223203-09c557.md`.

## Bloqueadores remanescentes (Sprint 3)

**Externos (aguardam resposta):**
1. **5 decisões do orientador** (recorte/título, artefato SI, fonte+licença, Spearman, formato/avaliação) — e-mails preparados em `docs/email_orientador_preparado.txt` (envio manual necessário).
2. **Autorização escrita do autor do dataset** (adaoduquesn@gmail.com) — email preparado em `docs/email_autor_dataset_preparado.txt` (envio manual necessário).
3. **Template oficial UFRN/CERES-BSI + ficha catalográfica SISBI + folha de avaliação** — necessário para gerar `docs/monografia_final.pdf` (atualmente só existe `monografia_draft_abnt.pdf`).

**Internos (podem ser resolvidos):**
- Membros da banca ([PENDENTE - ORIENTADOR]) — aguardar indicação.
- Confronto CBF por amostra ([PENDENTE - ORIENTADOR]) — só se exigido.
- Revisão Resumo/Abstract após decisões — depende das respostas.

**Pronto para envio ao orientador agora:** `docs/monografia_v2.md`, `docs/resumo_orientador.md`, `docs/monografia_draft_abnt.pdf/.docx`, `apresentacao/apresentacao_tcc.pdf`, repositório em `main` com validações OK.


## Status final — Sprint 4 (mass-ulw) — 2026-11-12 22:35:54 (snapshot histórico)

**Validações executadas:**
- `pytest tests/ -q` (PYTHONPATH=src): **52 passed** ✓
- `scripts/validate_cross.py`: **PASS — 2.659/2.660 idênticas, zero divergências de placar** (1 exceção conhecida) ✓
- `scripts/validate_champions.py`: **PASS — 19/19 campeões** ✓
- `scripts/check_monografia.py` (PYTHONPATH=src): **AUDITORIA NUMÉRICA: tudo confere** ✓

**Artefatos prontos para envio:**
- `docs/monografia_v2.md` (5994 palavras corpo, figuras [1..8], tabelas atualizadas)
- `docs/monografia_draft_abnt.pdf` (38 páginas, regenerado) / `docs/monografia_draft_abnt.docx`
- `docs/resumo_orientador.md` (atualizado: 52 testes, variáveis contextuais)
- `apresentacao/apresentacao_tcc.pdf`
- Repositório `main` com histórico limpo

**Checklist para envio ao orientador:**
- [x] Base validada e reproduzível
- [x] Monografia auditada numericamente
- [x] Dashboard funcional (Streamlit)
- [x] Testes e validações passando
- [x] E-mails preparados (orientador + autor dataset) — envio manual pendente (sem SMTP)
- [ ] Respostas às 5 decisões
- [ ] Template oficial + ficha SISBI + folha de avaliação
- [ ] Autorização escrita do autor do dataset (se necessário manter base processada)
- [ ] `docs/monografia_final.pdf` gerado no template

## Atualização 2026-11-19 — análise de contexto (caminho B)

Implementado por decisão do autor, sem novas fontes de dados e sem alterar os
números validados da versão 2:

- `src/context.py`: mesma UF, região, clássico, estádio habitual, faixas de
  descanso e de posição, além do frame contextual único.
- `src/associations.py`: bootstrap de Pollard, IC anual, diferença por cluster
  de temporada, ponto de quebra, grupos, vantagem por equipe e split-half.
- `scripts/analyze_context.py`: gera `figuras/tab5_contexto.csv`,
  `figuras/tab6_equipes.csv` e `figuras/contexto.json`.
- Dashboard: quinta aba **Contexto** (RF12), com filtros, IC, ranking por equipe
  e matriz de correlação (equipe-temporada/partida).
- Monografia v3: §5.4–5.5, Tabelas 5–7, Figuras 9–11, ICs na Tabela 1, resumo,
  conclusão e limitações atualizados.
- **104 testes** (95 rápidos + 9 de integração); auditor numérico cobre os novos
  números.

Atualização 20/11/2026: **117 testes** (106 rápidos + 11 de integração); a seção
5.7, a Tabela 11 e a Figura 13 incorporam a extensão de cartões (2013–2024).

Pendência: validação do orientador para manter H3–H5 e a mudança de nível como
análise exploratória no depósito. Nada foi classificado como causal.


## Atualização 2026-11-20 — auditoria de dados e seção 5.6 (histórico)

- **PR #2 mergeada** na `main`; branch `feat/contexto-vantagem-casa` removida.
- **Monografia v3:** Tabelas 1–10, Figuras 1–12, com a seção 5.6 de público e
  arbitragem (6.618 registros de público, 6.821 jogos com árbitro, 177 árbitros
  após normalização de nomes).
- **Auditoria de dados:** 150 verificações, 0 falhas (`docs/auditoria_dados.md`);
  SHA-256 do bruto, reconstrução byte a byte, junção 7.121/7.219, validação
  2.659/2.660 e 19/19 campeões.
- **Deck:** 14 slides (`apresentacao/apresentacao_tcc.pptx/.pdf`), com mudança de
  nível, contexto, matriz, público/arbitragem e anexo.
- **Resumo do orientador** atualizado em `docs/resumo_orientador.md`.

Pendências externas seguem: 5 decisões, autorização escrita do autor do dataset,
template oficial UFRN/CERES-BSI + ficha SISBI + folha de avaliação e banca.

## Atualização 2026-11-20 — cartões (§5.7)

- **Monografia v3 atualizada:** Tabelas 1–11, Figuras 1–13; a seção 5.7 de
  cartões (4.559 partidas de 2013–2024, 1 cartão não atribuído) usa DiD 2019→2020
  com efeitos fixos de equipe e IC conservador (+0,35; IC 95% −0,03 a +0,72).
- **Deck:** 16 slides, com dois slides de cartões.
- **Testes:** 117 (106 rápidos + 11 de integração); auditor numérico cobre a
  Tabela 11 e a Figura 13.
- **PR #4** com o pipeline de cartões e a versão atualizada do texto/deck.

## Atualização 2026-11-21 — artigo final 2013–2024 (PR #5)

O trabalho foi fechado como **artigo** no recorte **2013–2024**, com a base
aberta `BrazilianFootball/Data` (MIT). A PR #5 foi mergeada na `main`
(commit `6c34577`) e a branch `feat/artigo-2013-2024` removida.

**Pacote final:**

| Arquivo | Conteúdo | Páginas |
|---|---|---:|
| `docs/artigo_2013_2024.pdf` | artigo em inglês | 9 |
| `docs/artigo_2013_2024_pt.pdf` | artigo em português | 10 |
| `docs/artigo_2013_2024_abnt.pdf` | artigo em ABNT (NBR 6022/6023) | 16 |
| `docs/artigo_2013_2024_abnt_completo.pdf` | capa + folha de rosto + avaliação + artigo | 19 |
| `docs/resumo_artigo_orientador.pdf` | resumo para o orientador | 2 |

**Resultados principais:** Pollard 63,0% (IC 95% 61,7–64,3); queda de 65,0%
(2013–2018) para 61,0% (2019–2024), diferença de 4,0 p.p. (IC 0,9–6,6), quebra
em 2019; Poisson com multiplicador de gols do mandante −12,0% (1,565 → 1,377)
e prêmio de +56,5% para +37,7%; ICC 2,2% entre equipes; público ρ = 0,08 com a
vantagem e 0,41 com pontos; cartões +0,35 (IC −0,03 a +0,72); pênaltis
convertidos +0,05 (IC −0,06 a +0,15), piloto 2019–2020.

**Decisões pendentes para o artigo (substituem a tabela de 2006–2024):**

| # | Decisão | Resposta | Data | Impacto |
|---|---|---|---|---|
| 1 | Confirmar formato artigo e recorte 2013–2024 | pendente | — | entrega final |
| 2 | Template oficial UFRN/CERES-BSI e ficha SISBI | pendente | — | capa, paginação e ficha |
| 3 | Nomes, titulação, instituição, data e nota da banca | pendente | — | folha de avaliação |
| 4 | Manter seções de público e cartões ou só o núcleo | pendente | — | extensão do artigo |
| 5 | Dashboard como artefato complementar ou link | pendente | — | avaliação e repositório |

A tabela original de 2006–2024 e as seções 5.6/5.7 da monografia permanecem
como registro histórico. O artigo 2013–2024 não depende da autorização do
`Brasileirao_Dataset`, pois usa a base MIT; o pedido ao autor da base antiga só
é necessário se a monografia histórica continuar publicada.
