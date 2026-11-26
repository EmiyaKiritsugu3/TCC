# Vantagem de jogar em casa na Série A: uma análise baseada em modelos de 12 temporadas (2013–2024)

José Inamar de Medeiros Júnior

Universidade Federal do Rio Grande do Norte (UFRN), Centro de Ensino Superior do Seridó (CERES), Bacharelado em Sistemas de Informação, Caicó, RN, Brasil

## Resumo

A vantagem de jogar em casa é uma das regularidades mais robustas do esporte coletivo, mas sua magnitude e estabilidade no futebol brasileiro ainda são debatidas. Este artigo analisa 4.559 partidas da Série A entre 2013 e 2024, usando uma base de dados aberta e licenciada em MIT. Combinamos o índice de Pollard, um modelo formal de mudança de nível e um modelo de Poisson de ataque–defesa que separa a qualidade das equipes do efeito de jogar em casa. Os mandantes venceram 48,4% das partidas e conquistaram 63,0% dos pontos (IC 95% 61,7–64,3). A série anual cai de 65,0% em 2013–2018 para 61,0% em 2019–2024 (diferença de 4,0 p.p.; IC bootstrap por cluster 0,9–6,6), com ponto de quebra estimado em 2019. O modelo de Poisson conta a mesma história em espaço de gols: o multiplicador de gols do mandante caiu 12,0% (de 1,565 para 1,377; IC −18,1% a −5,5%), o que reduziu o prêmio de gols em casa de +56,5% para +37,7%. Apenas 2,2% da variância da vantagem por equipe-temporada está entre equipes, o que indica que a vantagem é predominantemente um fenômeno da liga, não um traço estável de cada clube. O público tem associação fraca com a vantagem de casa (ρ = 0,08), embora tenha associação forte com a força do clube (ρ = 0,41). Os cartões nos jogos sem torcida de 2020 se movem na direção esperada, mas permanecem imprecisos. A queda é robusta a controles de qualidade das equipes e de temporada e não é atribuível a um único canal; discutimos implicações para previsão, equilíbrio competitivo e interpretação de referenciais pós-2019.

**Palavras-chave:** vantagem de jogar em casa; futebol brasileiro; índice de Pollard; modelo de Poisson; mudança de nível; COVID-19.

## Abstract

Home advantage is one of the most robust regularities in team sports, but its magnitude and stability in Brazilian football remain debated. We study 4,559 matches of the Brazilian Série A from 2013 to 2024 using an open, MIT-licensed match database. We combine the Pollard points index, a formal change-point model, and a Poisson attack–defence model that separates team quality from the home effect. Home teams won 48.4% of matches and captured 63.0% of points (95% CI 61.7–64.3). The annual series falls from 65.0% in 2013–2018 to 61.0% in 2019–2024 (difference 4.0 pp; cluster-bootstrap CI 0.9–6.6), with the break date estimated at 2019. The Poisson model tells the same story in goal space: the home team's goal multiplier fell by 12.0% (from 1.565 to 1.377; CI −18.1% to −5.5%), reducing the home-goal premium from +56.5% to +37.7%. Only 2.2% of the variance in team-season home advantage is between teams, indicating that home advantage is predominantly a league-wide phenomenon rather than a stable club trait. Attendance is only weakly associated with home advantage (ρ = 0.08) although strongly associated with team strength (ρ = 0.41). Referee cards around the 2020 ghost games move in the expected direction but remain imprecise. The decline is robust to team quality and season effects and is not attributable to a single channel; we discuss implications for forecasting, competitive balance, and the interpretation of post-2019 benchmarks.

**Keywords:** home advantage; Brazilian football; Pollard index; Poisson model; change-point; COVID-19.

**Códigos JEL:** C12, C23, Z20.

## 1. Introdução

A vantagem de jogar em casa — a tendência sistemática de equipes se saírem melhor em casa do que fora — é um dos achados mais consistentes da literatura de economia do esporte. Ela foi documentada no futebol, no basquete, no hóquei no gelo e em outros esportes coletivos, com magnitudes que variam entre países, competições e períodos (POLLARD, 1986; NEVILL; HOLDER, 1999). No futebol, o fenômeno costuma ser resumido pela parcela de pontos conquistada pelos mandantes. Valores acima de 50% em um campeonato equilibrado de ida e volta indicam vantagem; em muitas ligas profissionais, a parcela observada fica entre 55% e 65% (POLLARD; SILVA; MEDEIROS, 2008; ALMEIDA; OLIVEIRA; SILVA, 2011).

A Série A brasileira é um laboratório interessante por três razões. Primeiro, combina um longo campeonato de pontos corridos com grandes distâncias territoriais e um conjunto heterogêneo de clubes, o que torna viagem, familiaridade com o estádio e apoio da torcida mecanismos plausíveis, mas potencialmente compensatórios. Segundo, a liga passou por dois choques salientes em uma janela curta: a introdução do árbitro assistente de vídeo (VAR) em 2019 e a pandemia de COVID-19 em 2020–2021, quando parte das partidas foi disputada sem torcida. Terceiro, a literatura brasileira é dominada por estudos descritivos com amostras curtas ou comparações agregadas, enquanto modelos formais que separam a qualidade das equipes do efeito de jogar em casa são escassos. As decisões de arbitragem também são sensíveis à pressão da torcida (NEVILL et al., 2002; GARICANO; PALACIOS-HUERTA; PRENDERGAST, 2005; BOYKO; BOYKO; BOYKO, 2007; DOHMEN, 2008; BURAIMO; FORREST; SIMMONS, 2010; SUTTER; KOCHER, 2004), o que torna o episódio brasileiro dos jogos sem torcida particularmente informativo.

