# Resumo executivo para o orientador — TCC vantagem de jogar em casa

**Aluno:** José Inamar de Medeiros Júnior · **Curso:** Sistemas de Informação · **Data:** 20/11/2026
**Título proposto:** *Análise estatística da vantagem de jogar em casa no Campeonato
Brasileiro Série A: desenvolvimento de um dashboard interativo para análise de
resultados históricos* (alternativo curto na spec, §2).

## 1. O que é

Pesquisa quantitativa aplicada + software: dashboard interativo (Streamlit) sobre
7.219 partidas da Série A 2006–2024, com proporções de resultados, médias de gols
e índice de Pollard por temporada e por equipe. Sem previsão, sem IA, sem apostas.

## 2. Status (software pronto, dados validados)

- Base primária auditada: **7.219 partidas**, 19 temporadas, zero duplicatas, zero
  placares ausentes, zero divergências vencedor×placar; 2016 com 379 jogos
  (Chapecoense×Atlético-MG cancelada) e 2020 estendida até 25/02/2021.
- Pipeline reproduzível + **114 testes automatizados** passando (105 rápidos + 9 de integração).
- **Monografia v3 atualizada** (20/11/2026): Tabelas 1–11, Figuras 1–13, §5.6 de
  público/arbitragem e §5.7 de cartões; auditor numérico confere todos os números citados.
- **Auditoria de dados:** 150 verificações, 0 falhas (`docs/auditoria_dados.md`);
  SHA-256 do bruto, reconstrução byte a byte, unicidade e cobertura conferidos.
- **Validação cruzada:** OpenFootball (CC0) em 2018–2024 → **2.659/2.660**
  partidas idênticas, zero divergências de placar; **19/19 campeões** recalculados.
- Fonte sem licença explícita → plano B: CSV bruto não versionado, download
  pinado + SHA-256 (ver `data/raw/FONTE.md`).
- **Contexto (v3):** viagem, clássico, estádio, descanso, força, era e pandemia
  (Tabelas 5–7; Figuras 10–11), com ICs e leitura descritiva.
- **Base externa (v3):** 6.618 registros de público (91,7%) e 6.821 jogos com
  árbitro (94,5%); 177 árbitros após normalização de nomes; 2024 completado pelo
  FBref (376 com público, 362 com árbitro). 2008 tem cobertura parcial; 2020–2021
  têm zeros reais de portões fechados.
- **Cartões (incorporados na §5.7):** 4.559 partidas de 2013–2024
  (BrazilianFootball/Data, MIT), com 1 cartão não atribuído. Em 2019 o mandante
  recebia 0,18 amarelo a menos; em 2020, +0,11; a mudança com efeitos fixos de
  equipe é +0,35 (IC 95% −0,03 a +0,72, com erros-padrão conservadores: máximo
  entre clusters de mandante e visitante; inclui zero). O padrão é sugestivo do
  canal da arbitragem, mas não conclusivo.
- **PR #2 mergeada** na `main`; repositório limpo e CI verde.

## 3. Resultados

- Mandante venceu **49,0%**, empates 26,8%, visitante 24,1%; gols 1,49 vs. 1,00.
- **Pollard geral: 63,7%** → H1 (> 50%) confirmada no período.
- Pollard anual **58,2% (2017) – 69,5% (2018)** → H2 sustentada, com mudança de
  nível pós-2018: **64,9% → 61,0%** (diferença 3,9 p.p.; IC 2,1–5,6); ponto de
  quebra em 2019.
- Contexto: distância não move o índice (63,4%–63,9%); clássicos sem viagem ficam
  em 58,2%; estádio habitual 64,1% vs. 59,4%; mandante zebra ainda 55,6%.
- **Matriz de correlação (Spearman):** por equipe-temporada (n=380), HA × casa
  +0,57 e HA × fora −0,46 (componentes mecânicos), distância −0,01, estádio +0,10,
  temporada −0,19, pontos +0,08 e posição −0,08. No nível de partida (n=7.219), a
  maior associação é a diferença de posição (+0,19); as demais ficam entre −0,05
  e +0,03.
- **Público:** público médio × HA = 0,068 (sem 2020–2021: −0,010); público × pontos
  = 0,461. Os pontos sobem de 43,1 (Q1) para 59,4 (Q4), enquanto o HA fica entre
  0,657 e 0,815, sem tendência. Em 2020, sem torcida, Pollard 60,2%; em 2022–2024,
  com público de volta, 60,6% — o retorno não restaurou o patamar pré-2019.
- **Arbitragem:** 6.821 jogos, 177 árbitros, mediana de 14 jogos, máximo de 284;
  vitória do mandante 48,9%; entre os 50 árbitros com 40+ jogos, faixa de
  40,8%–67,4%, com apenas 1 fora de ±2 DP (esperado: 2,3). A base identifica
  **quem apitou**; a §5.7 acrescenta cartões (2013–2024), mas pênaltis e decisões
  discricionárias seguem fora do alcance.

Tudo descritivo, sem leitura causal, pendente de validação do orientador.

## 4. Decisões solicitadas (spec §23)

1. Aprovar recorte 2006–2024 e título.
2. Aceitar dashboard + pesquisa quantitativa como artefato de SI.
3. Confirmar fonte e plano B de licença.
4. **Validar a análise exploratória de tendência/mudança de nível, as associações
   contextuais (H3–H5), a seção 5.6 de público/arbitragem e a seção 5.7 de cartões**
   — o texto já as apresenta como descritivas; falta o aval do orientador para
   mantê-las no depósito.
5. Formato exigido de projeto/TCC e avaliação do software.

## 5. Riscos assumidos e mitigação

- Escopo fechado (§7 da spec): fora previsão, IA, apostas e Séries B–D.
- Análise observacional, sem alegação causal; público é proxy (não medida exata de
  torcida) e a arbitragem é conhecida pela identidade e, em 2013–2024, pelos cartões.
- 2006 tem 4 divergências de mando/placar entre a base primária e a Base dos Dados;
  como 2006 não tem público/árbitro, não afetam a análise externa.
- 2008 tem cobertura parcial de público (163/380); excluir 2008 não muda a conclusão
  (ρ HA = −0,009; pontos = 0,777).
- 2024 combina 286 jogos da Base dos Dados e 90 do FBref; os 90 preenchidos têm
  média ~6% maior, então a média de 2024 é mais incerta.

## 6. Pronto para envio

- `docs/monografia_v2.md` — texto vigente (v3).
- `docs/monografia_draft_abnt.docx` e `.pdf` — rascunho formatado (NBR 14724:2024).
- `apresentacao/apresentacao_tcc.pptx` e `.pdf` — **16 slides** (inclui mudança de
  nível, contexto, matriz, público/arbitragem, cartões e anexo).
- `docs/resumo_orientador.md` — este resumo.
- `docs/auditoria_dados.md` — auditoria de dados (150 verificações).
- Repositório `main` com CI verde e PR #2 mergeada.

Pendências externas: 5 decisões do orientador; autorização escrita do autor do
dataset; template oficial UFRN/CERES-BSI + ficha SISBI + folha de avaliação;
indicação da banca.
