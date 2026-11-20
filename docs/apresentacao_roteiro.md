# Roteiro de apresentação e demonstração (10 min; Sprint 6)

## Slides (10 slides, conforme o deck em `apresentacao/apresentacao_tcc.pptx`)

1. **Problema** — qual a magnitude da vantagem de jogar em casa no Brasileirão 2006–2024?
2. **Método em 1 figura** — pipeline: fonte → limpeza → métricas → dashboard
   (cite auditoria + validação cruzada 99,96% — é o slide que blinda a banca).
3. **Resultado geral** — `fig1_distribuicao_geral.png` (Figura 5) + Pollard 63,7% (H1).
4. **Evolução** — `fig2_pollard_temporadas.png` (Figura 7) (58,2%–69,5%; H2) + `fig9_serie_ic.png` (Figura 9): mudança de nível pós-2018 (64,9% → 61,0%; IC 2,1–5,6); destaque 2017 × 2018 com cautela sobre ICs.
5. **Gols** — `fig4_gols_temporadas.png` (Figura 6) (1,49 × 1,00).
6. **Contexto (slide extra, se houver tempo)** — `fig10_contexto.png` (Figura 10): viagem não é o principal; clássico 58,2%; estádio habitual 64,1% vs. 59,4%; zebra 55,6%.
7. **Casos metodológicos** — 2016 (379 jogos) e 2020 (pandemia/VAR) em 2 bullets; 2020 não é o piso (2017 é menor).
8. **Limitações** — 3 bullets da spec §19 (sem causalidade; sem torcida/arbitragem/elenco; contexto por proxies).
9. **Conclusão** — resposta em 1 frase + contribuição (série longa + sistema reproduzível + decomposição descritiva).

## Demonstração ao vivo (3 min, ensaiar nesta ordem)

1. Abrir aba Visão geral com recorte total → ler os 7 cartões.
2. Mudar filtro para 2020 → mostrar Pollard 60,2% (gancho para falar da pandemia).
3. Aba Equipes: Flamengo 2019 (17V-2E-0D em casa) → mostrar tabela + download CSV.
4. Aba Contexto: alternar Clássico → Distância → Estádio; mostrar IC e ranking por equipe.
5. Aba Metodologia: apontar fonte, fórmula e relatório de qualidade.

## Plano B (se a internet/demo falhar)

Figuras `figuras/*.png` + `tab1_indicadores_temporada.csv` já exportados —
a apresentação anda sem o app no ar.