Este artigo faz três perguntas. Qual foi a magnitude da vantagem de jogar em casa na Série A entre 2013 e 2024? Ela mudou depois de 2018, e quando? Quais canais são consistentes com o padrão observado? Respondemos com um pipeline reproduzível construído sobre uma base aberta, o índice de Pollard, um modelo de mudança de nível e um modelo de Poisson de ataque–defesa. O modelo de Poisson é particularmente útil porque diferenças brutas entre casa e fora misturam o efeito de casa com a qualidade das equipes: uma equipe forte pode marcar muitos gols em casa simplesmente porque é forte. Ao estimar ataque e defesa para cada equipe, efeitos de temporada e um parâmetro separado de vantagem de casa, isolamos a assimetria dentro da partida que o índice descritivo apenas aproxima.

O artigo contribui de quatro maneiras. Primeiro, oferece uma série de 12 temporadas totalmente reproduzível, construída a partir de uma fonte licenciada em MIT, com validação explícita contra uma base pública independente. Segundo, estima a mudança de nível formalmente e reporta um intervalo bootstrap por cluster para a mudança, em vez de depender de inspeção visual. Terceiro, estima um modelo de Poisson de ataque–defesa com interação casa × período, que mostra que a queda está presente em espaço de gols e sobrevive a controles de qualidade das equipes e de temporada. Quarto, quantifica a heterogeneidade da vantagem entre equipes e a relaciona com público, contexto e cartões. Os resultados são descritivos e observacionais; não reivindicamos identificação causal.

O restante do artigo está organizado da seguinte forma. A seção 2 reúne dados e métodos. A seção 3 apresenta os resultados e a discussão. A seção 4 traz as considerações finais.

## 2. Dados e métodos

### 2.1 Base e validação

Os dados primários são as temporadas 2013–2024 da Série A, obtidas do repositório `BrazilianFootball/Data` (licença MIT), que extrai informações de partidas dos borderôs eletrônicos da Confederação Brasileira de Futebol (CBF). A amostra final contém 4.559 partidas: 380 por temporada, exceto 2016, que tem 379 porque a partida Chapecoense–Atlético-MG foi cancelada após o acidente aéreo da Chapecoense. A temporada 2020 foi disputada de 8 de agosto de 2020 a 25 de fevereiro de 2021 por causa da pandemia. Cada registro inclui data, equipes mandante e visitante, gols, estádio e cartões disciplinares. Os dados não incluem público nem identidade do árbitro; esses campos vêm da compilação da Base dos Dados/Transfermarkt para o mesmo período.

A amostra começa em 2013 por uma razão de disponibilidade: os borderôs eletrônicos da CBF começam nesse ano, e o repositório licenciado em MIT cobre 2013 em diante. Temporadas anteriores exigiriam uma fonte diferente, não eletrônica, e estão fora do escopo. Essa restrição é uma vantagem para a reprodutibilidade: toda a análise no nível de partida pode ser reconstruída a partir de uma fonte pública e permissiva.

Validamos os resultados das partidas contra o OpenFootball (CC0). Para 2018–2024, 2.658 de 2.660 partidas têm placares idênticos (99,92%). Permanece uma divergência de placar para Internacional × Atlético-MG em 2019 (o arquivo derivado da CBF registra 0–0; o OpenFootball registra 2–1), e uma partida de 2023 é um jogo de dois dias com divergência de data. Ambas estão documentadas no material de replicação. O recálculo dos campeões a partir dos resultados produz o campeão oficial nas 12 temporadas (2013–2024), incluindo o Botafogo-RJ em 2024.

### 2.2 Público, arbitragem e cartões

O público está disponível para 4.555 de 4.559 partidas (99,9%). Há 628 registros de público zero: 598 são reais (380 em 2020 e 218 em 2021); os outros 30 são zeros esparsos em outras temporadas, mantidos como registros, mas podem incluir falhas. A identidade do árbitro está disponível para 4.541 partidas (99,6%). Cartões amarelos e vermelhos estão disponíveis para todas as 4.559 partidas, com um cartão não atribuído em 2022 (registro malformado). Público e arbitragem vêm da Base dos Dados/Transfermarkt; 2024 foi complementado pelo FBref (90 partidas). Esses dados são usados apenas nas análises descritivas; os resultados principais dependem dos dados de partida licenciados em MIT.

### 2.3 Índice de Pollard e inferência

Os resultados são derivados do placar: vitória vale três pontos, empate vale um e derrota vale zero. O índice de Pollard (POLLARD, 1986; MATOS; AMARO; POLLARD, 2020) para a temporada t é

`HA_t = 100 × P^H_t / (P^H_t + P^A_t)`

