# Fichamentos — revisão bibliográfica (Sprint 4)

**Atenção metodológica:** fichas 2, 4 e 5 a partir de acesso aberto (ficha 3 por
resumo integral + metadados CC BY). A ficha 1 (original paywall) é citada via
*apud* Almeida et al. 2011, com âncora legível na ficha 2. Nada depende do CAPES.

## 1. Pollard, R. (1986). Home advantage in soccer: a retrospective analysis.

*Journal of Sports Sciences*, 4(3), 237–248. DOI: 10.1080/02640418608732122
[ORIGINAL PAYWALL — citar via *apud*: POLLARD, 1986 *apud* ALMEIDA et al., 2011.
Não fingir leitura do original.]

- **Objetivo:** quantificar retrospectivamente a vantagem de jogar em casa no futebol.
- **Método (o que o TCC adota):** aproveitamento percentual de pontos do mandante,
  incluindo empates; em competição equilibrada (ida e volta), > 50% = evidência
  de VC. É a definição operacional H1 do TCC (spec §6, §10.3-H).
- **Âncora legível:** o método está documentado no texto integral de
  Matos, Amaro & Pollard (2020), acesso aberto (ver ficha 2).

## 2. Matos, R. M.; Amaro, N.; Pollard, R. (2020). [ACESSO ABERTO]

How best to quantify home advantage in team sports. *RICYDE*, 16(59), 12–23.
DOI: 10.5232/ricyde2020.05902. PDF livre:
https://dialnet.unirioja.es/descarga/articulo/7325430.pdf

- **Objetivo:** comparar métodos de quantificar a VC (inclui o método percentual
  de Pollard reescalado e o de Stefani), em ligas de handebol de Portugal e Espanha.
- **Conexão:** referência metodológica efetivamente lida que descreve o método de
  Pollard — elimina a dependência do PDF paywall. Usar junto do *apud* da ficha 1.

## 3. Silva, C. D.; Moreira, D. G. (2008). A vantagem em casa no futebol.

*Rev. Bras. Cineantropometria e Desempenho Humano*, 10(2), 184–188.
DOI: 10.1590/1980-0037.2008v10n2p184. CC BY 4.0 (UFSC/OJS).
[FICHA POR RESUMO INTEGRAL + METADADOS — resumo lido em 28/10/2026;
texto integral em acesso aberto no mesmo endereço.]

- **Objetivo:** levantar a VC da Série A pelo % de pontos em casa e comparar com
  as principais ligas do mundo em 2002/03–2006/07.
- **Resultado:** Brasil **64,9 ± 2,2%**, significantemente maior (p < 0,05) que
  Alemanha, Argentina, Espanha, Inglaterra, Itália e Portugal; só a França não
  diferiu (p = 0,050). Fatores discutidos: território, clima, calendário, torcida.
- **Conexão:** primeiro benchmark Brasil × mundo e âncora numérica do TCC —
  nosso 63,7% (2006–2024) cai dentro da mesma ordem de grandeza, o que reforça
  consistência histórica. O TCC estende a série e empacota a análise em sistema
  reproduzível.

## 4. Almeida, L. G.; Oliveira, M. L.; Silva, C. D. (2011). [TEXTO INTEGRAL LIDO]

*RBEFE*, 25(1), 49–54. DOI: 10.1590/S1807-55092011000100006. CC BY-NC 4.0.

- **Objetivo:** comparar a VC das Séries A e B, 2003–2009 (n = 5.497 partidas).
- **Método:** Pollard (% pontos em casa); t pareado + effect size; fonte: soccerway.com.
- **Resultado:** Série B (69 ± 2,3%) > Série A (65 ± 2,3%), p < 0,05, η² = 0,57 (grande).
- **Discussão útil ao TCC:** distâncias/viagens maiores na B; familiaridade com campo;
  mandos alterados por punição/dinheiro; usaram o mandante **nominal da CBF**
  (primeiro clube do confronto) — mesma convenção adotada no TCC.
