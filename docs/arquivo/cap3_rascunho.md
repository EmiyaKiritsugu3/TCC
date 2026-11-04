# Rascunho — Capítulo 3. Metodologia (Sprint 7)

> Baseado integralmente no que foi executado. Sem números a inventar:
> todos vêm de `data/processed/quality_report.json`.

## 3.1 Classificação da pesquisa

Pesquisa aplicada (artefato de software), quantitativa, de objetivos exploratórios
e descritivos, por procedimentos documental e análise de dados secundários. Unidade
de análise: a partida, agregada por temporada e, secundariamente, por equipe.

## 3.2 Fonte e validação dos dados

Fonte primária: `Brasileirao_Dataset` (commit `15f027c`, acesso em 28/10/2026),
sem licença explícita — adotado o plano de não redistribuir o bruto (download
pinado no build; `.gitignore`; `data/raw/FONTE.md`). Auditoria inicial: 8.785
linhas, zero duplicatas, zero placares ausentes, zero divergências vencedor×placar.
Recorte 2006–2024: 7.219 partidas válidas, com dois casos documentados — 2016 com
379 jogos (Chapecoense×Atlético-MG cancelada) e temporada 2020 estendida até
25/02/2021 (atribuição por intervalo entre partidas, não por ano civil).
Validação cruzada independente contra o OpenFootball (domínio público, CC0) em
2018–2024: 2.659 de 2.660 partidas idênticas, zero divergências de placar; a única
exceção é de data e explicada (jogo de dois dias, 2023).

## 3.3 Critérios de inclusão e exclusão

Incluídas partidas da Série A, 2006–2024, com mandante, visitante e placar final
válido. Excluídos registros sem placar, com gols negativos, com mandante igual a
visitante e duplicatas — cada exclusão contabilizada em `quality_report.json`,
sem remoções silenciosas.

## 3.4 Indicadores

Resultado e pontos recalculados do placar (3/1/0); proporções, médias de gols e
índice de Pollard VC = Pm/(Pm+Pv)×100 (indefinido se Pm+Pv = 0). Mesma escala de
Pollard (1986) e Almeida et al. (2011), para comparabilidade com a literatura.