em que P^H_t e P^A_t são os pontos totais conquistados por mandantes e visitantes na temporada t. Um valor de 50 indica neutralidade; valores acima de 50 indicam vantagem de casa. Também usamos a vantagem por equipe-temporada HA_it = pontos por jogo em casa_it − pontos por jogo fora_it, que é a unidade da análise de heterogeneidade.

O índice de Pollard é nossa medida descritiva da vantagem agregada. Reportamos valores por temporada e um intervalo de confiança de 95% global baseado em reamostragem de partidas com reposição (4.000 repetições). Como partidas que envolvem as mesmas equipes não são independentes, os intervalos anuais são descritivos; para a mudança de nível usamos um bootstrap por cluster que reamostra temporadas inteiras. Essa distinção importa: os intervalos anuais respondem “quanto a média da temporada variaria se reamostrássemos suas partidas?”, não “qual é a incerteza amostral do parâmetro da liga?”.

### 2.4 Mudança de nível

Seja y_t o índice de Pollard na temporada t. Estimamos o modelo de mudança de média (CHOW, 1960)

`y_t = α + β · 1(t ≥ τ) + ε_t`

em que τ é uma data de quebra candidata. Estimamos τ minimizando a soma dos quadrados dos resíduos sobre todas as datas candidatas com pelo menos três temporadas de cada lado. A quebra estimada é a data que melhor separa duas médias constantes. Reportamos as médias pré e pós-quebra e a diferença; o intervalo de 95% para a diferença vem de um bootstrap por cluster que reamostra temporadas dentro de cada período (5.000 repetições). Este é um modelo descritivo de mudança de nível; não identifica a causa da quebra.

### 2.5 Poisson ataque–defesa

Para separar o efeito de casa da qualidade das equipes, modelamos os dois placares de cada partida. Seja i o mandante, j o visitante e t a temporada. Os gols esperados são

`log λ^H_ijt = μ + a_i − d_j + γ + δ · 1(t ≥ 2019) + θ_t`

`log λ^A_ijt = μ + a_j − d_i + θ_t`

usamos uma equipe de referência com ataque e defesa iguais a zero; os efeitos das demais equipes são relativos a ela. Aqui a_i é o ataque da equipe i, d_i sua defesa, γ a vantagem de casa antes de 2019, δ a mudança na vantagem de casa depois de 2019 e θ_t um efeito fixo de temporada. O modelo é uma especificação de Poisson de ataque–defesa na tradição de Maher (1982) e Dixon e Coles (1997); não aplicamos a correção para placares baixos porque o foco é o parâmetro de casa, não a previsão de placar.

Estimamos o modelo por mínimos quadrados reponderados iterativamente (IRLS de Poisson), com uma equipe de referência e uma temporada de referência. Os erros-padrão são robustos por cluster no nível da partida: as duas observações de gols da mesma partida são correlacionadas, e a clusterização por partida absorve essa dependência (CAMERON; GELBACH; MILLER, 2008; CAMERON; MILLER, 2015). Também reportamos a estatística de dispersão de Pearson; valores próximos de um são consistentes com a hipótese de variância de Poisson, e valores acima de um exigiriam erros quase-Poisson ou binomial negativa. As quantidades de interesse são γ, γ+δ e δ. Reportamos tanto os coeficientes em log quanto os efeitos multiplicativos exp(·)−1, que têm interpretação simples: o percentual em que os gols esperados do mandante excedem os do visitante, mantendo ataque, defesa e temporada fixos.

### 2.6 Heterogeneidade

Decompomos a variância da vantagem por equipe-temporada com um modelo de efeitos aleatórios de um fator:

`HA_it = μ + u_i + e_it`

em que u_i é um efeito de equipe e e_it é um resíduo equipe-temporada. A correlação intraclasse ρ = σ²_u/(σ²_u+σ²_e) é a parcela da variância que está entre equipes. Um valor próximo de zero implicaria que a vantagem de casa é um fenômeno da liga; um valor grande implicaria que os clubes diferem de forma persistente. A decomposição é descritiva e não impõe um modelo distribucional a u_i.

### 2.7 Canais

#### 2.7.1 Cartões e pênaltis

Para a extensão disciplinar, seja D_ijt a diferença entre cartões amarelos recebidos pelo mandante e pelo visitante na partida t. Estimamos

`D_ijt = β_0 + β_1 Post_t + α_i + α_j + ε_ijt`

em que Post_t = 1 para 2020 e α_i, α_j são efeitos fixos de mandante e visitante. O coeficiente β_1 é uma estimativa de diferenças em diferenças: compara a diferença de cartões casa–fora em 2020 com a diferença em 2019, após absorver diferenças invariantes no tempo entre equipes. Os erros-padrão são uma aproximação prática: calculamos variâncias robustas por cluster unidirecional por mandante e por visitante e tomamos o maior erro-padrão, o que evita o problema de variâncias negativas que a inclusão–exclusão multiway pode produzir em amostras pequenas (CAMERON; MILLER, 2015). Essa aproximação não é uma garantia formal de covariância two-way. A estimativa é descritiva; cartões refletem tanto decisões de arbitragem quanto comportamento dos jogadores. O JSON também marca gols de pênalti com `PN`; usamos essa marcação em um piloto, mas não observamos pênaltis perdidos ou marcados.

#### 2.7.2 Público

