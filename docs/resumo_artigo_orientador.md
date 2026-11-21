# Resumo para o Professor Barboza — proposta de artigo

Professor Barboza,

Preparei este resumo curto para o senhor avaliar se o trabalho pode virar um artigo de 8 a 10 páginas, em vez da monografia extensa. Como o senhor vem da matemática e me deu aula de Álgebra Linear, organizei o texto pelo que os dados permitem **modelar e testar**, e não apenas pelo que o dashboard mostra.

Depois da nossa conversa sobre o formato, ajustei o recorte para **2013–2024**. É o período em que os borderôs eletrônicos da CBF existem e em que o `BrazilianFootball/Data` (MIT) oferece resultados, gols, estádios e cartões de forma aberta. Isso permite publicar o núcleo do dashboard e reproduzir o artigo a partir de dados abertos. A Figura 2 e as extensões de público/arbitragem usam a base externa (Base dos Dados/Transfermarkt), com termos próprios; o bruto da CBF não é redistribuído.

## A pergunta

Qual foi a magnitude da vantagem de jogar em casa no Campeonato Brasileiro Série A entre 2013 e 2024, como ela variou entre temporadas e clubes, e quais fatores contextuais estão associados a essa variação. O estudo é descritivo e observacional: não testa causalidade nem faz previsão de resultados.

## O que eu já fiz

- **Base principal:** 4.559 partidas válidas, 12 temporadas (2013–2024), extraídas do `BrazilianFootball/Data` (MIT), com regras de limpeza documentadas e verificação de integridade.
- **Validação:** 2.658 de 2.660 placares idênticos ao OpenFootball (99,92%); uma divergência de placar e uma exceção de data documentadas; **12/12 campeões** recalculados. Relatório: `docs/validacao_cruzada_2013_2024.md`.
- **Indicador central:** índice de Pollard, que mede o percentual de pontos conquistados pelo mandante sobre o total de pontos em disputa. Em 63,0%, o mandante fica 13,0 pontos percentuais acima da neutralidade.
- **Métodos:** intervalo por bootstrap, mudança de nível, matriz de correlação de Spearman, análise de contexto e diferença-em-diferenças para o contraste 2019→2020.
- **Extensões:** público e arbitragem (2013–2024) e cartões por partida (2013–2024).

## O que os dados já mostram

1. **A vantagem existe e é grande.** Mandantes venceram 48,4% dos jogos, contra 26,9% de empates e 24,7% de vitórias visitantes. Marcaram 1,41 gol por jogo, contra 0,96 dos visitantes. Pollard geral: **63,0%** (IC 95% 61,7–64,3).
2. **A vantagem não é constante.** A série oscila entre 58,2% (2017) e 69,5% (2018), sem nunca cair abaixo de 50%. Há uma mudança de nível após 2018: **65,0% em 2013–2018 contra 61,0% em 2019–2024** (diferença de 4,0 p.p.; IC 95% 0,9–6,6).
3. **2020 ajuda a separar hipóteses, mas não resolve tudo.** Sem torcida, o Pollard caiu para **60,2%**, mas não desapareceu; em 2022–2024, com público de volta, ficou em **60,6%**. O retorno da torcida não restaurou o patamar anterior.

![Figura 1 — Índice de Pollard por temporada, com intervalo de 95% e mudança de nível em 2019 (2013–2024).](figuras/artigo_serie_pollard.png)

4. **Os canais tradicionais explicam pouco.** Distância entre cidades-sede não move o índice (62,0%–63,7%); clássicos sem viagem ainda registram 59,1%; o estádio habitual mostra 63,3% contra 60,7%; e o mandante desfavorecido na tabela ainda soma 54,2%. O público acompanha a força do clube (Spearman 0,41 com pontos), não a vantagem de casa (0,08). Estatísticas calculadas por `scripts/analyze_artigo.py` (`figuras/tab_artigo_contexto.csv`).

![Figura 2 — Público médio versus vantagem de casa e versus pontos por equipe-temporada (2013–2024).](figuras/artigo_publico_ha.png)

5. **Cartões são um canal promissor, mas a evidência é sugestiva.** Em 2019, o mandante recebia 0,18 amarelo a menos que o visitante; em 2020, a diferença passou a +0,11. Com efeitos fixos de equipe, a mudança é **+0,35**, mas o IC 95% (**−0,03 a +0,72**) inclui zero. Pênaltis convertidos: **+0,05** por jogo (IC 95% −0,06 a +0,15), sem mudança detectável; a fonte não registra pênaltis perdidos. Não é resultado conclusivo; é uma extensão que mostra que o canal arbitral pode ser medido.

![Figura 3 — Diferença de cartões amarelos casa−fora por temporada, com intervalo descritivo de 95%.](figuras/fig13_cartoes.png)

## O que ainda dá para fazer com os dados

Não faria mais tabelas descritivas nem gráficos soltos: isso encheria o artigo sem responder nada. Os dados permitem avançar em cinco frentes, em ordem de utilidade:

### 1. Modelo de Poisson para gols (a mais importante)

Modelar os gols como Poisson, com ataque e defesa por equipe e um parâmetro de vantagem de casa:

`log λ_casa = μ + ataque_i − defesa_j + γ`  
`log λ_fora = μ + ataque_j − defesa_i`

