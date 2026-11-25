# Guia de estudo para a banca — Artigo 2013–2024

**Artigo:** *Vantagem de jogar em casa na Série A: uma análise baseada em modelos de 12 temporadas (2013–2024)*
**Aluno:** José Inamar de Medeiros Júnior
**Orientador:** Prof. Dr. Francisco Marcio Barboza

> **Como usar este guia.** Leia primeiro a folha de resumo (seção 0). Depois estude os métodos com lápis na mão (seção 3), confira os resultados (seção 4) e treine as respostas (seção 7). No fim, use os roteiros de 5 e 15 minutos (seção 8) e o checklist (seção 12). A meta não é decorar: é conseguir explicar **por que** cada número existe e **o que ele não prova**.

---

## 0. Folha de resumo — os números que você não pode errar

| Conceito | Número/frase |
|---|---|
| Base principal | **4.559 partidas**, 12 temporadas, 2013–2024, `BrazilianFootball/Data` (MIT) |
| Cobertura | 380 jogos por temporada; **2016 tem 379** (Chapecoense × Atlético-MG cancelado) |
| Validação | **2.658 de 2.660** placares idênticos ao OpenFootball (**99,92%**) |
| Campeões | **12/12** conferidos |
| Pollard geral | **63,0%** (IC 95% **61,7–64,3**) |
| Resultados | 48,4% vitórias do mandante, 26,9% empates, 24,7% vitórias do visitante |
| Gols | 1,41 do mandante × 0,96 do visitante por jogo |
| Regime pré-2019 | **65,0%** (2013–2018) |
| Regime pós-2019 | **61,0%** (2019–2024) |
| Mudança | **−4,0 p.p.**; IC bootstrap por cluster **−6,6 a −0,9** (ou 0,9–6,6 na direção pré − pós) |
| Quebra | **2019** (mínimos quadrados; 12 observações anuais) |
| 2020 | **60,2%** sem torcida |
| 2022–2024 | **60,6%** com público de volta |
| Poisson, antes | prêmio de **+56,5%** (log 0,448; EP 0,026; IC 0,397–0,500) |
| Poisson, depois | prêmio de **+37,7%** (log 0,320; EP 0,026; IC 0,270–0,371) |
| Interação | **−0,128** (EP 0,037; IC −0,200 a −0,056; p < 0,001) |
| Multiplicador | **1,565 → 1,377**; queda relativa de **12,0%** |
| Prêmio em p.p. | **18,8 p.p.**; redução relativa de **33,3%** |
| ICC | **2,2%** da variância entre equipes; **97,8%** dentro de equipes/temporadas |
| Público | ρ = **0,08** com vantagem de casa; ρ = **0,41** com pontos |
| Cartões | DiD **+0,35** (EP 0,190; IC −0,03 a +0,72; n = 760) |
| Pênaltis | DiD **+0,05** (EP 0,052; IC −0,06 a +0,15; n = 760) |
| Testes | **117** passando |
| Auditoria de dados | **150 verificações, 0 falhas** |
| Artigo | EN 9 p.; PT 10 p.; ABNT 16 p.; pacote completo 19 p. |

**Frase de abertura (30 segundos):**
“O artigo mede a vantagem de jogar em casa na Série A entre 2013 e 2024, com 4.559 partidas de uma base MIT validada contra o OpenFootball. O mandante somou 63,0% dos pontos, mas a vantagem caiu de 65,0% para 61,0% depois de 2019. A queda aparece também em gols, sobrevive ao controle de ataque, defesa e temporada, e não é explicada por um único canal. O desenho é observacional; não afirmo causalidade.”

**Frase de fechamento (30 segundos):**
“A contribuição é descritiva e reprodutível: uma série de 12 temporadas, um modelo formal de mudança e um Poisson de ataque–defesa. O resultado central é que a vantagem é grande, mas não constante, e que o referencial pós-2019 é 61,0%, não 65,0%. A causa da queda segue em aberto.”

---

## 1. O problema e a pergunta

### 1.1 O que é vantagem de jogar em casa

É a tendência sistemática de equipes se saírem melhor em casa do que fora, controlando qualidade do time e contexto. No futebol, ela aparece em pontos, gols, vitórias e decisões de arbitragem. Não é “o mandante sempre ganha”: é uma assimetria média.

### 1.2 Por que a Série A é um bom laboratório

1. **Ponto corrido de ida e volta**, com 20 clubes e 38 rodadas: cada equipe joga uma vez em casa e uma fora contra cada adversário.
2. **Dimensão territorial**: viagens longas, diferenças regionais e estádios heterogêneos.
3. **Choques em janela curta**: VAR em 2019; pandemia em 2020–2021; retorno gradual da torcida.
4. **Lacuna na literatura brasileira**: muitos estudos descritivos, poucos modelos formais que separem qualidade das equipes do efeito de casa.