No nível equipe-temporada, calculamos correlações de Spearman entre o público médio e (i) a vantagem de casa por equipe-temporada e (ii) os pontos. O público é endógeno — depende do adversário, da fase, dos preços e do clima —, então as correlações são descritivas e não devem ser lidas como efeitos causais.

### 2.8 Reprodutibilidade

Todas as etapas são scriptadas. A base de partidas é construída por `scripts/build_mit_base.py`; as figuras e tabelas descritivas por `scripts/analyze_artigo.py`; o modelo de Poisson e a decomposição de variância por `scripts/analyze_models.py`; a análise de cartões por `scripts/analyze_cards.py`. Os JSONs brutos de partidas não são redistribuídos; a construção é fixada em um commit específico do repositório MIT. O repositório também contém o dashboard usado para explorar os dados.

## 3. Resultados e discussão

### 3.1 Nível e quebra

A Tabela 1 reporta as estatísticas descritivas por temporada. Os mandantes venceram 48,4% das partidas, os empates representaram 26,9% e os visitantes venceram 24,7%. A média de gols foi 1,41 para os mandantes e 0,96 para os visitantes. O índice de Pollard agregado foi 63,0% (IC 95% 61,7–64,3), 13,0 pontos percentuais acima da neutralidade.

**Tabela 1 – Estatísticas descritivas por temporada, Série A, 2013–2024.**

| Temporada | Partidas | Vitória / empate / derrota (%) | Gols casa / fora | Pollard (IC 95%) |
|---:|---:|---:|---:|---:|
| 2013 | 380 | 48,4 / 28,4 / 23,2 | 1,47 / 0,99 | 63,95 (59,28–68,24) |
| 2014 | 380 | 51,8 / 24,2 / 23,9 | 1,42 / 0,84 | 65,17 (60,56–69,65) |
| 2015 | 380 | 52,6 / 23,9 / 23,4 | 1,46 / 0,90 | 65,87 (61,30–70,12) |
| 2016 | 379 | 53,3 / 24,8 / 21,9 | 1,49 / 0,92 | 67,11 (62,80–71,43) |
| 2017 | 380 | 43,9 / 27,1 / 28,9 | 1,38 / 1,04 | 58,24 (53,43–62,64) |
| 2018 | 380 | 53,2 / 28,9 / 17,9 | 1,38 / 0,79 | 69,51 (65,35–73,68) |
| 2019 | 380 | 48,2 / 26,1 / 25,8 | 1,38 / 0,92 | 62,25 (57,77–67,08) |
| 2020 | 380 | 45,0 / 28,4 / 26,6 | 1,41 / 1,07 | 60,17 (55,44–64,60) |
| 2021 | 380 | 45,8 / 29,7 / 24,5 | 1,27 / 0,94 | 61,83 (57,20–66,21) |
| 2022 | 380 | 44,2 / 28,4 / 27,4 | 1,41 / 0,98 | 59,30 (54,49–63,87) |
| 2023 | 380 | 46,8 / 25,8 / 27,4 | 1,42 / 1,07 | 60,65 (56,10–65,15) |
| 2024 | 380 | 47,4 / 26,6 / 26,1 | 1,41 / 1,03 | 61,69 (57,06–66,10) |

Nota: índice de Pollard = 100 × pontos do mandante/(pontos do mandante + pontos do visitante). Os intervalos de confiança são descritivos, obtidos por bootstrap de 4.000 reamostragens de partidas; não corrigem a dependência entre partidas das mesmas equipes na temporada. Fonte: BrazilianFootball/Data (MIT).

A vantagem de casa em 2013–2024 foi grande para padrões internacionais: 63,0% dos pontos foram para os mandantes, 13,0 pontos percentuais acima da neutralidade. A série por temporada, porém, não é plana (Figura 1). Ela varia de 58,2% em 2017 a 69,5% em 2018, e os valores altos de 2015–2016 e 2018 são seguidos por um patamar mais baixo depois de 2019. A impressão visual é confirmada pelo modelo de mudança de nível: a data de quebra que minimiza a soma dos quadrados dos resíduos é 2019, com média pré-quebra de 65,0% e média pós-quebra de 61,0% (diferença de 4,0 p.p.; IC bootstrap por cluster 0,9–6,6). A temporada 2020, disputada sem torcida, registrou 60,2%; as temporadas 2022–2024, com o público de volta, tiveram média de 60,6%. O retorno dos espectadores não restaurou o nível pré-2019.

![Figura 1 – Índice de Pollard por temporada, 2013–2024. Os pontos são valores anuais; a faixa sombreada é um intervalo descritivo de 95% por bootstrap de partidas. As linhas tracejadas são as médias de 2013–2018 (65,0%) e 2019–2024 (61,0%); a linha pontilhada vertical marca 2019.](../figuras/artigo_serie_pollard.png)

Fonte: elaboração do autor; BrazilianFootball/Data (MIT).

### 3.2 A queda em espaço de gols

