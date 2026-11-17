# Especificação de design — Correção e otimização do TCC_00

**Data:** 2026-11-17
**Origem:** Auditoria técnica de 2026-11-17 (estado atual do projeto)
**Escopo aprovado:** Completo — críticos (C1–C3) + médios (M1–M8)
**Abordagem aprovada:** B — fases incrementais com gates de validação

---

## 1. Contexto e problema

A auditoria de 2026-11-17 confirmou que o núcleo técnico do projeto está saudável e
reproduzível: download pinado com SHA-256, 7.219 partidas processadas, 52 testes
passando, validação cruzada de 99,96% (2.659/2.660) e 19/19 campeões. Contudo,
a governança de entrega e a documentação estão desatualizadas:

1. **Divergência factual (C1):** a monografia afirma 31 testes, enquanto a suíte real
   tem 52 (48 rápidos + 4 de integração). O pior é que
   `scripts/check_monografia.py:53` exige literalmente as strings `"31 testes"` e
   `"31 passed"`, de modo que a auditoria numérica passa **validando um número
   errado** — um falso positivo que mascara a inconsistência.
2. **Estado não consolidado (C2):** cinco arquivos modificados não commitados e
   três grupos untracked no `working tree`; o estado auditável diverge do HEAD.
3. **Bloqueios externos (C3):** cinco decisões do orientador, indicação da banca,
   autorização do autor do dataset e template UFRN/ficha SISBI para o PDF final.
4. **Dívidas de qualidade (M1–M8):** auditoria sem `if __name__`, scripts sem
   testes, funções longas, código morto, CI sem empacotamento, docs stale,
   riscos não cobertos e ausência de medição de cobertura.

## 2. Objetivos

- G1. Fazer a auditoria numérica **detectar** um número desatualizado de testes,
  em vez de consagrá-lo.
- G2. Sincronizar todos os artefatos textuais (monografia, resumo, QA, comunicações,
  deck) com os números reais.
- G3. Consolidar o `working tree` num baseline auditável e versionado.
- G4. Elevar a robustez de scripts e da auditoria sem alterar resultados estatísticos.
- G5. Ampliar o CI para validar empacotamento e artefatos, com cobertura medida.

## 3. Não-objetivos

- Não redistribuir CSV bruto/processado nem alterar hashes ou regras de limpeza.
- Não introduzir alegações causais, previsão, IA ou apostas (spec §7).
- Não editar `docs/arquivo/` (material histórico).
- Não prometer resolver bloqueios que dependem de terceiros — apenas registrá-los
  e preparar as ações manuais.
- Não alterar os indicadores Validados: 7.219 partidas, 49,0/26,8/24,1%,
  1,49×1,00 gols, Pollard 63,66%, 99,96%, 19/19.

## 4. Critérios de sucesso

| ID | Critério | Verificação |
|---|---|---|
| S1 | Texto e auditoria concordam em 58 testes (54 rápidos + 4 integração) — número final após inclusão dos 5 testes de guarda/borda previstos nesta spec | `grep` + cadeia verde |
| S2 | Meta-teste prova que a auditoria falha se o número voltar a 31 | teste de guarda executado |
| S3 | Nenhum valor obsoleto (22, 31, 5.511) em docs vigentes | `grep` em `docs/` exceto `arquivo/` |
| S4 | `git status --short` sem modificações pendentes ao fim da Fase 0 | `git status` |
| S5 | Cadeia completa verde ao fim de cada fase | pytest, cross, champions, check_monografia |
| S6 | CI valida `pip install -e .` e executa smoke tests | workflow revisado + execução local |
| S7 | Cobertura medida com baseline documentado | relatório `pytest-cov` |

## 5. Design por fases

Cada fase termina com a cadeia de validação verde e um commit atômico. Se uma fase
falhar, o rollback é `git revert` do commit da fase — nunca `reset --hard`.

### Fase 0 — Consolidação do baseline
- Decidir o destino das mudanças pendentes: **commitar como baseline** (recomendado,
  pois `decisoes_orientador.md`, `resumo_orientador.md`, `monografia_v2.md`, `.docx`
  e `.pdf` já passaram nas validações) ou revertê-las.
- Remover ou ignorar `.omo/` (artefato de ferramenta, não do projeto).
- Declarar os dois e-mails preparados como versionados (são artefatos de entrega).
- **Gate:** `git status --short` limpo; cadeia verde.

### Fase 1 — Corrigir C1 com guarda anti-regressão
- Substituir 31→52 em `docs/monografia_v2.md:218,353,557,573`, Tabela 4
  (`:359-364`), `scripts/check_monografia.py:53`, `apresentacao/apresentacao_tcc.pptx`
  (slide 9) e regenrar `.docx`/`.pdf`.
- Detalhar a composição: 48 rápidos + 4 de integração (a Tabela 4 passa a listar
  os 12 arquivos de teste, não apenas 6).
- Criar meta-teste em `tests/test_check_monografia_guard.py`: copia a monografia para
  um diretório temporário, troca 52→31 e executa o auditor, esperando **falha**.
  O teste garante que o auditor não volte a validar número obsoleto.