### 1.3 A pergunta

O artigo responde a três perguntas:

1. **Qual foi a magnitude** da vantagem de jogar em casa entre 2013 e 2024?
2. **Ela mudou depois de 2018**, e quando?
3. **Quais canais** são compatíveis com o padrão observado?

O desenho é **descritivo e observacional**. Não é um experimento, não é um modelo causal e não é um modelo de previsão de placar.

### 1.4 A contribuição

- Série de **12 temporadas** construída sobre base aberta e reprodutível.
- **Mudança de nível** estimada formalmente, com IC por cluster de temporada.
- **Poisson ataque–defesa** que separa qualidade das equipes do efeito de casa.
- **Decomposição de variância** mostrando que a vantagem é predominantemente da liga, não um traço estável de clube.
- Evidência **multi-canal**: público, cartões e pênaltis, com limites explícitos.

---

## 2. Dados

### 2.1 Fonte e recorte

- Fonte principal: `BrazilianFootball/Data`, licença MIT, commit `0dd1bc5`.
- Recorte: **2013–2024**, 12 temporadas, **4.559 partidas**.
- O recorte começa em 2013 porque os borderôs eletrônicos da CBF começam nesse ano e a base MIT cobre 2013 em diante. Temporadas anteriores exigiriam outra fonte e estão fora do escopo.
- A base bruta **não é redistribuída**; o pipeline reconstrói o recorte a partir do commit fixado.

### 2.2 Cobertura e limpeza

- 380 partidas por temporada, exceto **2016 (379)**: Chapecoense × Atlético-MG foi cancelado após o acidente aéreo.
- A temporada **2020** vai de 8 de agosto de 2020 a 25 de fevereiro de 2021 por causa da pandemia.
- A base contém resultados, gols, estádios, cartões e gols de pênalti marcados com `PN`.
- **Público**: 4.555 de 4.559 partidas (99,9%).
- **Árbitro**: 4.541 partidas (99,6%).
- **Cartões**: todas as 4.559 partidas; um cartão não atribuído em 2022 (registro malformado).
- **Público zero**: 628 registros; **598 são reais** (380 em 2020 e 218 em 2021); **30 são zeros esparsos** em outras temporadas, mantidos como registros, mas podem conter falhas.
- **2024**: público complementado pelo FBref (90 partidas).

### 2.3 Validação

- Comparação com **OpenFootball (CC0)** para 2018–2024.
- **2.658 de 2.660** placares idênticos: **99,92%**.
- **Uma divergência de placar**: 08/12/2019, Internacional × Atlético-MG. A base MIT registra **0–0**; as fontes oficiais registram **2–1 para o Internacional**. O artigo documenta a divergência em vez de alterar a fonte bruta.
- **Uma exceção de data**: Botafogo-RJ × Athletico-PR, 2023, jogo de dois dias (21 e 22/10), 1–1. A base registra 22/10; o OpenFootball, 21/10.
- **12/12 campeões** recalculados, incluindo Botafogo-RJ em 2024.
- Impacto da divergência de placar: 1 partida em 4.559 (0,02%); Pollard e Poisson permanecem iguais no arredondamento; o ICC passaria de 2,2% para 2,3% se a base fosse corrigida. As conclusões qualitativas não mudam.

### 2.4 O que a base não tem

- Não observa **Copa do Brasil, Libertadores ou Sul-Americana**. A congestão de outras competições não é identificada; a diferença de descanso é uma proxy imperfeita.
- Não tem **pênaltis marcados/perdidos**: só gols de pênalti convertidos (`PN`).
- Não tem **faltas por árbitro** nem tipos de cartão por decisão.
- Não tem **xG, odds, lesões, altitude ou clima**.
- Não é uma base de **Séries B–D nem futebol feminino**.

---

## 3. Métodos

### 3.1 Índice de Pollard

O índice mede a parcela dos pontos que ficou com o mandante:

```text
Pollard = 100 × P_H / (P_H + P_A)
```

- `P_H`: pontos totais do mandante.
- `P_A`: pontos totais do visitante.
- **50%** é neutralidade; acima de 50% indica vantagem de casa.
- No artigo: **63,0%**, ou 13,0 p.p. acima de 50%.
- O índice é descritivo e agrega vitórias e empates. Não é probabilidade de vitória.

### 3.2 Bootstrap e intervalos de confiança