O índice descritivo mistura o efeito de casa com a qualidade das equipes. O modelo de Poisson separa os dois. A Tabela 2 reporta as estimativas. Antes de 2019, os gols esperados do mandante eram 56,5% maiores que os do visitante, condicionais a ataque, defesa e temporada (coeficiente em log 0,448; EP 0,026; IC 95% 0,397–0,500). Depois de 2019, a diferença caiu para 37,7% (coeficiente em log 0,320; EP 0,026; IC 95% 0,270–0,371). A interação é negativa e precisa: o multiplicador de gols do mandante caiu 12,0% (de 1,565 para 1,377; coeficiente em log −0,128; EP 0,037; IC 95% −0,200 a −0,056; p < 0,001); o prêmio de gols em casa caiu de +56,5% para +37,7% (18,8 p.p.; 33,3% de redução relativa). A dispersão de Pearson é 0,925, portanto não há evidência de superdispersão; os erros-padrão robustos por cluster são os relevantes.

**Tabela 2 – Modelo de Poisson ataque–defesa, 2013–2024.**

| Parâmetro | Coeficiente (log) | EP | IC 95% | Efeito multiplicativo |
|---|---:|---:|---:|---:|
| Vantagem de casa antes de 2019 | 0,448 | 0,026 | 0,397 a 0,500 | +56,5% |
| Vantagem de casa × pós-2019 | −0,128 | 0,037 | −0,200 a −0,056 | −12,0% |
| Vantagem de casa depois de 2019 | 0,320 | 0,026 | 0,270 a 0,371 | +37,7% |

Nota: modelo de Poisson com ataque e defesa por equipe, efeitos fixos de temporada e interação casa × pós-2019. N = 4.559 partidas (9.118 observações de gols); 84 parâmetros. Erros-padrão robustos por cluster de partida. Dispersão de Pearson = 0,925. O efeito multiplicativo é exp(β) − 1. Fonte: cálculos do autor.

O modelo, portanto, confirma o resultado descritivo em uma especificação mais exigente: a queda não é artefato de mudanças na composição das equipes nem de tendências de pontuação da liga. É uma mudança na assimetria de casa dentro da partida.

### 3.3 A vantagem é específica de cada equipe?

A decomposição de um fator da vantagem por equipe-temporada produz uma correlação intraclasse de 0,022: apenas cerca de 2,2% da variância está entre equipes, enquanto 97,8% está dentro das equipes ao longo das temporadas. A vantagem média por equipe-temporada é 0,709 ponto por jogo, mas o componente de variância entre equipes é pequeno (0,004) em relação ao componente dentro (0,170). Isso sugere que a vantagem de casa é primordialmente um fenômeno da liga: o componente entre equipes é pequeno, e os 97,8% restantes são variação equipe-temporada que mistura diferenças persistentes dentro da equipe com ruído entre temporadas. A decomposição não estima parâmetros por clube; com 12 temporadas e 36 equipes, um modelo hierárquico seria necessário para separar efeitos persistentes de clube do ruído, e a decomposição descritiva não sustenta afirmações fortes de vantagem persistente específica de clube.

### 3.4 Contexto e público

Os contrastes contextuais são modestos. A distância produz um gradiente monotônico, mas raso: o índice de Pollard é 63,7% para viagens curtas (<500 km), 62,9% para viagens médias (500–1.499 km) e 62,0% para viagens longas (≥1.500 km); os intervalos de confiança se sobrepõem, então o gradiente é descritivo, não decisivo. Os clássicos têm índice menor (59,1%) que os não clássicos (63,2%), consistente com a ideia de que rivais locais são mais equilibrados ou mais acostumados ao estádio. O estádio habitual está associado a 63,3% contra 60,7% de um estádio alternativo. O gradiente contextual mais forte é a força pré-jogo: o mandante tem 73,3% quando é favorito, 62,1% quando a partida é equilibrada e 54,2% quando é azarão. Mesmo o azarão permanece acima de 50%.

O público é um correlato fraco da vantagem de casa e um correlato forte da força da equipe. No nível equipe-temporada (n = 240), a correlação de Spearman entre público médio e vantagem de casa é 0,08; entre público e pontos, é 0,41 (Figura 2). Excluir os 30 zeros esparsos fora de 2020–2021 deixa as correlações praticamente iguais (0,08 e 0,39). O padrão é consistente com a literatura que identifica o apoio da torcida como um canal entre vários: o público separa clubes grandes de pequenos, mas não explica por que o mesmo clube é mais favorecido em casa. A temporada 2020 sem torcida e o retorno de 2022–2024 reforçam o ponto: o índice caiu para 60,2% sem torcida e ficou em 60,6% depois do retorno, de modo que a torcida não é a história toda, nem é irrelevante.

![Figura 2 – Público, vantagem de casa e pontos no nível equipe-temporada, 2013–2024. Cada ponto é uma equipe-temporada; as linhas são ajustes de mínimos quadrados; ρ é o coeficiente de Spearman. Esquerda: vantagem de casa (pontos em casa menos pontos fora por jogo). Direita: pontos totais na temporada.](../figuras/artigo_publico_ha.png)

Fonte: elaboração do autor; BrazilianFootball/Data (MIT) e Base dos Dados/Transfermarkt.

### 3.5 Cartões e pênaltis

