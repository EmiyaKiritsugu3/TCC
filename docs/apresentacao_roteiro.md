# Roteiro de apresentação e demonstração (10 min; deck de 14 slides)

## Slides

**Núcleo (≈ 9 min):**

1. **Capa** — título, autor, orientador.
2. **Problema** — magnitude da vantagem de jogar em casa na Série A 2006–2024.
3. **Método em uma figura** — fonte pinada → limpeza → métricas → dashboard →
   validação dupla; 2.659/2.660 e 19/19 campeões.
4. **Resultado geral** — `fig1_distribuicao_geral.png`; 49,0% / 63,7% / 1,49 × 1,00.
5. **Evolução (H2)** — `fig2_pollard_temporadas.png`; 58,2%–69,5%.
6. **Mudança de nível pós-2018** — `fig9_serie_ic.png`; 64,9% → 61,0%
   (IC 2,1–5,6); ponto de quebra 2019, com VAR e pandemia no mesmo período.
7. **Gols** — `fig4_gols_temporadas.png`; +0,49 gol/jogo.
8. **Contexto** — `fig10_contexto.png`; distância 63,4%–63,9%, clássico 58,2%,
   estádio 64,1% vs. 59,4%, zebra 55,6%.
9. **Público e arbitragem** — `fig12_publico_ha.png`; 6.618 registros, 177 árbitros,
   ρ público × HA = 0,04 e ρ público × pontos = 0,79; 2020 60,2% × 2022–2024 60,6%.
10. **Dois anos, duas notas de método** — 2016 (379 jogos) e 2020 (portões fechados).
11. **Limitações** — observacional; público é proxy; arbitragem só identidade;
   2008 parcial e 2024 completado pelo FBref; sem causalidade.
12. **Conclusão** — 63,7% em 19 temporadas; contribuição: série longa + pipeline
    reproduzível + dashboard.

**Backup (se a banca pedir):**

13. **Matriz de correlação** — `fig11_correlacoes_equipe.png`; +0,57/−0,46 são
    componentes mecânicos; distância −0,01, estádio +0,10, temporada −0,19.
14. **Anexo — resultados por temporada** — tabela completa no CSV + roteiro da demo.

## Tempo sugerido

| Bloco | Slides | Tempo |
|---|---|---:|
| Problema + método | 2–3 | 1,5 min |
| Resultados gerais e evolução | 4–6 | 3,0 min |
| Contexto e público/arbitragem | 8–9 | 2,0 min |
| Método, limitações e conclusão | 10–12 | 2,5 min |
| Perguntas / backup | 13–14 | restante |

## Demonstração ao vivo (3 min, ensaiar nesta ordem)

1. Abrir **Visão geral** com recorte total → ler os cartões.
2. Mudar filtro para **2020** → Pollard 60,2% (gancho para pandemia).
3. Aba **Equipes**: Flamengo 2019 (17V-2E-0D em casa) → tabela + download CSV.
4. Aba **Contexto**: alternar Clássico → Distância → Estádio; mostrar IC e ranking.
5. Aba **Contexto → Matriz**: alternar Equipe-temporada → Partida; destacar distância ~0.
6. Aba **Metodologia**: fonte, fórmula, relatório de qualidade e validação.

> A seção de público/arbitragem está na monografia (Tabelas 8–10, Figura 12);
> o dashboard atual não tem aba externa. Se a banca pedir, usar o slide 9 e o
> `docs/analise_publico_arbitragem.md`.

## Plano B (se a internet/demo falhar)

Figuras `figuras/*.png`, `figuras/tab1_indicadores_temporada.csv` e o PDF do deck
já estão exportados — a apresentação anda sem o app no ar.