- **IC geral**: bootstrap de partidas, 4.000 reamostragens, intervalo percentil 2,5%–97,5%.
- **ICs anuais**: mesmo procedimento por temporada; são descritivos e não corrigem a dependência entre partidas das mesmas equipes.
- **Diferença pré/pós**: **bootstrap por cluster de temporada** (5.000 reamostragens). Reamostra temporadas inteiras dentro de cada período, preservando a dependência entre partidas da mesma temporada.
- **Por que cluster?** Porque a unidade de variação do corte é a temporada, não a partida. Reamostrar partidas soltas subestimaria a incerteza da mudança de nível.
- O IC da diferença é **0,9–6,6** na direção pré − pós; equivalentemente, **−6,6 a −0,9** na direção pós − pré.

### 3.3 Modelo de mudança de nível

```text
y_t = α + β·1(t ≥ τ) + ε_t
```

- `y_t`: Pollard da temporada `t`.
- `τ`: ano de quebra candidato.
- `β`: mudança de nível depois da quebra.
- O artigo estima `τ` por **mínimos quadrados**, testando cortes com pelo menos **três temporadas de cada lado**.
- O corte que minimiza a soma dos quadrados dos resíduos é **2019**.
- Médias: **64,978%** antes; **60,985%** depois; diferença **3,993 p.p.**
- Com 12 observações anuais, o ano exato é impreciso; o objeto robusto é a **diferença entre as médias**, não a data.
- 2019 coincide com o VAR; 2020 com a pandemia. O modelo **não identifica a causa**.

### 3.4 Modelo de Poisson ataque–defesa

Para cada partida, os dois placares são tratados como contagens:

```text
gols_casa ~ Poisson(λ_casa)
gols_fora ~ Poisson(λ_fora)

log λ_casa = μ + a_i − d_j + γ + δ·1(t ≥ 2019) + θ_t
log λ_fora = μ + a_j − d_i + θ_t
```

- `a_i`: ataque da equipe `i`.
- `d_j`: defesa da equipe `j`; entra com sinal negativo porque defesa melhor reduz o λ do adversário.
- `γ`: vantagem de casa antes de 2019.
- `δ`: mudança da vantagem de casa depois de 2019.
- `θ_t`: efeito fixo de temporada.
- **Identificação**: o modelo usa uma equipe de referência com ataque e defesa iguais a zero. Os demais parâmetros são relativos a ela. Também seria possível impor `Σ a_i = Σ d_i = 0`.
- **Estimação**: máxima verossimilhança poissoniana via IRLS (mínimos quadrados reponderados iterativamente).
- **Erros-padrão**: cluster-robustos por partida, porque os dois placares da mesma partida são correlacionados.
- **Dispersão de Pearson**: 0,925; próxima de 1, sem evidência de superdispersão.
- **Dimensão**: 4.559 partidas, 9.118 observações de gols, 84 parâmetros.
- **Por que 84?** 36 equipes × 2 parâmetros = 72; menos 2 da equipe de referência = 70; mais intercepto, casa, interação e 11 dummies de temporada = 84.

**Interpretação dos coeficientes:**

- `exp(γ) − 1 = +56,5%`: antes de 2019, o mandante marcava 56,5% mais gols que o visitante, controlando ataque, defesa e temporada.
- `exp(γ + δ) − 1 = +37,7%`: depois de 2019.
- `exp(δ) − 1 = −12,0%`: o multiplicador de gols do mandante caiu 12,0%.
- O prêmio em pontos percentuais caiu **18,8 p.p.** (56,5 − 37,7), uma redução relativa de **33,3%**.
- **Não diga** “o mandante marca 12% menos gols”: a queda de 12,0% é no **multiplicador relativo**, não no total de gols.

### 3.5 Decomposição de variância e ICC

Modelo one-way para a vantagem por equipe-temporada:

```text
HA_it = μ + u_i + e_it
```

- `u_i`: efeito de equipe.
- `e_it`: resíduo equipe-temporada.
- `ICC = σ²_u / (σ²_u + σ²_e)`: parcela da variância que está **entre equipes**.
- Resultado: **ICC = 0,0223** (2,2%); variância entre 0,0039; dentro 0,1702; **97,8%** dentro.
- n = 240 equipe-temporadas; 36 clubes.
- O ICC é uma decomposição descritiva; **não estima parâmetros por clube** e não autoriza ranking de clubes.
- A leitura correta: o componente entre clubes é pequeno; a maior parte é variação equipe-temporada (mistura de diferenças persistentes dentro da equipe e ruído).

### 3.6 Diferenças-em-diferenças para cartões e pênaltis

Para cartões:

```text
yellow_diff_m = β_0 + β_1·Post2020_m + α_casa + α_fora + ε_m
```