A extensão disciplinar é sugestiva, mas não conclusiva (Figura 3). Em 2019, o mandante recebeu 0,18 cartão amarelo a menos que o visitante; em 2020, a diferença passou a +0,11. A mudança bruta é +0,29. Com efeitos fixos de mandante e visitante, a estimativa de diferenças em diferenças é +0,35 (EP 0,190; IC 95% −0,03 a +0,72; n = 760). Restringindo a amostra às 16 equipes presentes nos dois anos, obtemos +0,34 (IC 95% −0,04 a +0,72; n = 480). O ponto estimado é consistente com um canal de arbitragem/torcida, mas o intervalo inclui zero, e 2020 também mudou o calendário, os protocolos e o ambiente do VAR. Tratamos o resultado, portanto, como um sinal de robustez, não como evidência de efeito causal da arbitragem. No mesmo recorte, os pênaltis convertidos não mostram mudança detectável: +0,05 por jogo (EP 0,052; IC 95% −0,06 a +0,15; n = 760).

![Figura 3 – Diferença de cartões amarelos entre mandante e visitante, 2013–2024. Os pontos são médias por temporada; a faixa sombreada é um intervalo descritivo de 95% por bootstrap; a faixa vermelha marca 2020.](../figuras/fig13_cartoes.png)

Fonte: elaboração do autor; BrazilianFootball/Data (MIT).

### 3.6 Discussão geral

O primeiro resultado é que a vantagem de casa na Série A foi grande, mas não estável. O agregado de 63,0% está alinhado com estimativas brasileiras anteriores em torno de 65% (SILVA; MOREIRA, 2008; ALMEIDA; OLIVEIRA; SILVA, 2011; POLLARD; SILVA; MEDEIROS, 2008), mas o patamar pós-2019 é claramente menor. O modelo de mudança de nível situa a quebra em 2019, o ano de introdução do VAR. A coincidência é sugestiva, mas o desenho não separa o VAR das outras mudanças que vieram depois, incluindo a pandemia, o calendário e o retorno gradual do público. O modelo de Poisson mostra que a queda não é um efeito de composição: ela sobrevive a efeitos fixos de ataque, defesa e temporada. Essa é a evidência mais forte do artigo.

O segundo resultado é que a queda é visível em gols, não apenas em pontos. O multiplicador de gols do mandante caiu 12,0% (de 1,565 para 1,377), e o prêmio de gols em casa caiu de +56,5% para +37,7% (18,8 p.p.; 33,3% de redução relativa). Isso importa para previsão e para a interpretação de referenciais históricos. Um modelo calibrado em 2013–2018 superestimaria o efeito de casa depois de 2019. Analistas deveriam usar dados pós-2019, ou modelar explicitamente a quebra, ao avaliar partidas atuais.

O terceiro resultado é que a heterogeneidade entre equipes é pequena. Apenas cerca de 2,2% da variância da vantagem por equipe-temporada está entre equipes; os 97,8% restantes estão dentro das equipes ao longo das temporadas. Isso contrasta com a intuição comum de que alguns clubes são persistentemente mais dependentes do mando. Nesta amostra, o componente da liga domina; a decomposição não estima parâmetros por clube, e um modelo hierárquico seria necessário para separar efeitos persistentes de ruído. A implicação prática é que um parâmetro comum de vantagem de casa pode ser adequado para muitos propósitos; modelos específicos por equipe devem ser usados com cautela e com encolhimento parcial, não como rankings isolados.

O quarto resultado é que o público não é um correlato forte da vantagem de casa. Isso pode parecer surpreendente, mas é consistente com a visão multicanal: o apoio da torcida é um insumo, e seu efeito pode ser compensado por qualidade das equipes, táticas e comportamento da arbitragem. A literatura de jogos sem torcida encontrou efeitos de público em algumas ligas (FISCHER; HAUCAP, 2021; SCOPPA, 2021; ENDRICH; GESCHE, 2020; BRYSON et al., 2021), mas as magnitudes variam e a identificação não é uniforme. Nossa evidência brasileira aponta para uma associação modesta, não dominante.

O resultado de cartões é o mais especulativo. O ponto estimado está na direção esperada, mas o intervalo inclui zero e a temporada 2020 é um conjunto de tratamentos. O exercício é útil principalmente para mostrar que o canal da arbitragem pode ser medido com dados abertos; não é um teste causal. O piloto de pênaltis convertidos não sustenta um canal arbitral forte: o intervalo inclui zero, mas não exclui um efeito positivo moderado, e a medida exclui pênaltis perdidos. Um desenho mais forte combinaria pênaltis, faltas e tipos de cartão, e usaria o retorno gradual do público como contraste adicional.

#### 3.6.1 Limitações

A análise é observacional. A quebra de 2019 coincide com o VAR; a temporada 2020 coincide com a pandemia; o retorno do público coincide com mudanças de protocolos e calendário. Não reivindicamos identificação causal. A data de quebra é estimada com apenas 12 observações anuais; seu timing exato é impreciso, e o objeto robusto é a diferença entre as médias pré e pós-2019, não a data em si. A amostra começa em 2013 porque os borderôs eletrônicos da CBF começam nesse ano; temporadas anteriores exigiriam uma fonte diferente e estão fora do escopo. Os dados de partidas têm uma divergência de placar e uma exceção de data em relação ao OpenFootball, ambas documentadas. O público está ausente em quatro partidas; dos 628 zeros, 598 são reais (2020–2021) e 30 são zeros esparsos em outras temporadas. O modelo de Poisson assume variância de Poisson e estrutura log-linear; a estatística de dispersão está próxima de um, mas uma binomial negativa ou uma correção de Dixon–Coles poderia ser explorada. A decomposição de variância é um modelo descritivo de um fator; um modelo hierárquico com efeitos de equipe e temporada forneceria melhor encolhimento e incerteza para a vantagem específica de cada equipe. Por fim, cartões não são decisões: refletem tanto a discricionariedade do árbitro quanto o comportamento dos jogadores; os dados incluem pênaltis convertidos, mas não pênaltis marcados/perdidos nem faltas por árbitro.