com `Σ ataque = Σ defesa = 0` para identificar o modelo. Isso estima a vantagem de casa **em escala de gols**, separa qualidade de ataque e defesa e permite testar se `γ` mudou depois de 2019. Se houver superdispersão, uso binomial negativa; se os placares baixos desviarem, correção de Dixon-Coles. É o passo que transforma médias descritivas em um modelo com parâmetros interpretáveis e intervalos de confiança.

### 2. Modelo hierárquico para a vantagem por equipe

Estimar uma vantagem de casa específica por equipe, com encolhimento:

`γ_i ~ N(γ, σ_γ²)`

O teste de `σ_γ²` responde a uma pergunta substantiva: a vantagem de casa é um fenômeno da liga ou varia de forma relevante entre clubes? O encolhimento também resolve o ruído das equipes com poucas temporadas — hoje o ranking por equipe tem correlação ítem-par de apenas 0,46, o que mostra que a estimativa isolada é instável. Além disso, o modelo decompõe a variância total em qualidade de equipe, temporada, vantagem de casa e resíduo — a forma mais direta de quantificar o "resíduo grande" que hoje aparece só de forma qualitativa.

### 3. Mudança de nível com incerteza

Hoje o corte em 2019 é visual. Posso estimar formalmente uma regressão segmentada:

`y_t = α + β t + δ · 1(t ≥ τ) + ε_t`

e estimar `τ` por mínimos quadrados, com intervalo por bootstrap, comparando 2019 com cortes alternativos. Isso dá uma resposta matemática a "quando mudou e quanto mudou", em vez de apenas apontar o ano no gráfico.

### 4. Inferência correta para dependência

Os ICs anuais por bootstrap de partidas ignoram que as mesmas equipes se repetem. Posso refazer com **bootstrap por cluster** (equipe-temporada) e usar **testes de permutação** para os contrastes de contexto e para 2020. Não é uma análise nova; é a correção necessária para que os intervalos e valores-p sejam confiáveis.

### 5. PCA/SVD da matriz equipe × temporada (opcional)

A matriz de correlação 12×12 já mostra que os componentes casa/fora dominam. Uma PCA/SVD da matriz de desempenho por equipe-temporada pode dizer se a vantagem de casa é um eixo próprio ou apenas ruído em torno do primeiro componente (força do clube). Só incluiria se ajudasse a interpretar; não faria isso apenas para exibir álgebra linear.

## O que eu não faria

- Redes neurais ou modelos caixa-preta para prever placar: não respondem à pergunta e não são auditáveis.
- Clusterizar equipes ou jogadores sem uma hipótese: vira exercício de técnica, não análise.
- Mais tabelas por temporada/equipe: o dado já está no repositório; no artigo, só o que sustenta a conclusão.
- Afirmações causais sobre torcida, VAR ou arbitragem: o desenho é observacional.

## Como ficaria o artigo (8–10 páginas)

| Seção | Conteúdo | Páginas |
|---|---|---:|
| Título, resumo e abstract | pergunta, dados, resultados principais | 0,5 |
| 1. Introdução | problema, lacuna, objetivo, contribuição | 1,5 |
| 2. Dados e métodos | base, Pollard, bootstrap, mudança de nível, contexto, DiD | 1,5 |
| 3. Resultados | série anual, nível, contexto, público e cartões | 3,0 |
| 4. Discussão | literatura, interpretação, limites | 1,5 |
| 5. Conclusão | resposta curta e agenda | 0,5 |
| Referências | ABNT, cerca de 15 entradas | 1,0 |

**Tabelas e figuras previstas:** Tabela 1 (indicadores por temporada, condensada); Tabela 2 (contrastes de contexto); Tabela 3 (público e cartões); Figura 1 (série de Pollard com IC); Figura 2 (público × HA); Figura 3 (cartões casa−fora). Se o modelo de Poisson entrar, ele ganha uma tabela própria e a Figura 1 pode ser substituída pelo ajuste do modelo.

## O que sai da monografia

- Capítulo de desenvolvimento do dashboard e telas: fica apenas um parágrafo e o link do repositório.
- Revisão de literatura extensa: reduzida ao essencial para situar a pergunta.
- 11 tabelas e 13 figuras: ficam 3 e 3; o restante vai para material suplementar.
- Apêndices de dicionário de dados, casos de teste e qualidade: ficam no repositório.

## O que eu gostaria de saber do senhor

1. O formato artigo (8–10 páginas) e o recorte 2013–2024 substituem a monografia no curso? Qual o limite de páginas e o template?
2. O senhor acha que vale investir no modelo de Poisson e no modelo hierárquico, ou prefere manter o artigo mais descritivo e enxuto?
3. O dashboard entra como artefato complementar ou apenas como link de reprodutibilidade?
4. Mantenho as extensões de público e cartões no artigo ou deixo apenas o núcleo (Pollard, variação e contexto)?
5. Qual o veículo/formato de avaliação: artigo acadêmico, relatório técnico ou artigo de congresso?

Obrigado pela leitura. Se o senhor aprovar o formato, eu preparo o rascunho completo do artigo já com as tabelas e figuras finais.

José Inamar de Medeiros Júnior