- `yellow_diff = amarelos_casa − amarelos_fora`.
- `Post2020 = 1` para 2020.
- `α_casa`, `α_fora`: efeitos fixos de equipe.
- `β_1`: DiD; compara a diferença casa−fora em 2020 com a de 2019, absorvendo diferenças invariantes no tempo entre equipes.
- Erros-padrão: cluster unidirecional por mandante e por visitante; o artigo usa o **maior** dos dois, uma aproximação prática que evita variâncias negativas da covariância two-way. Não é garantia formal de covariância two-way.
- Resultado: **+0,35** (EP 0,190; IC −0,03 a +0,72; n = 760). Times comuns em 2019 e 2020: +0,34 (IC −0,04 a +0,72; n = 480).
- O IC inclui zero; a leitura é **sugestiva, não conclusiva**.

Para pênaltis, o mesmo desenho com `pen_diff` (gols de pênalti convertidos):

- Resultado: **+0,05** (EP 0,052; IC −0,06 a +0,15; n = 760).
- Times comuns: +0,05 (IC −0,05 a +0,15).
- **Limite**: só observamos pênaltis convertidos (`PN`); não observamos pênaltis marcados/perdidos. O denominador não existe.

### 3.7 Spearman e contexto

- **Spearman** mede correlação monotônica entre ranks; não exige normalidade e é robusta a outliers.
- Público × vantagem de casa: **ρ = 0,08** (fraca).
- Público × pontos: **ρ = 0,41** (forte/moderada).
- Excluindo os 30 zeros esparsos: **0,08 e 0,39**.
- Contexto: distância, clássico, estádio habitual e força pré-jogo. Tudo descritivo; sem identificação causal.

### 3.8 Reprodutibilidade

- `scripts/build_mit_base.py`: constrói a base 2013–2024.
- `scripts/analyze_artigo.py`: Pollard, ICs, quebra, contexto e Figura 1.
- `scripts/analyze_models.py`: Poisson e decomposição de variância.
- `scripts/analyze_cards.py`: cartões e pênaltis.
- `scripts/validate_champions.py --base data/processed/matches_processed_2013_2024.csv`: 12/12 campeões.
- `scripts/build_artigo.py`, `build_artigo_abnt.py`, `build_capa_artigo.py`: PDFs.
- `scripts/build_deck_artigo.py`, `build_deck_banca.py`, `make_deck_figures.py`: apresentações.
- 117 testes; auditoria de dados com 150 verificações.

---

## 4. Resultados

### 4.1 Nível e mudança

- Pollard geral: **63,0%** (IC 61,7–64,3).
- Mandante venceu **48,4%**; empates **26,9%**; visitante **24,7%**.
- Gols: **1,41** do mandante × **0,96** do visitante.
- Série anual: mínimo **58,2%** (2017), máximo **69,5%** (2018).
- Pré-2019: **65,0%**; pós-2019: **61,0%**; diferença **4,0 p.p.** (IC 0,9–6,6).
- Quebra estimada: **2019**.
- 2020: **60,2%**; 2022–2024: **60,6%**.
- **Leitura**: a vantagem é grande, mas não é constante; o retorno da torcida não restaurou o patamar anterior.

### 4.2 Gols

- Antes: **+56,5%** (log 0,448; EP 0,026; IC 0,397–0,500).
- Depois: **+37,7%** (log 0,320; EP 0,026; IC 0,270–0,371).
- Interação: **−0,128** (EP 0,037; IC −0,200 a −0,056; p < 0,001).
- Multiplicador: **1,565 → 1,377**; **−12,0%**.
- Prêmio: **18,8 p.p.**; **33,3%** de redução relativa.
- **Leitura**: a queda não é só no índice; aparece no espaço de gols e sobrevive ao controle de ataque, defesa e temporada.

### 4.3 Equipes

- ICC **2,2%**; 97,8% da variação é equipe-temporada.
- **Leitura**: a vantagem é predominantemente um fenômeno da liga; não é um traço permanente de clube. Rankings de “quem tem mais vantagem em casa” são instáveis com 12 temporadas.

### 4.4 Público

- ρ = **0,08** com a vantagem de casa; ρ = **0,41** com pontos.
- 2020: **60,2%**; 2022–2024: **60,6%**.
- **Leitura**: o público separa clubes grandes de pequenos, mas não explica a vantagem dentro do mesmo clube. A torcida é um canal entre vários; 2020 também mudou calendário e protocolos.

### 4.5 Cartões e pênaltis