#### 3.6.2 Implicações

Para previsão e avaliação de equipes, a principal implicação é que o efeito de casa pré-2019 não é um referencial seguro. Um modelo que ignora a quebra superestimará a vantagem de jogar em casa no regime pós-2019. Para o equilíbrio competitivo, uma vantagem de casa menor tende a reduzir a importância do mando e pode mudar o trade-off entre estratégias em casa e fora. Para política, os resultados não sustentam uma explicação de causa única: o apoio da torcida importa menos do que uma leitura ingênua dos jogos sem torcida de 2020 sugeriria, e o canal da arbitragem permanece sugestivo. O pipeline aberto torna possível atualizar a análise à medida que novas temporadas ficam disponíveis.

## 4. Considerações finais

A pergunta era dupla: qual foi a magnitude da vantagem de jogar em casa na Série A entre 2013 e 2024 e ela mudou? A resposta curta é: **a vantagem foi grande, mas o referencial mudou**. O mandante conquistou **63,0%** dos pontos (IC 61,7–64,3), com quebra estimada em **2019**: **65,0% em 2013–2018** contra **61,0% em 2019–2024** (4,0 p.p.; IC 0,9–6,6). Para uso prático, a referência é a média pós-2019 de **61,0%** (60,6% em 2022–2024); os valores anuais variam de 59,3% a 62,3%, e o patamar não volta aos 65,0% anteriores.

A diferença não é só de pontos. No modelo de Poisson de ataque–defesa, o multiplicador de gols do mandante caiu **12,0%** (de 1,565 para 1,377; IC −18,1% a −5,5%), e o prêmio de gols em casa caiu de **+56,5%** para **+37,7%** (18,8 p.p.; 33,3% de redução relativa). Em termos concretos, uma equipe com expectativa de **1,0 gol fora de casa** passaria de cerca de **1,57 gol esperado em casa** no regime antigo para cerca de **1,38** no regime atual. Um modelo calibrado em 2013–2018, portanto, superestima a vantagem de casa em cerca de **4 p.p. de pontos** e **0,19 gol** nesse exemplo.

A vantagem também não é um traço estável de cada clube. Apenas **2,2%** da variância da vantagem por equipe-temporada está entre equipes; **97,8%** está dentro das equipes ao longo das temporadas. Isso tem uma implicação prática: rankings de "quem tem mais vantagem de casa" são pouco confiáveis com 12 temporadas, e um parâmetro comum de liga é mais defensável do que estimativas isoladas por clube. Clubes e analistas devem evitar tratar a vantagem de casa como uma característica permanente da equipe.

Os canais testados não explicam a queda sozinhos. O público tem correlação fraca com a vantagem de casa (**ρ = 0,08**), embora forte com a força da equipe (**ρ = 0,41**); em 2020, sem torcida, o Pollard foi **60,2%**, e em 2022–2024, com público de volta, **60,6%** — o retorno não restaurou o padrão pré-2019. Os cartões se movem na direção esperada (**+0,35**), mas o IC inclui zero (**−0,03 a +0,72**), e 2020 concentra pandemia, calendário e protocolos. A leitura responsável é multicanal: VAR (2019), pandemia (2020), calendário, público e arbitragem podem contribuir, mas este desenho não separa esses choques.

**O que fica de concreto:**

- adotar **61,0%** (ou 60,6% em 2022–2024) como referência pós-2019 em análises e previsões;
- não classificar clubes por vantagem de casa sem encolhimento e intervalos de confiança;
- tratar 2020 como choque de público, não como experimento isolado;
- usar o pipeline aberto para atualizar a série a cada temporada.

As limitações são as de um estudo observacional de 12 temporadas: a série começa em 2013 por causa dos borderôs eletrônicos; há uma divergência de placar e uma exceção de data na validação; só observamos pênaltis convertidos (`PN`); pênaltis marcados/perdidos e faltas por árbitro não estão disponíveis; e a quebra de 2019 coincide com o VAR. Os dados cobrem apenas a Série A; a participação na Copa do Brasil e na Libertadores não é observada, então a congestão de outras competições não é identificada, e a diferença de descanso é, na melhor das hipóteses, uma proxy imperfeita. A agenda futura é objetiva: **(i)** atualizar com 2025; **(ii)** estimar um modelo hierárquico bayesiano para a vantagem por equipe; **(iii)** incorporar pênaltis, faltas, tipos de cartão e congestão de outras competições; **(iv)** replicar em Séries B–D e no futebol feminino; **(v)** testar o VAR como evento e o retorno gradual da torcida como contraste; **(vi)** usar odds ou Elo para separar expectativa de qualidade.

## Disponibilidade de dados e código