- **Conexão:** benchmark direto; o TCC cobre 2006–2024 só na A, com granularidade
  anual em vez de média do período.

## 5. Ribeiro, L. C. et al. (2022). [TEXTO INTEGRAL LIDO]

*J. Hum. Kinetics*, 81, 251–258. DOI: 10.2478/hukin-2022-0047. PMC8884879.

- **Objetivo:** efeito da ausência de torcida (COVID) na VC das Séries A e B, 2018–2020
  (n = 2.280; dados do site da CBF).
- **Resultado:** Série A caiu em 2019 e 2020 vs 2018; Série B estável. Confundidor
  importante: **VAR estreou na Série A em 2019** (menos viés pró-casa) — não dá para
  atribuir a queda só à torcida. 2020 ainda teve calendário comprimido e 5 substituições.
- **ALERTA DE ESCALA:** usam HA = ((H−A)/A)×100% (ex.: 128% em 2018-A), **não** Pollard.
  Não comparar esses números com os do TCC sem conversão.
- **Conexão:** explica nosso 2020 (Pollard 60,2%, abaixo da média): torcida ausente +
  VAR + calendário atípico. Reforça declarar 2020 como temporada anômala na discussão.

## 6. Sharda, R.; Delen, D.; Turban, E. (2019). [CONTEÚDO VERIFICADO NO PDF]

*Business intelligence e análise de dados para gestão do negócio*. 4. ed.
Cap. 2 (especialmente §§2.8, 2.9 e 2.11) e Cap. 3.

- **BI = análise descritiva:** "a análise de negócios descritiva (isto é, BI) é o
  nível de entrada na taxonomia", respondendo "O que aconteceu?" (Cap. 3) —
  legitima o escopo exclusivamente descritivo do TCC em vez de preditivo.
- **Visualização:** "o uso de representações visuais para explorar, dar sentido
  e comunicar dados" (§2.8, citando Few, 2007); o retratado são informações
  (dados agregados e contextualizados), não fatos brutos.
- **Gráficos (§2.9):** linhas para séries temporais/tendências; barras para
  comparar categorias (podendo ser empilhadas); pizza só para poucas categorias.
- **Dashboards (§2.11):** informações consolidadas numa única tela, digeríveis
  "num simples relance", com KPIs e aprofundamento por drill-down — exatamente
  a arquitetura do `app.py` (cartões → séries → tabela). Há até caso esportivo
  (Dallas Cowboys com Tableau, Caso 2.7).
- **Conexão:** Cap. 2.3 e justificativa das telas/gráficos no Cap. 4.

## 7. Few, S. (2006). [CONTEÚDO VERIFICADO NO PDF]

*Information dashboard design: the effective visual communication of data.*
Sebastopol: O'Reilly Media. Cap. 1 (§1.3.1), Cap. 3 e Cap. 5 (§5.1).

- **Definição (§1.3.1):** "visual display of the most important information needed
  to achieve one or more objectives; consolidated and arranged on a single screen
  so the information can be monitored at a glance" — o `app.py` segue à risca:
  tela única por aba, cartões + séries + tabela.
- **Erros a evitar (Cap. 3):** estourar a tela única, contexto insuficiente,
  detalhe/precisão excessivos, variedade sem sentido, mídia inadequada,
  codificação imprecisa, má organização, destaque ineficaz, decoração inútil.
- **Simplicidade (§5.1):** "Simplify, simplify, simplify"; incluir só o necessário,
  condensado sem perda de sentido, em mídia legível mesmo pequena; o dashboard
  dá o panorama instantâneo, o detalhe vem depois (drill-down → aba de partidas).
- **Conexão:** justifica cada decisão visual do Cap. 4 e o que o projeto evitou.

## Síntese para o cap. 2

A literatura converge em VC persistente no Brasil (~65% Pollard, acima da Europa),
maior na B que na A em 2003–2009, e sensível a contexto (torcida, VAR, viagens).
O TCC contribui com: série anual longa e homogênea (2006–2024, 20 clubes ida/volta),
auditoria documentada e sistema reproduzível — não com nova teoria causal.