- Cartões: 2019 mandante recebia **0,18 amarelo a menos**; 2020, **+0,11**; DiD **+0,35** (IC −0,03 a +0,72).
- Pênaltis convertidos: **+0,05** (IC −0,06 a +0,15).
- **Leitura**: cartões vão na direção esperada, mas o IC inclui zero; pênaltis não mostram mudança detectável. Nenhum dos dois prova viés arbitral.

### 4.6 Contexto

- Distância: **63,7%** (<500 km), **62,9%** (500–1.499 km), **62,0%** (≥1.500 km); gradiente raso, ICs se sobrepõem.
- Clássico: **59,1%** vs. **63,2%** não clássico.
- Estádio habitual: **63,3%** vs. **60,7%** outro estádio.
- Força pré-jogo: **73,3%** favorito, **62,1%** equilibrado, **54,2%** azarão.
- **Leitura**: os contrastes são modestos; o gradiente mais forte é a força pré-jogo. Distância/viagem não explicam a vantagem sozinhas.

---

## 5. Interpretação e limites

### 5.1 O que você pode concluir

- A vantagem de casa foi **grande** no período: 63,0% dos pontos.
- Ela **caiu** de 65,0% para 61,0% no período pós-2019.
- A queda é **robusta em gols** e não é composição de equipes/temporadas.
- A vantagem é **predominantemente da liga**, não um traço estável de clube.
- O público é **canal fraco**; cartões são **sugestivos**; pênaltis são **nulos** no piloto.
- O referencial prático pós-2019 é **61,0%** (60,6% em 2022–24).

### 5.2 O que você não pode concluir

- Que o VAR **causou** a queda.
- Que a torcida **causou** a queda.
- Que a arbitragem **causou** a queda.
- Que 2019 é uma data causal exata.
- Que um clube específico tem vantagem permanente.
- Que 2025 repetirá 61,0% sem teste fora da amostra.
- Que times que viajam mais são piores **por causa** da viagem.
- Que pênaltis/cartões provam viés arbitral.

### 5.3 Canais confundidos

- **2019**: VAR.
- **2020–2021**: pandemia, jogos sem torcida, calendário comprimido, protocolos.
- **Retorno da torcida**: 2022–2024, mas com mudanças de calendário e protocolos.
- **Arbitragem**: cartões refletem decisões e comportamento dos jogadores.
- **Público**: endógeno (adversário, fase, preço, clima, expectativa).

### 5.4 Viés e endogeneidade

- **Seleção**: clubes que disputam Libertadores são mais fortes e têm elencos maiores; comparar clubes é confundido.
- **Priorização**: clubes podem poupar titulares em uma competição.
- **Público**: não é atribuído aleatoriamente.
- **Arbitragem**: identidade do árbitro não é decisão; cartões não são “tratamento”.
- **Recorte**: Série A apenas; outras competições não observadas.
- **Medida**: pênaltis só convertidos; sem denominador.

---

## 6. Literatura e posicionamento

### 6.1 Quatro frentes

1. **Vantagem de casa no esporte**: Pollard (1986); Nevill & Holder (1999).
2. **Brasil**: Silva & Moreira (2008); Pollard, Silva & Medeiros (2008).
3. **Modelos de placar**: Maher (1982); Dixon & Coles (1997).
4. **Jogos sem torcida**: Bryson et al. (2021); Fischer & Haucap (2021); Endrich & Gesche (2020); Scoppa (2021).

### 6.2 O que o artigo adiciona

- 12 temporadas com base aberta e validação explícita.
- Mudança de nível formal, com IC por cluster.
- Poisson ataque–defesa com interação casa × pós-2019.
- Decomposição de variância mostrando que a vantagem é da liga.
- Evidência multi-canal com limites claros.
- Reprodutibilidade: scripts, testes e base reconstruível.

### 6.3 A lacuna

A literatura brasileira é majoritariamente descritiva, com amostras curtas ou comparações agregadas. Faltam modelos que separem qualidade das equipes do efeito de casa e que testem a estabilidade temporal com choques brasileiros (VAR, pandemia, retorno da torcida).

---

## 7. Perguntas prováveis da banca (com respostas)

### 7.1 Escopo e dados

**1. Por que 2013–2024?**
Porque os borderôs eletrônicos da CBF começam em 2013 e a base MIT cobre 2013 em diante. Antes disso, a fonte seria outra e o recorte deixaria de ser reproduzível com o mesmo pipeline.

**2. Por que não incluir 2006–2012?**
Mudaria a fonte, o esforço de validação e o escopo. O artigo foi desenhado para uma base aberta e homogênea; 2013–2024 já tem 12 temporadas e dois choques relevantes.