O código de replicação e as tabelas derivadas estão disponíveis em https://github.com/EmiyaKiritsugu3/TCC. Os dados de partidas vêm do BrazilianFootball/Data (MIT, commit `0dd1bc5`); público e arbitragem vêm da Base dos Dados/Transfermarkt; a validação usa o OpenFootball (CC0). O arquivo de partidas processado não é redistribuído; ele é reconstruído pelos scripts a partir da fonte pública fixada.

## Referências

ALMEIDA, L. G.; OLIVEIRA, M. L.; SILVA, C. D. Uma análise da vantagem de jogar em casa nas duas principais divisões do futebol profissional brasileiro. **Revista Brasileira de Educação Física e Esporte**, v. 25, n. 1, p. 49-54, 2011.

BASE DOS DADOS. **Brasileirão Série A**. 2026. Disponível em: https://basedosdados.org/dataset/c861330e-bca2-474d-9073-bc70744a1b23. Acesso em: 20 nov. 2026.

BOYKO, R. H.; BOYKO, A. R.; BOYKO, M. G. Referee bias contributes to home advantage in English Premiership football. **Journal of Sports Sciences**, v. 25, n. 11, p. 1185-1194, 2007.

BRAZILIANFOOTBALL/DATA. **BrazilianFootball/Data**: results and match cards from Brazilian football. 2026. Disponível em: https://github.com/BrazilianFootball/Data. Acesso em: 20 nov. 2026.

BRYSON, A. et al. Causal effects of an absent crowd on performances and refereeing decisions during Covid-19. **Economics Letters**, v. 198, 109664, 2021.

BURAIMO, B.; FORREST, D.; SIMMONS, R. The 12th man?: refereeing bias in English and German soccer. **Journal of the Royal Statistical Society: Series A**, v. 173, n. 2, p. 431-449, 2010.

CAMERON, A. C.; GELBACH, J. B.; MILLER, D. L. Bootstrap-based improvements for inference with clustered errors. **Review of Economics and Statistics**, v. 90, n. 3, p. 414-427, 2008.

CAMERON, A. C.; MILLER, D. L. A practitioner's guide to cluster-robust inference. **Journal of Human Resources**, v. 50, n. 2, p. 317-372, 2015.

CHOW, G. C. Tests of equality between sets of coefficients in two linear regressions. **Econometrica**, v. 28, n. 3, p. 591-605, 1960.

DIXON, M. J.; COLES, S. G. Modelling association football scores and inefficiencies in the football betting market. **Journal of the Royal Statistical Society: Series C**, v. 46, n. 2, p. 265-280, 1997.

DOHMEN, T. J. The influence of social forces: evidence from the behavior of football referees. **Economic Inquiry**, v. 46, n. 3, p. 411-424, 2008.

ENDRICH, M.; GESCHE, T. Home-bias in referee decisions: evidence from "ghost games" during the COVID-19 pandemic. **Economics Letters**, v. 197, 109621, 2020.

FISCHER, K.; HAUCAP, J. Does crowd support drive the home advantage in professional football? Evidence from German ghost games during the COVID-19 pandemic. **Journal of Sports Economics**, v. 22, n. 8, p. 982-1008, 2021.

GARICANO, L.; PALACIOS-HUERTA, I.; PRENDERGAST, C. Favoritism under social pressure. **Review of Economics and Statistics**, v. 87, n. 2, p. 208-216, 2005.

MAHER, M. J. Modelling association football scores. **Statistica Neerlandica**, v. 36, n. 3, p. 109-118, 1982.

MATOS, R. M.; AMARO, N.; POLLARD, R. How best to quantify home advantage in team sports. **RICYDE**, v. 16, n. 59, p. 12-23, 2020.

NEVILL, A. M.; BALMER, N. J.; WILLIAMS, A. M. The influence of crowd noise and experience upon refereeing decisions in football. **Psychology of Sport and Exercise**, v. 3, n. 4, p. 261-272, 2002.

NEVILL, A. M.; HOLDER, R. L. Home advantage in sport: an overview of studies on the advantage of playing at home. **Sports Medicine**, v. 28, n. 4, p. 221-236, 1999.

OPENFOOTBALL. **South America: Brazil**. 2026. Disponível em: https://github.com/openfootball/south-america. Acesso em: 20 nov. 2026.

POLLARD, R. Home advantage in soccer: a retrospective analysis. **Journal of Sports Sciences**, v. 4, n. 3, p. 237-248, 1986.

POLLARD, R.; SILVA, C. D.; MEDEIROS, N. C. Home advantage in football in Brazil: differences between teams and the effects of distance traveled. **Brazilian Journal of Soccer Science**, v. 1, n. 1, p. 3-10, 2008.

SCOPPA, V. Social pressure in the stadiums: do agents change behavior without crowd support? **Journal of Economic Psychology**, v. 82, 102344, 2021.

SILVA, C. D.; MOREIRA, D. G. A vantagem em casa no futebol: comparação entre o Campeonato Brasileiro e as principais ligas nacionais do mundo. **Revista Brasileira de Cineantropometria e Desempenho Humano**, v. 10, n. 2, p. 184-188, 2008.

SUTTER, M.; KOCHER, M. G. Favoritism of agents: the case of referees' home bias. **Journal of Economic Behavior & Organization**, v. 53, n. 4, p. 461-469, 2004.
