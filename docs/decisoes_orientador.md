# Decisões do orientador — TCC vantagem de jogar em casa

**Aluno:** José Inamar de Medeiros Júnior · **Curso:** Sistemas de Informação
**Última atualização:** 17/11/2026 (ampliação proativa, sem resposta do orientador ainda)

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

Pendência: validação do orientador para manter H3–H5 e a mudança de nível como
análise exploratória no depósito. Nada foi classificado como causal.