**3. Quantas partidas? Por que não 4.560?**
4.559. São 12 × 380 = 4.560, menos uma: 2016 tem 379 porque Chapecoense × Atlético-MG foi cancelado após o acidente aéreo.

**4. A base é confiável?**
Sim, com limites documentados: 2.658/2.660 placares idênticos ao OpenFootball (99,92%), 12/12 campeões, uma divergência de placar e uma exceção de data. A divergência de 2019 é conhecida e quantificada.

**5. O que é o `PN`?**
É a marcação de gol de pênalti convertido no JSON. O artigo usa `PN` para o piloto de pênaltis, mas não observa pênaltis marcados/perdidos.

**6. O público é confiável?**
É uma proxy. Vem da Base dos Dados/Transfermarkt, com 2024 complementado pelo FBref. Pode misturar pagante e total; é endógeno. Usamos só nas análises descritivas.

**7. Quantos zeros de público?**
628; 598 reais (380 em 2020, 218 em 2021) e 30 esparsos em outras temporadas, mantidos como registros, mas podem conter falhas.

**8. Por que não usar só vitórias?**
Porque o Pollard usa pontos e incorpora empates. A proporção de vitórias é 48,4%; o Pollard é 63,0% dos pontos. São medidas diferentes.

### 7.2 Métodos

**9. O que é o índice de Pollard?**
`100 × pontos do mandante / (pontos do mandante + pontos do visitante)`. 50% é neutralidade; acima disso, vantagem de casa.

**10. Por que bootstrap?**
Porque não queremos depender de normalidade e queremos uma incerteza descritiva. Reamostramos partidas para o IC geral e temporadas inteiras para a diferença pré/pós.

**11. Por que cluster de temporada na mudança?**
Porque a unidade do corte é a temporada. Reamostrar partidas soltas ignoraria a dependência dentro da temporada e subestimaria a incerteza.

**12. Como você estimou a quebra?**
Grid search de `τ` no modelo segmentado, com pelo menos três temporadas de cada lado, minimizando a soma dos quadrados dos resíduos. O mínimo é 2019.

**13. Por que 2019 e não 2020?**
Porque 2019 minimiza o SSE. Mas o ano é impreciso com 12 observações; o objeto robusto é a diferença de médias, não a data. 2019 também coincide com o VAR, o que impede atribuição causal.

**14. Por que Poisson?**
Porque gols são contagens; o modelo log-linear permite separar ataque, defesa, temporada e efeito de casa, com parâmetros interpretáveis.

**15. Como você identifica ataque e defesa?**
Com uma equipe de referência (ataque e defesa zero). Os parâmetros são relativos; também seria possível impor soma zero. Os valores absolutos não têm significado.

**16. O que significa `exp(γ) − 1`?**
É o efeito multiplicativo da vantagem de casa. `γ = 0,448` → `exp(0,448) = 1,565` → +56,5%.

**17. Por que não negative binomial?**
A dispersão de Pearson foi 0,925, próxima de 1; não há evidência de superdispersão. Negative binomial ou quasi-Poisson seriam alternativas se a dispersão fosse maior.

**18. Por que não Dixon–Coles?**
O foco é o parâmetro de vantagem de casa, não a previsão exata de placar. A correção de placares baixos poderia ser explorada, mas não é necessária para a conclusão central.

**19. O que é ICC?**
A parcela da variância da vantagem por equipe-temporada que está entre equipes: `σ²_u/(σ²_u+σ²_e)`. No artigo, 2,2%.

**20. O ICC 2,2% significa que 2,2% dos clubes têm vantagem?**
Não. É 2,2% da **variância**, não dos clubes. A maior parte (97,8%) é variação equipe-temporada.

**21. O que é DiD?**
Diferenças-em-diferenças: compara a mudança de um grupo tratado com a mudança de um grupo de comparação. Aqui, 2020 vs. 2019, com efeitos fixos de equipe. É descritivo, não causal.

**22. Por que o erro-padrão dos cartões é “conservador”?**
Porque calculamos cluster por mandante e por visitante e tomamos o maior. É uma aproximação prática; não é garantia formal de covariância two-way.

### 7.3 Resultados

**23. Qual é o número principal?**
63,0% dos pontos para o mandante (IC 61,7–64,3), mas com queda para 61,0% no período pós-2019.

**24. A queda é grande?**
4,0 p.p. no Pollard; 12,0% no multiplicador de gols. É material, mas não catastrófica. O IC da diferença (0,9–6,6) exclui zero.

**25. A queda é só no índice?**
Não. O Poisson mostra queda no espaço de gols, controlando ataque, defesa e temporada.

**26. A queda é composição de equipes?**
Não. O modelo de Poisson com ataque/defesa e efeitos de temporada continua mostrando a interação negativa.

