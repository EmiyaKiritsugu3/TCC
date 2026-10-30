# Relatório de Auditoria — Fase 1 (base bruta)

**Arquivo:** `data/raw/campeonato-brasileiro-full.csv`
**Fonte:** https://github.com/adaoduque/Brasileirao_Dataset — commit `15f027c` (2026-02-05), acesso em 2026-10-28
**Script:** `scripts/audit_fase1.py` (não altera nenhum arquivo; só lê)
**Licença:** repositório sem arquivo LICENSE — e-mail de autorização ao autor pendente. Não redistribuir o CSV.

## 1. Cobertura por temporada

Base total: 8.785 linhas (2003–2025). Recorte do TCC (2006–2024): **7.219 partidas** (esperado: 7.220).

| Temporada | Obs. | Esperado | Delta | Início – Fim |
|---|---:|---:|---:|---|
| 2006–2015 | 380 cada | 380 | 0 | ok |
| 2016 | 379 | 380 | −1 | 14/05/2016 – 11/12/2016 — ver §3.1 |
| 2017–2019 | 380 cada | 380 | 0 | ok |
| 2020 | 380 | 380 | 0 | 08/08/2020 – 25/02/2021 — ver §3.2 |
| 2021–2024 | 380 cada | 380 | 0 | ok |

Temporadas fora do recorte (referência de formato, sem exigência de 380): 2003: 552, 2004: 552, 2005: 462.

## 2. Qualidade (recorte 2006–2024, salvo indicação)

- Datas não interpretáveis (`%d/%m/%Y`): **0**
- Rodada nula: **0**; intervalo 1–38 em todas as temporadas do recorte
- Placar ausente: **0** (total e recorte); gols negativos: **0**; maior placar por lado: 7
- Linhas 100% duplicadas (com ou sem ID): **0**; IDs repetidos: **0**
- Triplas (data, mandante, visitante) repetidas: **0**; espelhadas no mesmo dia: **0**
- Mandante == visitante: **0**
- Campo `vencedor` × placar recalculado (7.219 avaliadas): **0 divergências**

## 3. Anomalias explicadas

### 3.1 2016 — falta Chapecoense × Atlético-MG (rodada 38)
Atlético-MG tem 37 jogos (342 em casa / 341 fora) e Chapecoense 37 (132 / 133) — falta exatamente o confronto da rodada 38, em que a Chapecoense seria mandante. É a partida de 11/12/2016 cancelada após a tragédia do voo da Chapecoense (W.O. duplo decretado em campo, sem efeito competitivo). **Decisão para a Fase 2:** manter a base com 379 partidas em 2016 e registrar o motivo; não inventar placar nem excluir nada adicionalmente.

### 3.2 2020/2021 — temporada 2020 terminou em 25/02/2021
A temporada 2020 soma 380 partidas, mas 112 têm data em 2021 (pandemia de COVID-19; jogos reagendados carregam a rodada **original** — ex.: Goiás × São Paulo, rodada 1, em 03/12/2020; Palmeiras × Vasco, rodada 1, em 26/01/2021). A segmentação por reinício de rodada falha aqui; a regra adotada (novo segmento = intervalo > 45 dias + rodada ≤ 5) separa corretamente 2020 (08/08/2020–25/02/2021) de 2021 (29/05/2021–09/12/2021), ambas com 380. **Decisão para a Fase 2:** atribuir temporada por intervalo de datas/rodada, nunca pelo ano civil isolado.

### 3.3 Cabeçalho × legenda
Coluna de rodada chama-se `rodata` (typo), não `Rodada`; coluna `Dia` da legenda não existe no CSV. Colunas de formação/técnicos vazias nas temporadas antigas — descartar no pipeline (fora do escopo).

## 4. Clubes (43 nomes no recorte)

Mandante e visitante balanceados em todos, exceto o par afetado por §3.1. Presença integral nas 19 temporadas (361 + 361): Flamengo, Fluminense, São Paulo. Caso de renomeação entre temporadas: **Barueri (2009) → Grêmio Prudente (2010)** — mesma franquia, nomes distintos por temporada; tratar como entidades separadas por temporada na comparação entre equipes, com nota na monografia. O par `Gremio` × `Gremio Prudente` apontado pelo script é falso positivo de substring (só coexistem em temporadas diferentes).

## 5. Pendências (fora da auditoria técnica)

1. **Licença:** enviar e-mail ao autor e anexar a resposta; sem isso, manter `data/raw/` fora de repositório público.
2. **Confronto CBF:** definir com o orientador a amostra mínima (sugestão: conferir integralmente 3 temporadas, incluindo 2016 e 2020, contra fonte oficial).
3. **Decisões da seção 23 da spec:** recorte, título, artefato, fonte e formato do curso.

## 6. Conclusão

Base **apta para a Fase 2** com as regras acima: filtro 2006–2024 por temporada (não por ano), 2016 com 379 partidas documentadas, descarte das colunas fora do esquema lógico da seção 8.1 da spec. Nenhuma exclusão ou correção silenciosa foi feita nesta fase.
