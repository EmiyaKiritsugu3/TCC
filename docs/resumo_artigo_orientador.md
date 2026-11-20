# Resumo para o orientador — proposta de artigo

**Título proposto:** Vantagem de jogar em casa na Série A: uma análise descritiva de 19 temporadas (2006–2024)

**Formato:** artigo de 8 a 10 páginas, com 3 tabelas e 3 figuras, em vez da monografia extensa.

## Em uma frase

Em 19 temporadas, o mandante somou **63,7%** dos pontos em disputa; a vantagem caiu depois de 2018, mas não desapareceu, e os canais testados — viagem, estádio, público e cartões — explicam apenas parte do fenômeno.

## O que o trabalho pergunta

Qual foi a magnitude da vantagem de jogar em casa no Campeonato Brasileiro Série A entre 2006 e 2024, como ela variou entre temporadas e clubes, e quais fatores contextuais estão associados a essa variação. O estudo é **descritivo e observacional**: não testa causalidade nem faz previsão de resultados.

## O que foi feito

- **Base principal:** 7.219 partidas válidas, 19 temporadas (2006–2024), com regras de limpeza documentadas, download pinado e verificação SHA-256.
- **Validação:** 99,96% de concordância com o OpenFootball (2.659/2.660 partidas) e recálculo de **19/19 campeões**.
- **Indicador central:** índice de Pollard, que mede o percentual de pontos conquistados pelo mandante sobre o total de pontos em disputa. Em 63,7%, o mandante fica 13,7 pontos percentuais acima da neutralidade.
- **Métodos complementares:** intervalo de confiança por bootstrap, mudança de nível, matriz de correlação de Spearman, análise de contexto e diferença-em-diferenças para o contraste 2019→2020.
- **Extensões externas:** público e arbitragem (2007–2024) e cartões por partida (2013–2024).

## Cinco resultados que sustentam o artigo

1. **A vantagem existe e é grande.** Mandantes venceram 49,0% dos jogos, contra 26,8% de empates e 24,1% de vitórias visitantes. Marcaram 1,49 gol por jogo, contra 1,00 dos visitantes. Pollard geral: **63,7%** (IC 95% 62,6–64,7).
2. **A vantagem não é constante.** A série oscila entre 58,2% (2017) e 69,5% (2018), sem nunca cair abaixo de 50%. Há uma mudança de nível após 2018: **64,9% em 2006–2018 contra 61,0% em 2019–2024** (diferença de 3,9 p.p.; IC 95% 2,1–5,6).
3. **2020 ajuda a separar hipóteses, mas não resolve tudo.** Sem torcida, o Pollard caiu para **60,2%**, mas não desapareceu; em 2022–2024, com público de volta, ficou em **60,6%**. O retorno da torcida não restaurou o patamar anterior.
4. **Os canais tradicionais explicam pouco.** Distância entre cidades-sede não move o índice (63,4%–63,9%); clássicos sem viagem ainda registram 58,2%; o estádio habitual mostra 64,1% contra 59,4%; e o mandante desfavorecido na tabela ainda soma 55,6%. O público acompanha a força do clube (Spearman 0,46 com pontos), não a vantagem de casa (0,07; −0,01 sem 2020–2021).
5. **Cartões são um canal promissor, mas a evidência é sugestiva.** Em 2019, o mandante recebia 0,18 amarelo a menos que o visitante; em 2020, a diferença passou a +0,11. Com efeitos fixos de equipe, a mudança é **+0,35**, mas o IC 95% (**−0,03 a +0,72**) inclui zero. Não é resultado conclusivo; é uma extensão que mostra que o canal arbitral pode ser medido.

## O que o artigo entrega

- A série anual contínua mais longa do tema com base auditada e validação externa.
- Um retrato da magnitude, da variação e da mudança de nível da vantagem de casa.
- Uma decomposição descritiva dos fatores associados, separando o que os dados permitem dizer do que não permitem.
- Um pipeline reproduzível e um dashboard como artefato de apoio, sem transformar o artigo em relatório de software.

## Estrutura proposta (8–10 páginas)

| Seção | Conteúdo | Páginas |
|---|---|---:|
| Título, resumo e abstract | pergunta, dados, resultados principais | 0,5 |
| 1. Introdução | problema, lacuna, objetivo, contribuição | 1,5 |
| 2. Dados e métodos | base, Pollard, bootstrap, mudança de nível, contexto, DiD | 1,5 |
| 3. Resultados | série anual, nível, contexto, público e cartões | 3,0 |
| 4. Discussão | literatura, interpretação, limites | 1,5 |
| 5. Conclusão | resposta curta e agenda | 0,5 |
| Referências | ABNT, cerca de 15 entradas | 1,0 |

**Tabelas e figuras previstas:** Tabela 1 (indicadores por temporada, condensada); Tabela 2 (contrastes de contexto); Tabela 3 (público e cartões); Figura 1 (série de Pollard com IC); Figura 2 (público × HA); Figura 3 (cartões casa−fora).

## O que sai da monografia

- Capítulo de desenvolvimento do dashboard e telas: fica apenas um parágrafo e o link do repositório.
- Revisão de literatura extensa: reduzida ao essencial para situar a pergunta.
- 11 tabelas e 13 figuras: ficam 3 e 3; o restante vai para material suplementar.
- Apêndices de dicionário de dados, casos de teste e qualidade: ficam no repositório.
- Detalhamento de todas as fontes externas: resumido em um parágrafo de dados e limitações.

## Cuidados interpretativos

- O desenho é observacional; não há alegação causal.
- Público é um proxy de torcida, não uma medida direta.
- 2020 concentra pandemia, calendário atípico, protocolos e VAR; o desenho não separa esses choques.
- Cartões refletem arbítrio e comportamento do jogador; pênaltis e decisões discricionárias não são observados.
- A fonte primária não tem licença explícita; o bruto não é redistribuído e a reprodução usa download pinado.

## Decisões que preciso do orientador

1. O formato artigo (8–10 páginas) substitui a monografia no curso? Qual o limite de páginas e o template?
2. O dashboard entra como artefato complementar ou apenas como link de reprodutibilidade?
3. Mantenho as extensões de público e cartões no artigo ou deixo apenas o núcleo (Pollard, variação e contexto)?
4. Qual o veículo/formato de avaliação: artigo acadêmico, relatório técnico ou artigo de congresso?