**27. O que aconteceu em 2020?**
O Pollard foi 60,2% sem torcida. Em 2022–2024, com público de volta, 60,6%. O retorno não restaurou o patamar pré-2019.

**28. O público explica a vantagem?**
Não sozinho. ρ = 0,08 com a vantagem; ρ = 0,41 com pontos. O público separa clubes grandes de pequenos, mas não explica a vantagem dentro do clube.

**29. Os cartões mostram viés?**
Sugerem, mas não provam. O DiD é +0,35, com IC incluindo zero; 2020 mistura pandemia, calendário e protocolos.

**30. E os pênaltis?**
+0,05, IC −0,06 a +0,15; sem mudança detectável. Só observamos convertidos, não marcados/perdidos.

**31. Qual é a conclusão sobre heterogeneidade?**
A vantagem é predominantemente da liga; o componente entre clubes é pequeno (2,2%). Não há evidência de traços persistentes fortes por clube.

**32. Qual é o benchmark pós-2019?**
61,0% (60,6% em 2022–24). Não use 65,0% para previsão ou análise do período atual.

### 7.4 Causalidade e limitações

**33. Você pode afirmar que o VAR causou a queda?**
Não. 2019 coincide com o VAR, mas também com outros cambios; o desenho é observacional e não isola o VAR.

**34. Você pode afirmar que a torcida causou a queda?**
Não. 2020 muda torcida, calendário, protocolos e ambiente. O retorno da torcida não restaura o padrão, o que sugere que a torcida não é a história toda.

**35. O que você não consegue separar?**
VAR, pandemia, calendário, retorno da torcida, arbitragem e mudanças de qualidade/estilo. O artigo trata isso como limitação, não como identificação.

**36. Qual é a maior limitação?**
O desenho observacional e a confusão dos choques de 2019–2021. Além disso, a base cobre apenas Série A e não observa outras competições.

**37. O que você faria com mais dados?**
2025 fora da amostra; calendário de Copa/Libertadores; odds/xG; modelo hierárquico bayesiano; Séries B–D e futebol feminino.

**38. O que você não faria?**
Não usaria machine learning caixa-preta para prever placar; não trataria 2019 como causa; não ranquearia clubes sem encolhimento; não afirmaria causalidade.

### 7.5 “Pegadinhas” comuns

**39. “A vantagem caiu 12%?”**
Cuidado: 12,0% é a queda relativa do **multiplicador de gols**. No Pollard, a queda é 4,0 p.p. (65,0 → 61,0).

**40. “O mandante vence 63%?”**
Não. O mandante vence 48,4%; 63,0% é a parcela dos **pontos**.

**41. “O ICC é 53,5%?”**
Não. O valor correto é **2,2%**. O 53,5% era um erro antigo, corrigido no artigo.

**42. “Pênaltis +0,05 é significativo?”**
Não. O IC inclui zero; o resultado é nulo/indetectável, não “prova de ausência”.

**43. “Cartões +0,35 é significativo?”**
Não. O IC inclui zero; é sugestivo, não conclusivo.

**44. “Times que viajam mais são piores por causa da viagem?”**
A associação descritiva existe, mas é confundida com região, qualidade e calendário. Não é causal. A distância no nível da partida tem gradiente raso (63,7/62,9/62,0) e ICs sobrepostos.

**45. “A quebra em 2019 prova o VAR?”**
Não. O ano é estimado, impreciso, e coincide com outros choques. A diferença pré/pós é o objeto robusto.

---

## 8. Roteiros de fala

### 8.1 Versão de 5 minutos (6 slides)

1. **Capa (20 s).** “O artigo mede a vantagem de jogar em casa na Série A entre 2013 e 2024, com 4.559 partidas de uma base MIT validada.”
2. **Pergunta e base (50 s).** “Três perguntas: magnitude, mudança e canais. A base tem 12 temporadas, 99,92% de placares idênticos e 12/12 campeões.”
3. **Nível (60 s).** “O mandante somou 63,0% dos pontos, mas caiu de 65,0% para 61,0% depois de 2019. A quebra é estimada em 2019; o IC da diferença é 0,9–6,6.”
4. **Gols (60 s).** “O Poisson confirma: o prêmio de gols caiu de +56,5% para +37,7%; o multiplicador caiu 12,0%, controlando ataque, defesa e temporada.”
5. **Equipes e canais (60 s).** “O ICC é 2,2%: a vantagem é da liga, não de um clube. O público tem ρ = 0,08 com a vantagem e 0,41 com pontos; cartões são sugestivos; pênaltis são nulos.”
6. **Conclusão (40 s).** “A vantagem é grande, mas não constante. A queda é robusta em gols; a causa segue em aberto. O benchmark pós-2019 é 61,0%.”