- **Gate:** cadeia verde + meta-teste passando.

### Fase 2 — Sincronização documental
- `docs/qa_final.md`: 22→52 testes, 5.511→5.994 palavras, deck 22→52.
- `docs/comunicacoes_pendentes.md`: 22→52 testes.
- `docs/monografia_v2.md:8`: atualizar a nota que ainda cita `[TODO-BANCA]`,
  `[TODO-CBF]`, `[TODO-ORIENTADOR]` para `[PENDENTE - ORIENTADOR]`.
- `docs/resumo_orientador.md`: conferir consistência final.
- Atualizar `AGENTS.md:4` (commit de origem do knowledge base) e referências de
  versão em `docs/qa_final.md` / `docs/comunicacoes_pendentes.md`.
- **Gate:** `grep -R "22 testes\|31 testes\|31 passed\|5\.511" docs/ --exclude-dir=arquivo` sem resultados.

### Fase 3 — Robustez da auditoria e scripts
- `scripts/check_monografia.py`: mover corpo para `main()` com
  `if __name__ == "__main__"`; validar presença dos cabeçalhos antes dos `split()`
  (`:80`, `:149`) com mensagem de erro clara.
- `scripts/fetch_raw.py`: `argparse`, `except` estreito (evitar `BaseException`),
  timeout no download.
- `scripts/validate_cross.py`: extrair a regra de `KNOWN_DATE_EXCEPTIONS` para
   função testável; cobrir com teste unitário o caso de 1 exclusivo de cada lado.
- `src/openfootball.py:91-99`: inicializar `data_iso` e falhar com mensagem clara
  se uma linha de jogo preceder a data; teste de borda.
- `src/context.py:79-80`: validar clube presente em `CLUB_COORDS` com erro
  descritivo; teste de borda.
- **Gate:** 54+ testes passando (52 + novos testes de borda).

### Fase 4 — Qualidade de código
- Decompor `scripts/audit_fase1.main` (185 lin.), `scripts/build_docx.main` (121)
  e `src/clean_data.clean_matches` (103) em helpers menores, sem mudar comportamento.
- Remover código morto: `prev_r` (`clean_data.py:37,49`; `audit_fase1.py:78,89`),
  `def norm` (`audit_fase1.py:189`), `n = len(t)` (`make_figures.py:49`),
  `OPTIONAL_COLUMNS` (`load_data.py:21`), `winner_raw` (`clean_data.py:74`),
  `import re` duplicado (`build_docx.py:21,39`), `Path` não usado em dois testes.
- **Gate:** suite verde; diff revisado; nenhuma mudança de indicadores.

### Fase 5 — CI e cobertura
- Adicionar etapa `pip install -e .` ao `.github/workflows/ci.yml` e conferir
  disponibilidade de `actions/checkout@v7` / `actions/setup-python@v7`.
- Adicionar smoke tests: `bootstrap.py --check`, `make_figures.py`, `build_docx.py`,
  `export_table1.py` (em diretório temporário, sem poluir o repo).
- Adicionar `pytest-cov` a `requirements-dev.txt`; medir cobertura e registrar
  baseline em `docs/qa_final.md`.
- **Gate:** cadeia verde localmente com cobertura medida.

## 6. Estratégia de testes

- TDD para a Fase 1: escrever primeiro o meta-teste que exige falha do auditor com
  número obsoleto; só depois alterar monografia e auditor.
- Testes de borda para `openfootball` e `context` na Fase 3.
- Testes unitários para a regra de exceção de `validate_cross`.
- Nenhum teste deve depender de rede; integração continua marcada e verificada
  contra a base local gerada.

## 7. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Regenerar `.docx`/`.pdf` mude formatação | Comparar contagem de páginas e figuras antes/depois; manter rascunho identificado |
| Meta-teste seja frágil a mudança de texto | Basear-se na extração do número pelo próprio auditor, não em regex rígida de frase |
| Refatoração altere indicadores | Rodar `check_monografia.py` após cada fase; qualquer divergência reverte a fase |
| CI com actions v7 inexistente | Confirmar disponibilidade; se indisponível, fixar v4 |
| Bloqueios externos indefinidos | Registrados como apêndice, sem bloquear as fases técnicas |

## 8. Apêndice — ações manuais pendentes (fora do escopo técnico)

1. Enviar `docs/email_orientador_preparado.txt` (5 decisões + resumo + template).
2. Enviar `docs/email_autor_dataset_preparado.txt` (autorização escrita).
3. Obter indicação dos 2º e 3º membros da banca.
4. Obter template oficial UFRN/CERES-BSI, ficha catalográfica SISBI e folha de avaliação.
5. Gerar `docs/monografia_final.pdf` no template e registrar QA final.

Estas ações dependem de terceiros e não são pré-requisito para as fases 0–5.

---

## 9. Auto-revisão da spec

- [x] Sem placeholders TBD/TODO não intencionais
- [x] Consistência interna: escopo, fases e critérios de sucesso alinhados
- [x] Escopo focado num único plano de implementação
- [x] Ambiguidades resolvidas: destino do working tree, composição de 52 testes,
      tratamento dos bloqueios externos
