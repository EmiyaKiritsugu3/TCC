# Roteiro de apresentação e demonstração (11 min; deck de 16 slides)

## Slides

**Núcleo (≈ 10 min):**

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
10. **Cartões — série** — `fig13_cartoes.png`; 4.559 partidas (2013–2024);
    −0,18 em 2019, +0,11 em 2020.
11. **Cartões — limite** — +0,35 com efeitos fixos, IC 95% −0,03 a +0,72;
    inclui zero; 2020 confunde pandemia, calendário e protocolos.
12. **Dois anos, duas notas de método** — 2016 (379 jogos) e 2020 (portões fechados).
13. **Limitações** — observacional; público é proxy; cartões não são decisões;
    2008 parcial e 2024 completado pelo FBref; sem causalidade.
14. **Conclusão** — 63,7% em 19 temporadas; contribuição: série longa + pipeline
    reproduzível + dashboard + extensão de cartões.

**Backup (se a banca pedir):**

15. **Matriz de correlação** — `fig11_correlacoes_equipe.png`; +0,57/−0,46 são
    componentes mecânicos; distância −0,01, estádio +0,10, temporada −0,19.
16. **Anexo — resultados por temporada** — tabela completa no CSV + roteiro da demo.

## Tempo sugerido

| Bloco | Slides | Tempo |
|---|---|---:|
| Problema + método | 2–3 | 1,5 min |
| Resultados gerais, evolução e contexto | 4–8 | 3,0 min |
| Público e cartões | 9–11 | 2,5 min |
| Método, limitações e conclusão | 12–14 | 2,5 min |
| Perguntas / backup | 15–16 | restante |

## Demonstração ao vivo (3 min, ensaiar nesta ordem)

1. Abrir **Visão geral** com recorte total → ler os cartões.
2. Mudar filtro para **2020** → Pollard 60,2% (gancho para pandemia).
3. Aba **Equipes**: Flamengo 2019 (17V-2E-0D em casa) → tabela + download CSV.
4. Aba **Contexto**: alternar Clássico → Distância → Estádio; mostrar IC e ranking.
5. Aba **Contexto → Matriz**: alternar Equipe-temporada → Partida; destacar distância ~0.
6. Aba **Metodologia**: fonte, fórmula, relatório de qualidade e validação.

> Público/arbitragem estão na monografia (Tabelas 8–10, Figura 12); cartões estão
> na seção 5.7, Tabela 11 e Figura 13. O dashboard atual não tem aba externa.
> Se a banca pedir, usar os slides 9–11 e os relatórios em `docs/`.

## Plano B (se a internet/demo falhar)

Figuras `figuras/*.png`, `figuras/tab1_indicadores_temporada.csv` e o PDF do deck
já estão exportados — a apresentação anda sem o app no ar.