### 8.2 Versão de 15 minutos (11 slides)

1. **Capa (30 s).** Contexto e objetivo.
2. **Literatura (90 s).** Quatro frentes e a lacuna.
3. **Pergunta (60 s).** As três perguntas e o desenho observacional.
4. **Dados (90 s).** Fonte, cobertura, validação e limites.
5. **Métodos (120 s).** Pollard, mudança, Poisson, ICC; explicar identificação.
6. **Resultado 1 (120 s).** 63,0%; 65→61; −4,0 p.p.; IC.
7. **Resultado 2 (120 s).** +56,5→+37,7; −12,0%; prêmio 18,8 p.p.
8. **Resultado 3 (90 s).** ICC 2,2%; público 0,08/0,41; 2020/2022–24.
9. **Canais (90 s).** Cartões +0,35; pênaltis +0,05; confundimento.
10. **Contribuições/limitações (90 s).** O que entrega e o que não entrega.
11. **Conclusão (60 s).** 61,0% de benchmark; obrigado.

---

## 9. Glossário

- **Ataque (`a_i`)**: efeito log-multiplicativo da capacidade ofensiva da equipe.
- **Defesa (`d_j`)**: efeito log-multiplicativo da qualidade defensiva; sinal negativo no λ do adversário.
- **Bootstrap**: reamostragem com reposição para estimar incerteza.
- **Cluster**: grupo de observações correlacionadas; aqui, temporada ou partida.
- **DiD**: diferenças-em-diferenças.
- **Dispersão de Pearson**: estatística de ajuste do Poisson; ~1 é compatível com variância igual à média.
- **Efeito fixo**: intercepto específico de equipe/temporada.
- **ICC**: correlação intraclasse; parcela da variância entre grupos.
- **IRLS**: mínimos quadrados reponderados iterativamente; estimação de GLM.
- **Log link**: `log λ = Xβ`; efeitos multiplicativos.
- **Pollard**: índice de pontos do mandante sobre o total.
- **Proxy**: medida indireta de um conceito.
- **Spearman**: correlação de ranks.
- **Superdispersão**: variância maior que a média.
- **Variável endógena**: determinada dentro do sistema; público, por exemplo.

---

## 10. Fórmulas e notação

```text
Pollard = 100 × P_H / (P_H + P_A)

y_t = α + β·1(t ≥ τ) + ε_t

gols_casa ~ Poisson(λ_casa)
gols_fora ~ Poisson(λ_fora)

log λ_casa = μ + a_i − d_j + γ + δ·1(t ≥ 2019) + θ_t
log λ_fora = μ + a_j − d_i + θ_t

HA_it = μ + u_i + e_it
ICC = σ²_u / (σ²_u + σ²_e)

yellow_diff_m = β_0 + β_1·Post2020_m + α_casa + α_fora + ε_m
```

---

## 11. Plano de estudo de 7 dias

| Dia | Foco | Meta |
|---|---|---|
| 1 | Seções 0–2 | Explicar o problema, a base e a validação sem olhar |
| 2 | Seção 3.1–3.4 | Derivar Pollard, mudança e Poisson; explicar identificação |
| 3 | Seção 3.5–3.8 | Explicar ICC, DiD, Spearman e reprodutibilidade |
| 4 | Seção 4 | Reproduzir a tabela de números e interpretar cada um |
| 5 | Seção 7 | Responder 20 perguntas em voz alta, sem ler |
| 6 | Seções 5–6 | Limitações, causalidade e literatura |
| 7 | Seções 8 e 12 | Simular 5 e 15 minutos; checklist final |

---

## 12. Checklist final

- [ ] Sei explicar o que é a vantagem de casa e por que 50% é neutralidade.
- [ ] Sei recitar os 12 números principais sem olhar.
- [ ] Sei derivar o Pollard e o Poisson em uma folha.
- [ ] Sei explicar por que o Poisson separa qualidade do efeito de casa.
- [ ] Sei explicar a identificação por equipe de referência.
- [ ] Sei explicar o ICC 2,2% e o que ele **não** significa.
- [ ] Sei explicar a diferença entre 4,0 p.p. e 12,0%.
- [ ] Sei explicar por que 2019 não é causa.
- [ ] Sei explicar o que o público e os cartões mostram — e não mostram.
- [ ] Sei listar as limitações sem hesitar.
- [ ] Sei apresentar em 5 e em 15 minutos.
- [ ] Sei dizer “não sei” quando a pergunta estiver fora do escopo, e propor como testar.
