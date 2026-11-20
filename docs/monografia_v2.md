# Análise estatística da vantagem de jogar em casa no Campeonato Brasileiro Série A: desenvolvimento de um dashboard interativo para análise de resultados históricos

> **Documento consolidado — versão 3 (19/11/2026).**
> Base: rascunhos `cap1`–`cap7` unificados e renumerados; **estrutura alinhada ao
> padrão UFRN/CERES-BSI** (Resolução Nº 001/2016-CSI, Anexo 1 + 3 TCCs do curso na
> BDM: capa institucional, folha de rosto, folha de avaliação, listas, cap. 1 com
> 1.1–1.6 no padrão do curso). Texto pronto em 3ª pessoa; o que ainda exige o aluno
> está marcado com a tag [PENDENTE - ORIENTADOR]. Na conversão para o template: Times New Roman ou Arial 12,
> espaçamento 1,5, margens 3 cm esq. / 2 cm dir., A4. Ficha catalográfica é emitida
> pela SISBI no depósito da BDM (não incluir por conta própria). Pós-orientador:
> aplicar as 5 decisões de `docs/resumo_orientador.md` (departamento da capa já
> confirmado: DCT).
> **Versão 3:** acrescenta a análise de contexto (viagem, clássico, estádio,
> descanso, força e era), intervalos de confiança anuais e a mudança de nível
> pós-2018, sem alterar os números validados da versão 2.

---

## CAPA (elemento pré-textual, p. 1 — sem número)

<!-- Departamento confirmado: "Departamento de Computação e Tecnologia" (DCT), como nos TCCs do curso na BDM. -->

UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
CENTRO DE ENSINO SUPERIOR DO SERIDÓ
DEPARTAMENTO DE COMPUTAÇÃO E TECNOLOGIA
BACHARELADO EM SISTEMAS DE INFORMAÇÃO

ANÁLISE ESTATÍSTICA DA VANTAGEM DE JOGAR EM CASA NO CAMPEONATO BRASILEIRO SÉRIE A: DESENVOLVIMENTO DE UM DASHBOARD INTERATIVO PARA ANÁLISE DE RESULTADOS HISTÓRICOS

JOSÉ INAMAR DE MEDEIROS JÚNIOR

CAICÓ – RN
2026

## FOLHA DE ROSTO (obrigatória, p. 2 — sem número)

JOSÉ INAMAR DE MEDEIROS JÚNIOR

ANÁLISE ESTATÍSTICA DA VANTAGEM DE JOGAR EM CASA NO CAMPEONATO BRASILEIRO SÉRIE A: DESENVOLVIMENTO DE UM DASHBOARD INTERATIVO PARA ANÁLISE DE RESULTADOS HISTÓRICOS

<!-- Redação peculiar à Natureza do trabalho (meio da página), no padrão dos TCCs do curso: -->

Trabalho de conclusão de curso apresentado para obtenção de título de bacharel no curso de Sistemas de Informação do Centro de Ensino Superior do Seridó da Universidade Federal do Rio Grande do Norte.

Orientador: Prof. Dr. Francisco Marcio Barboza

CAICÓ – RN
2026

<!-- Ficha catalográfica NÃO va aqui: emitida pelo Sistema de Bibliotecas (SISBI)
     após o depósito na BDM; alocar como visto em amostras, antes da folha de
     avaliação, só na versão final impressa. -->

## FOLHA DE AVALIAÇÃO (obrigatória, p. 3 — sem número)

JOSÉ INAMAR DE MEDEIROS JÚNIOR

ANÁLISE ESTATÍSTICA DA VANTAGEM DE JOGAR EM CASA NO CAMPEONATO BRASILEIRO SÉRIE A: DESENVOLVIMENTO DE UM DASHBOARD INTERATIVO PARA ANÁLISE DE RESULTADOS HISTÓRICOS

Trabalho de conclusão de curso apresentado para obtenção de título de bacharel no curso de Sistemas de Informação do Centro de Ensino Superior do Seridó da Universidade Federal do Rio Grande do Norte.

<!-- Data da defesa + banca, preencher após indicações do orientador: -->

Caicó – RN, [dia] de [mês] de 2026

Aprovado em: __/__ /____ — Nota: ______

Banca Examinadora:

Dr. Francisco Marcio Barboza
Orientador — DCT/UFRN

**[PENDENTE - ORIENTADOR]** 2º membro da banca — aguardar indicação do orientador (nome, titulação, vínculo)

**[PENDENTE - ORIENTADOR]** 3º membro da banca — aguardar indicação do orientador (nome, titulação, vínculo)

---

## LISTA DE FIGURAS (opcional, recomendada — o trabalho tem 13 figuras)

Figura 1 — Aba Visão geral do dashboard: filtros, cartões de indicadores e distribuição de resultados.
Figura 2 — Aba Evolução histórica: índice de Pollard por temporada, distribuição de resultados, médias de gol e tabela anual.
Figura 3 — Aba Equipes e partidas: consulta por equipe/temporada, desempenho em casa e fora e tabela de partidas (recorte: temporada 2019, equipe Flamengo).
Figura 4 — Aba Metodologia e dados: fonte, período, regras de limpeza e relatório de qualidade.
Figura 5 — Distribuição dos resultados das 7.219 partidas da Série A, 2006–2024.
Figura 6 — Média de gols por partida de mandantes e visitantes por temporada, 2006–2024.
Figura 7 — Índice de vantagem em casa de Pollard por temporada, 2006–2024.
Figura 8 — Proporção de vitórias do mandante, empates e vitórias do visitante por temporada, 2006–2024.
Figura 9 — Série anual do índice de Pollard com intervalo de confiança de 95% e médias pré/pós-2019.
Figura 10 — Pollard por contexto da partida: clássico, distância, mesma UF, estádio, descanso, força, era e pandemia.
Figura 11 — Matriz de correlação por equipe-temporada (Spearman).
Figura 12 — Público médio, vantagem casa−fora e pontos médios por temporada por equipe (2007–2024).
Figura 13 — Cartões amarelos casa−fora por temporada, com intervalo de confiança de 95% e destaque para 2020 (2013–2024).

## LISTA DE TABELAS

Tabela 1 — Indicadores por temporada: n, proporções de resultados, médias de gols, pontos, índice de Pollard e IC 95%.
Tabela 2 — Evidências da vantagem de jogar em casa na literatura brasileira e neste trabalho.
Tabela 3 — Matriz de rastreabilidade: requisito funcional, tela e evidência/teste.
Tabela 4 — Síntese dos testes automatizados por grupo.
Tabela 5 — Pollard por contexto da partida, com n e IC 95%, 2006–2024.
Tabela 6 — Extremos da vantagem casa−fora por equipe (pelo menos cinco temporadas).
Tabela 7 — Correlações de Spearman com a vantagem casa−fora por equipe-temporada.
Tabela 8 — Público e índice de Pollard por bloco, 2007–2024.
Tabela 9 — Associações do público com desempenho e vantagem de casa.
Tabela 10 — Público médio e desempenho por quartil de público (times com pelo menos cinco temporadas), 2007–2024.
Tabela 11 — Cartões por temporada, diferença casa−fora e IC 95%, 2013–2024.

## LISTA DE SIGLAS

BDM — Biblioteca Digital de Monografias (UFRN).
BSI — Bacharelado em Sistemas de Informação.
CBF — Confederação Brasileira de Futebol.
CC0 — Creative Commons Zero (dedicação ao domínio público).
CERES — Centro de Ensino Superior do Seridó (UFRN).
CSV — valores separados por vírgula (*comma-separated values*).
DCT — Departamento de Computação e Tecnologia (CERES/UFRN).
DOI — identificador de objeto digital (*digital object identifier*).
HA — vantagem de jogar em casa (*home advantage*).
JSON — notação de objetos JavaScript (*JavaScript object notation*).
NBR — Norma Brasileira (ABNT).
RF — requisito funcional.
RNF — requisito não funcional.
SHA — algoritmo de hash seguro (*secure hash algorithm*; SHA-256 na verificação de integridade).
SISBI — Sistema de Bibliotecas da UFRN.
UFRN — Universidade Federal do Rio Grande do Norte.
VAR — árbitro assistente de vídeo (*video assistant referee*).
VC — vantagem em casa (índice de Pollard).

---

## RESUMO

Este trabalho apresenta uma análise estatística descritiva da vantagem de jogar em casa no Campeonato Brasileiro Série A entre as temporadas de 2006 e 2024, acompanhada do desenvolvimento de um dashboard interativo para exploração dos resultados históricos. A pesquisa, de natureza aplicada, abordagem quantitativa e objetivos exploratórios e descritivos, utilizou dados secundários de partidas de um repositório público, submetidos a auditoria de qualidade, padronização e validação cruzada contra uma fonte independente. A base resultante, de 7.219 partidas válidas, sustentou o cálculo de proporções de resultados, médias de gols e do índice de vantagem em casa de Pollard — percentual de pontos conquistados pelos mandantes, VC = Pm/(Pm+Pv)×100 — por período, por temporada e por equipe, exibidos em aplicação web desenvolvida em Python, com Pandas, Plotly e Streamlit, coberta por testes automatizados. Os resultados indicam predominância persistente do mando: os mandantes venceram 49,0% das partidas, os visitantes 24,1%, e o índice agregado do período foi de 63,7%, variando de 58,2% (2017) a 69,5% (2018), sem queda abaixo de 50% em nenhuma temporada. A série, porém, não é estacionária: o índice cai de 64,9% em 2006–2018 para 61,0% em 2019–2024 (diferença de 3,9 p.p.; IC 95% 2,1–5,6), mudança de nível coincidente com a estreia do VAR e a pandemia. A análise contextual mostra que não há associação relevante com a distância (63,4%–63,9%), que clássicos sem viagem ainda registram 58,2%, que o estádio habitual mostra 4,7 p.p. de diferença bruta (0,13 ponto/jogo na comparação dentro de equipe-temporada) e que o mandante desfavorecido na tabela ainda soma 55,6%. A matriz de correlação por equipe-temporada mostra associação forte com os componentes casa/fora (+0,57 e −0,46), mas quase nula com distância média (−0,01), pontos (0,08) e posição (−0,08), e fraca com estádio habitual (0,10). Uma base externa de público (2007–2024; 6.618 partidas) mostra que o público médio acompanha a força do clube (Spearman 0,46 com pontos), mas não a vantagem casa−fora (0,07; −0,01 sem 2020–2021); sem torcida em 2020, o índice caiu para 60,2%, mas não desapareceu. Uma extensão com 4.559 partidas (2013–2024) mostra que o mandante recebia 0,18 cartão amarelo a menos em 2019 e +0,11 em 2020; a mudança com efeitos fixos de equipe é +0,35, mas o IC 95% (−0,03 a +0,72) inclui zero, de modo que o canal arbitral é sugestivo, não conclusivo. O estudo não avalia causalidade nem previsão de resultados. Como contribuição, entrega uma série histórica homogênea de 19 temporadas, um fluxo de tratamento reproduzível e auditado, uma decomposição descritiva dos fatores associados e um sistema de apoio à análise de dados esportivos.

**Palavras-chave:** vantagem de jogar em casa; índice de Pollard; futebol brasileiro; dashboard; visualização de dados; análise descritiva.

## ABSTRACT

This work presents a descriptive statistical analysis of home advantage in Brazil's Série A football league across the 2006–2024 seasons, along with the development of an interactive dashboard for exploring historical results. An applied, quantitative, exploratory and descriptive study based on secondary match data from a public repository, audited for quality and cross-validated against an independent source; the resulting dataset contains 7,219 valid matches. It supports the computation of result proportions, goal averages and Pollard's home advantage index — the percentage of points won by home teams, HA = Pm/(Pm+Pv)×100 — for the whole period, by season and by team, displayed in a web application built with Python, Pandas, Plotly and Streamlit and covered by automated tests. Results show a persistent home predominance: home teams won 49.0% of matches, away teams 24.1%, and the aggregate index for the period was 63.7%, ranging from 58.2% (2017) to 69.5% (2018), never falling below 50%. The series is not stationary, however: the index falls from 64.9% in 2006–2018 to 61.0% in 2019–2024 (difference 3.9 pp; 95% CI 2.1–5.6), a level shift coinciding with the introduction of VAR and the pandemic. Contextual analysis shows no relevant association with distance (63.4%–63.9%), that zero-travel derbies still register 58.2%, that the usual stadium shows a 4.7 pp raw difference (0.13 point per game in the within-team-season comparison) and that a home team ranked below its opponent still reaches 55.6%. The team-season correlation matrix shows a strong association with the home/away components (+0.57 and −0.46), but almost none with average distance (−0.01), points (0.08) and rank (−0.08), and a weak one with the usual stadium (0.10). An external attendance dataset (2007–2024; 6,618 matches) shows that average attendance tracks club strength (Spearman 0.46 with points) but not home advantage (0.07; −0.01 excluding 2020–2021); without crowds in 2020, the index fell to 60.2% but did not disappear. An extension with 4,559 matches (2013–2024) shows that home teams received 0.18 fewer yellow cards in 2019 and 0.11 more in 2020; the change with team fixed effects is +0.35, but the 95% CI (−0.03 to +0.72) includes zero, so the refereeing channel is suggestive rather than conclusive. The study makes no causal or predictive claims. Its contribution is a homogeneous 19-season historical series, a reproducible and audited data pipeline, a descriptive decomposition of associated factors, and a usable analytics system for sports data.

**Keywords:** home advantage; Pollard index; Brazilian football; dashboard; data visualization; descriptive analytics.

**[PENDENTE - ORIENTADOR]** Revisar Resumo/Abstract após as 5 decisões (item 4: Spearman). Conferir contagem de palavras se exigida.

---

## SUMÁRIO (obrigatório)

**1 INTRODUÇÃO**
1.1 Tema e delimitação
1.2 Contextualização e problema
1.3 Objetivos da pesquisa
&nbsp;&nbsp;&nbsp;&nbsp;1.3.1 Objetivo geral
&nbsp;&nbsp;&nbsp;&nbsp;1.3.2 Objetivos específicos
1.4 Delimitação do estudo
1.5 Motivação e justificativa
1.6 Estrutura do trabalho
**2 REFERENCIAL TEÓRICO**
2.1 A vantagem de jogar em casa
2.2 Evidências no futebol brasileiro
2.3 Análise de dados e visualização como apoio à decisão
2.4 Síntese
**3 METODOLOGIA**
3.1 Classificação da pesquisa
3.2 Fonte e validação dos dados
3.3 Critérios de inclusão e exclusão
3.4 Indicadores
**4 ANÁLISE E DESENVOLVIMENTO DO SISTEMA**
4.1 Arquitetura
4.2 Tratamento dos dados e cálculos
4.3 Requisitos e telas
4.4 Testes
**5 RESULTADOS E DISCUSSÃO**
5.1 Resultados gerais do período 2006–2024
5.2 Variação entre temporadas
5.3 Discussão frente à literatura
5.4 Fatores contextuais associados
5.5 Matriz de correlação
5.6 Público e arbitragem: evidência externa
5.7 Cartões: um canal de arbitragem
5.8 Resposta às perguntas de pesquisa
**6 CONCLUSÃO**
6.1 Resposta à pergunta
6.2 Contribuição
6.3 Limitações
6.4 Trabalhos futuros
**REFERÊNCIAS**
**APÊNDICE A — Dicionário de dados**
**APÊNDICE B — Relatório de qualidade da base**
**APÊNDICE C — Validações executadas**
**APÊNDICE D — Casos de teste e instruções de execução**

<!-- No template final: sublinhar títulos de capítulos (NBR 6024), incluir número
     de página à direita com leader pontilhado (NBR 6027), e page-num a partir de 1
     na Introdução. -->

---

# 1 INTRODUÇÃO

## 1.1 Tema e delimitação

Este trabalho trata da vantagem de jogar em casa no Campeonato Brasileiro Série A — o fenômeno pelo qual equipes mandantes conquistam, historicamente, mais pontos e gols que as visitantes — e de sua exploração por meio de um dashboard interativo. O recorte são as temporadas completas de 2006 a 2024 da Série A masculina, em formato de 20 clubes e pontos corridos, totalizando 7.219 partidas com placar válido.

## 1.2 Contextualização e problema

No futebol, equipes mandantes conquistam historicamente mais pontos que visitantes, fenômeno conhecido como vantagem de jogar em casa e quantificado desde Pollard (1986, *apud* Almeida et al., 2011) pelo percentual de pontos conquistados pelos mandantes. No Brasil, estudos apontam patamar próximo de 65% (SILVA; MOREIRA, 2008; ALMEIDA et al., 2011), acima das ligas europeias.

A literatura nacional, porém, trabalha com janelas temporais distintas e granularidades diferentes: Silva e Moreira (2008) cobrem 2002/03–2006/07; Almeida et al. (2011) cobrem 2003–2009 de forma agregada; Ribeiro et al. (2022) concentram-se em 2018–2020. Falta, nesse conjunto, uma série anual longa e homogênea — restrita ao formato estável de 20 clubes em pontos corridos, com auditoria documentada da base e validação externa — que permita observar como o fenômeno varia ano a ano sem trocar de régua no meio do caminho. É essa lacuna que delimita o problema: sem uma série nessas condições, qualquer comparação entre temporadas corre o risco de confundir efeito de formato, de fonte ou de métrica com variação real da vantagem de jogar em casa.

A partir desse contexto, a pergunta de pesquisa é: qual foi a magnitude da vantagem de jogar em casa no Campeonato Brasileiro Série A entre 2006 e 2024, e como os indicadores de mandantes e visitantes variaram entre as temporadas? Perguntas secundárias: proporções de resultados; médias de gols; evolução anual do índice de Pollard; diferenças entre temporadas e clubes; associação entre o contexto da partida (viagem, clássico, estádio, descanso, força e era) e o índice; e uma matriz de correlação entre indicadores e contexto.

A pesquisa parte de duas hipóteses principais, formuladas antes da análise. **H1:** o índice de Pollard do período 2006–2024 será superior a 50%, indicando que os mandantes somaram mais pontos que os visitantes. **H2:** o índice não permanecerá constante entre as temporadas, com variação observável na série anual. A dimensão contextual é exploratória e formulada em três hipóteses adicionais, todas descritivas. **H3:** a distância e o clássico não explicam o grosso da vantagem. **H4:** o estádio habitual está associado a uma vantagem adicional modesta. **H5:** há uma mudança de nível após 2018, com queda sustentada do índice. H3–H5 não são testes causais: servem para delimitar quanto cada mecanismo pode explicar.

## 1.3 Objetivos da pesquisa

### 1.3.1 Objetivo geral

Desenvolver um dashboard interativo para analisar estatisticamente a vantagem de jogar em casa na Série A, considerando as temporadas de 2006 a 2024.

### 1.3.2 Objetivos específicos

Conforme a especificação do projeto: identificar e documentar a fonte de dados; padronizar e verificar a base; calcular indicadores de resultados, gols, pontos e vantagem em casa; comparar os indicadores entre temporadas e, secundariamente, entre equipes; descrever associações entre o contexto da partida (viagem, clássico, estádio, descanso, força e era) e o índice, incluindo uma matriz de correlação, sem pretensão causal; construir visualizações interativas; testar os cálculos; e discutir resultados e limitações da análise baseada em placares.

## 1.4 Delimitação do estudo

O estudo abrange a Série A masculina, temporadas completas 2006–2024 (formato estável de 20 clubes em pontos corridos), partidas com placar válido (n = 7.219). Ficam fora do escopo: previsão de resultados, inteligência artificial, apostas, outras divisões e dados de jogadores.

## 1.5 Motivação e justificativa

A motivação para este trabalho nasce de dois interesses que correram em paralelo: o acompanhamento cotidiano do futebol brasileiro e a formação do autor em Sistemas de Informação. A pergunta pela "força do mando de campo" aparece a cada rodada, no discurso de comentaristas e torcedores — inclusive o autor —, quase sempre sem qualquer número que a sustente; ao mesmo tempo, o curso oferece as ferramentas para transformar dados públicos nessas respostas. Ao descobrir que os resultados históricos do Campeonato Brasileiro estavam disponíveis em um repositório aberto, a oportunidade de unir os dois interesses se tornou concreta: verificar com dados o que o cotidiano do esporte já sugeria, e entregar o resultado não como um relatório estático, mas como um instrumento que qualquer pessoa possa explorar.

A temática é adequada a Sistemas de Informação porque envolve aquisição e tratamento de dados, definição de indicadores, visualização interativa e construção de um sistema de apoio à análise — uma aplicação direta do que a análise de negócios descritiva discute, respondendo "o que aconteceu?" (SHARDA; DELEN; TURBAN, 2019). A contribuição não é alegar ineditismo do fenômeno, e sim combinar um recorte histórico longo e homogêneo (19 temporadas), um fluxo de tratamento reproduzível e auditado e um dashboard interativo para exploração dos dados, permanecendo útil como ferramenta de consulta após o término do curso.

Em termos práticos, a contribuição se desdobra em três entregas verificáveis. A primeira é a série anual homogênea de 19 temporadas (2006–2024), com 7.219 partidas válidas, regras de limpeza documentadas e dois casos metodológicos tratados sem imputação (2016 e 2020). A segunda é o fluxo reproduzível e auditado: download pinado por commit com verificação SHA-256, construção determinística da base processada, validação cruzada externa de 99,96% e recálculo dos 19 campeões a partir dos placares. A terceira é o dashboard reutilizável, com cinco abas que cobrem do panorama geral à consulta por equipe e à análise de contexto, coberto por 114 testes automatizados (105 rápidos + 9 de integração) e formatado em português. A análise contextual não muda a pergunta central: ela delimita o que os dados permitem dizer sobre os fatores associados, sem converter associação em causa. Nenhuma das três depende de alegação causal: o valor está na medida repetível e na exploração assistida, não na explicação do fenômeno.

## 1.6 Estrutura do trabalho

O restante do documento organiza-se em cinco capítulos: o capítulo 2 revisa a literatura sobre vantagem em casa e fundamentos de análise de dados e visualização; o capítulo 3 descreve a metodologia; o capítulo 4 detalha o desenvolvimento do sistema; o capítulo 5 apresenta e discute os resultados; o capítulo 6 conclui, com limitações e trabalhos futuros.

---

# 2 REFERENCIAL TEÓRICO

## 2.1 A vantagem de jogar em casa

Fenômeno documentado em diversos esportes coletivos, a vantagem de jogar em casa define-se operacionalmente, desde Pollard (1986, *apud* ALMEIDA et al., 2011), pelo percentual de pontos conquistados pelos mandantes: acima de 50% em competição equilibrada de ida e volta indica vantagem. O método — incluindo empates no cálculo — é o adotado neste trabalho (ver seção 3.4) e está descrito em texto aberto em Matos, Amaro e Pollard (2020), que o compara a alternativas de quantificação. Fatores associados na literatura: torcida, arbitragem, familiaridade com o campo e deslocamentos (NEVILL; HOLDER, 1999, *apud* ALMEIDA et al., 2011).

Cada um desses fatores tem um mecanismo plausível, ainda que nenhum seja medido neste estudo. A torcida atua como pressão ambiental: apoio contínuo aos mandantes e hostilidade aos visitantes, com possível efeito indireto sobre decisões da arbitragem em lances interpretativos. Os deslocamentos impõem fadiga de viagem e quebra de rotina aos visitantes — fator que Almeida et al. (2011) aventam ao comparar divisões com logísticas distintas. A arbitragem, por sua vez, concentra a hipótese de viés inconsciente pró-mandante em decisões discricionárias, e não de favorecimento deliberado. O experimento de Nevill, Balmer e Williams (2002) mediu esse canal: árbitros avaliando lances com barulho de torcida marcaram 15,5% menos faltas contra o mandante do que em silêncio. A familiaridade com o campo cobre dimensões do estádio, gramado e referências espaciais que beneficiam quem treina e joga habitualmente no local. Há ainda o componente territorial e de rotina: dormir em casa, manter horários de treino e evitar hotéis e aeroportos preservam a preparação do mandante. Na vertente biológica, Neave e Wolfson (2003) associam o mando à territorialidade, com elevação de testosterona nos mandantes. O ponto metodológico relevante é que esses mecanismos são correlacionados entre si — torcida cheia, viagem longa do adversário e arbitragem sob pressão costumam ocorrer juntos —, de modo que dados de placar e mando, sozinhos, não permitem isolar causas. Por isso este trabalho trata o conjunto como contexto interpretativo da literatura e restringe suas conclusões ao plano descritivo: medir a magnitude e a variação, sem atribuir parcela a cada mecanismo.

## 2.2 Evidências no futebol brasileiro

Silva e Moreira (2008) encontraram para a Série A (2002/03–2006/07) 64,9 ± 2,2%, acima de Alemanha, Argentina, Espanha, Inglaterra, Itália e Portugal (só a França não diferiu) — primeira âncora numérica nacional. Almeida et al. (2011), em 2003–2009 (n = 5.497), reportaram Série B (69 ± 2,3%) acima da Série A (65 ± 2,3%), com grande tamanho de efeito (η² = 0,57), aventando viagens e condições de campo como explicação; usaram o mandante nominal da CBF, convenção mantida aqui. Ribeiro et al. (2022), em 2018–2020 (n = 2.280, Séries A e B), observaram queda na Série A coincidente com torcida ausente e estreia do VAR (2019) — sem atribuição causal isolada, posição também adotada aqui. Atenção às escalas: Ribeiro et al. usam ((H−A)/A)×100%, não o índice de Pollard; os valores não são diretamente comparáveis.

A Tabela 2 sintetiza essas evidências para leitura comparada com o presente estudo. Três observações orientam a comparação. Primeiro, o patamar brasileiro situa-se consistentemente na faixa de 60–70% na escala de Pollard, acima do que se reporta para as grandes ligas europeias — o que torna o Brasil um caso empiricamente interessante, e não apenas uma réplica. Segundo, a diferença entre divisões encontrada por Almeida et al. (2011), com efeito de grande magnitude, sugere que condições estruturais (viagens, estádios) pesam tanto quanto a força das equipes, hipótese compatível com a decisão deste trabalho de manter a análise no plano descritivo. Terceiro, a janela 2018–2020 de Ribeiro et al. (2022) ilumina exatamente o período de ruptura sanitária e regulatória (pandemia, VAR), e seus resultados são o contraponto direto para a leitura da temporada 2020 neste trabalho (ver §5.3). A contribuição incremental do presente estudo nesse quadro é a granularidade anual contínua sobre 19 temporadas homogêneas, com base auditada e validação externa — escala temporal que nenhum dos três estudos cobre com o mesmo recorte de formato.

**Tabela 2 — Evidências da vantagem de jogar em casa no futebol brasileiro.**

| Estudo | Período | Amostra | Métrica | Resultado principal |
|---|---|---|---|---|
| Silva e Moreira (2008) | 2002/03–2006/07 | Série A (5 temporadas) | Pollard | 64,9 ± 2,2%; acima de 6 ligas europeias |
| Almeida et al. (2011) | 2003–2009 | n = 5.497 (A + B) | Pollard | Série B 69 ± 2,3% acima da Série A 65 ± 2,3% (η² = 0,57) |
| Ribeiro et al. (2022) | 2018–2020 | n = 2.280 (A + B) | ((H−A)/A)×100% | Queda na Série A com torcida ausente e VAR; sem causa isolada |
| Este trabalho | 2006–2024 | n = 7.219 (19 temporadas) | Pollard | 63,7% no período; 58,2%–69,5% ao ano; mudança de nível pós-2018 (64,9% → 61,0%) |

Fonte: Elaboração própria, a partir das referências.

## 2.3 Análise de dados e visualização como apoio à decisão

A análise de negócios descritiva — o nível de entrada da taxonomia analítica de Sharda, Delen e Turban (2019) — responde "o que aconteceu?", o que legitima o escopo exclusivamente descritivo deste trabalho. Acima dela, na mesma taxonomia, estariam os níveis diagnóstico ("por que aconteceu?"), preditivo ("o que vai acontecer?") e prescritivo ("o que fazer?") — todos deliberadamente fora do escopo, conforme a delimitação (§1.4). Essa renúncia é uma decisão de desenho, não uma lacuna acidental: com apenas placar e mando nominal, o trabalho não dispõe das variáveis (público, arbitragem, elenco — e da viagem, só a distância entre sedes) que qualquer pretensão diagnóstica ou preditiva exigiria.

Sua interface típica é o dashboard, definido por Few (2006) como exibição visual das informações mais importantes para um ou mais objetivos, consolidadas em tela única e monitoráveis de relance. O sistema desenvolvido segue a definição — tela única por aba, cartões de indicadores, séries e tabela com exploração detalhada — e evita os erros catalogados por Few: tela estourada, contexto insuficiente, precisão excessiva e decoração inútil, buscando a simplicidade de "só o necessário, condensado sem perda de sentido". Na prática, isso se traduz em cinco abas de navegação única (sem menus aninhados), oito cartões na visão geral com unidade explícita, ajuda metodológica embutida no próprio indicador de Pollard e mensagens de estado vazio em vez de telas quebradas (RF10). A formatação em português com vírgula decimal (RNF04) e a separação entre cálculo, gráfico e interface (RNF06) completam a aderência: o usuário lê números no padrão local, e o código mantém cada camada testável isoladamente.

## 2.4 Síntese

A vantagem em casa persiste no Brasil em torno de 65% (escala de Pollard), é sensível a contexto e não tem causa única estabelecida. Este trabalho não propõe nova teoria: estende a série (2006–2024, granularidade anual), audita a base e entrega a análise em sistema reproduzível. O fio que une as três frentes revisadas é a medida comum: o percentual de pontos do mandante permite comparar divisões, décadas e contextos regulatórios distintos sem trocar de régua, e é sobre essa régua estável que os capítulos seguintes assentam metodologia, sistema e resultados.

---

# 3 METODOLOGIA

## 3.1 Classificação da pesquisa

Pesquisa aplicada (resulta em artefato de software), quantitativa, de objetivos exploratórios e descritivos, por procedimentos de pesquisa documental e análise de dados secundários, conforme a classificação de Gil (2008). Unidade de análise: a partida, agregada por temporada e, secundariamente, por equipe. O desenho segue as etapas da especificação (§9.2): revisão bibliográfica, escolha e auditoria da fonte, limpeza padronizada, construção dos indicadores, desenvolvimento do dashboard, testes contra casos manuais e base processada, e análise com registro de limitações. A opção pela partida como unidade — em vez do clube-temporada — preserva a granularidade máxima da fonte e permite qualquer agregação posterior sem perda; as agregações por temporada e por equipe são visões derivadas, recalculadas das mesmas linhas, o que elimina divergência entre telas por construção (RNF03).

## 3.2 Fonte e validação dos dados

Fonte primária: repositório público *Brasileirao_Dataset* (commit `15f027c`, acesso em 28/10/2026), sem licença explícita — adotou-se o plano de não redistribuir os dados brutos (download fixado no script de construção; arquivo bruto fora do versionamento; registro de proveniência em arquivo próprio). Auditoria inicial: 8.785 linhas, zero duplicatas, zero placares ausentes, zero divergências entre campo de vencedor e recálculo pelo placar.

O recorte 2006–2024 contém 7.219 partidas válidas, com dois casos documentados: 2016 com 379 jogos (a partida Chapecoense × Atlético-MG foi cancelada após a tragédia do voo da equipe) e a temporada 2020 estendida até 25/02/2021 (temporada atribuída por intervalo entre partidas, não por ano civil).

Validação cruzada independente contra o OpenFootball (domínio público, CC0) em 2018–2024: 2.659 de 2.660 partidas idênticas, zero divergências de placar; a única exceção é de data e explicada (jogo disputado em dois dias, 2023). Como segurança adicional, a classificação final de cada temporada foi recalculada a partir dos placares e confirmou os 19 campeões oficiais.

As ameaças à validade são declaradas de partida. Validade de constructo: o "mando" é o mandante nominal da fonte, que nem sempre corresponde ao estádio habitual da equipe (clássicos com mando trocado, reformas, punições com portões fechados) — o indicador mede, portanto, vantagem do mandante designado, não do estádio próprio. Validade interna: sem grupo de controle nem covariáveis (público, arbitragem, elenco, clima); da viagem, apenas a distância entre cidades-sede, nenhuma diferença observada admite leitura causal; o desenho é observacional sobre dados secundários. Validade externa: os resultados valem para a Série A masculina em pontos corridos com 20 clubes (2006–2024) e não se generalizam para outras divisões, formatos (mata-mata), futebol feminino ou outros países — a própria diferença entre Séries A e B reportada por Almeida et al. (2011) adverte contra a extrapolação. Validade de conclusão: todas as conclusões são descritivas sobre a série observada; a mudança de nível pós-2018 foi descrita com bootstrap por temporada e busca de ponto de quebra, sem teste causal. Como 2019 coincide com a estreia do VAR e antecede a pandemia, os choques não são separáveis; o texto não atribui a queda a um deles isoladamente.

**[PENDENTE - ORIENTADOR]** Confronto por amostra com a CBF, caso o orientador exija. Base já validada por cruzamento com OpenFootball (99,96%) e por campeões (19/19).

## 3.3 Critérios de inclusão e exclusão

Foram incluídas partidas da Série A entre 2006 e 2024 com mandante, visitante e placar final válido. Foram excluídos registros sem placar, com gols negativos, com mandante igual a visitante e duplicatas — toda exclusão contabilizada no relatório de qualidade da base, sem remoções silenciosas.

A franquia Barueri (2009) e Grêmio Prudente (2010) é a mesma entidade renomeada entre temporadas; os nomes são mantidos separados e a comparação por equipe é sempre contextualizada pela temporada, sem fusão de identidades no pipeline.

## 3.4 Indicadores

Para cada partida, o resultado e os pontos (3/1/0) são recalculados a partir do placar. Indicadores: proporções de vitória do mandante, empate e vitória do visitante; médias de gols por lado e diferença média; pontos somados por lado; e índice de Pollard, VC = Pm/(Pm+Pv)×100, indefinido quando Pm+Pv = 0. Adota-se a mesma escala de Pollard (1986) e Almeida et al. (2011), para comparabilidade com a literatura.

H1 é avaliada pelo índice agregado do período; H2, pela comparação descritiva das 19 temporadas, sem teste inferencial. A escala adotada é a de Pollard (1986), conforme Almeida et al. (2011) e Matos, Amaro e Pollard (2020).

A análise contextual usa oito dimensões derivadas da base, sem alterar placar ou mando: distância entre cidades-sede (haversine; clássicos na mesma cidade = 0), indicador de clássico, mesma unidade federativa, estádio mais frequente da equipe na temporada (proxy de estádio habitual), diferença de descanso entre as equipes (apenas partidas da Série A) e posição relativa na tabela antes da partida (favorito, equilibrado ou zebra, com margem de três posições), era (pré-2019 ou 2019+) e pandemia (2020–2021). Para cada grupo, o Pollard é recalculado e acompanhado de IC 95% por bootstrap de partidas (2.000 reamostragens por grupo e 3.000 para o indicador geral; EFRON; TIBSHIRANI, 1993). Comparações entre recortes usam bootstrap por temporada (4.000 reamostragens), preservando a dependência entre partidas da mesma temporada. Para reduzir a influência da força do clube, algumas comparações são feitas dentro de equipe-temporada: o resultado de cada partida é comparado com a média do próprio clube nos jogos em casa daquela temporada. A mudança de nível é descrita pelo melhor ponto de quebra da série anual e pela diferença entre as médias pré e pós-2019; não há teste de hipótese causal. A matriz de correlação usa Spearman (Pearson sobre os ranks), com pares completos e n ≥ 30: uma matriz por equipe-temporada (n = 380; HA, componentes, pontos, posição, distância média, estádio habitual e temporada) e outra por partida (n = 7.219; saldo de gols, distância, descanso, diferença de posição, clássico, estádio, era e pandemia). A leitura é descritiva: sem p-valor e sem causalidade; no nível de partida, as observações não são independentes.

---

# 4 ANÁLISE E DESENVOLVIMENTO DO SISTEMA

## 4.1 Arquitetura

Pipeline em camadas separadas: `load_data` (leitura da cópia imutável da fonte), `clean_data` (padronização e regras de limpeza), `metrics` (funções puras dos indicadores), `context` (variáveis descritivas de viagem, clássico, estádio, descanso, tabela e era), `associations` (bootstrap, grupos, mudança de nível, matriz de correlação e vantagem por equipe), `charts` (gráficos em Plotly) e a aplicação Streamlit com cinco abas. A separação segue o RNF06 (manutenibilidade): cálculos não conhecem interface, gráficos não calculam — recebem dicionários prontos — e a aplicação apenas filtra, formata e exibe. Essa disciplina é o que permite testar cada camada isoladamente: `metrics` com DataFrames sintéticos de três linhas, `clean_data` com brutos fabricados, `charts` com dicionários e a interface com `AppTest`, sem Selenium nem servidor de verdade.

A reprodutibilidade (RNF02) é garantida por construção determinística. O fluxo exige três comandos encadeados: baixar a fonte pinada (`fetch_raw.py`, com verificação SHA-256 e modo `--check` offline), construir a base (`build_processed.py`, mesma entrada → mesma saída, sem aleatoriedade nem dependência de relógio) e rodar os testes. As versões exatas do ambiente estão fixadas em `requirements-lock.txt` (pandas 3.1.0, Streamlit 1.66.1, Plotly 7.1.0), com faixas compatíveis em `requirements.txt`. A base processada acompanha um relatório de qualidade em JSON; a reprodução do fluxo produz os mesmos 7.219 registros e o mesmo relatório.

## 4.2 Tratamento dos dados e cálculos

A conversão de tipos não faz coerção silenciosa: placar ausente não se torna 0–0; valores negativos são rejeitados. A regra de espaços foi endurecida para o pandas 3 (`_strip` apara colunas de texto e do dtype `string`, preservando `NA`), e a ordem dos filtros importa: clubes ausentes são removidos antes da comparação mandante × visitante, para que `NA` não contamine a contagem de exclusões. A temporada é atribuída por intervalo entre partidas, método robusto a reagendamentos (caso 2020). Resultado e pontos são recalculados do placar. Dois casos permanecem documentados: 2016 com 379 jogos e conclusão da temporada 2020 em fevereiro de 2021.

A unicidade da base é fiscalizada em três níveis: `match_id` duplicado, linha integral duplicada e tripla (data, mandante, visitante) repetida — mantendo-se a primeira ocorrência e registrando o resto (zero ocorrências na base atual). Cada exclusão é contabilizada por motivo no `quality_report.json`, sem remoções silenciosas. A reconstrução da base após o endurecimento do pipeline alterou exclusivamente espaços em branco do campo `stadium`; todos os demais campos permaneceram idênticos célula a célula, prova verificada por comparação automatizada antes/depois.

## 4.3 Requisitos e telas

O sistema atende 12 requisitos funcionais (carga validada, filtros por temporada, indicadores gerais, séries temporais, médias de gols, consulta por equipe, tabela de partidas, ajuda metodológica, informações de proveniência, tratamento de estado vazio, exportação CSV e análise de contexto) e 8 requisitos não funcionais (simplicidade, reprodutibilidade, consistência entre gráficos, usabilidade em português, robustez, manutenibilidade, portabilidade e ausência de dados pessoais).

As quatro telas originais são evidenciadas nas Figuras 1 a 4; a aba Contexto é apresentada na seção 5.4. A Tabela 3 mostra a rastreabilidade de cada requisito funcional até a tela que o atende e a evidência que a comprova.

**Tabela 3 — Matriz de rastreabilidade (requisito → tela → evidência).**

| Requisito | Tela | Evidência / teste |
|---|---|---|
| RF01 — Carregar dados validados | Todas (carga na abertura) | erro legível se base ausente/vazia/sem colunas; `carregar()` |
| RF02 — Filtrar temporadas | Filtros globais + todas | multiselect alimenta `base`; respeitado por cartões e gráficos |
| RF03 — Indicadores gerais | Visão geral (Figura 1) | 7 cartões; `test_caso_referencia_tres_partidas` |
| RF04 — Comparar temporadas | Evolução histórica (Figura 2) | série de Pollard + barras 100%; `by_season` |
| RF05 — Comparar gols | Evolução histórica (Figura 2) | linha casa × fora; médias 1,49 × 1,00 |
| RF06 — Consultar equipe | Equipes e partidas (Figura 3) | `team_season` (53/37/90/38 Flamengo 2019) |
| RF07 — Tabela de partidas | Equipes e partidas (Figura 3) | dataframe filtrado por equipe/temporada |
| RF08 — Explicar indicadores | Visão geral + Metodologia | ajuda do Pollard; fórmulas na aba Metodologia |
| RF09 — Informações dos dados | Metodologia (Figura 4) | fonte, período, qualidade em JSON |
| RF10 — Filtros sem resultados | Todas | avisos + `st.stop`; recorte vazio retorna Nones |
| RF11 — Exportar CSV | Equipes e partidas | botão de download do recorte filtrado |
| RF12 — Analisar contexto | Contexto | `group_pollard` + `team_home_advantage` + `correlation_matrix`; IC 95%; nota de não causalidade |

Fonte: Elaboração própria, a partir da especificação.

**Figura 1 — Aba Visão geral do dashboard.**
(`figuras/app1_visao_geral.png`)
Legenda: filtros, cartões de indicadores e distribuição de resultados (recorte 2006–2024). Fonte: Elaboração própria.

**Figura 2 — Aba Evolução histórica do dashboard.**
(`figuras/app2_evolucao_historica.png`)
Legenda: índice de Pollard por temporada, distribuição de resultados, médias de gol e tabela anual. Fonte: Elaboração própria.

**Figura 3 — Aba Equipes e partidas do dashboard.**
(`figuras/app3_equipes_partidas.png`)
Legenda: consulta por equipe/temporada, desempenho em casa e fora e tabela de partidas (recorte: temporada 2019, equipe Flamengo). Fonte: Elaboração própria.

**Figura 4 — Aba Metodologia e dados do dashboard.**
(`figuras/app4_metodologia_dados.png`)
Legenda: fonte, período, regras de limpeza e relatório de qualidade. Fonte: Elaboração própria.

<!-- Renumeração concluída: Figuras 1–4 no capítulo 4 e Figuras 5–8 no capítulo 5, com legendas completas nas seções correspondentes e resumo na Lista de Figuras (`figuras/LEGENDAS.md` é a fonte das legendas). -->

## 4.4 Testes

Cento e quatorze testes automatizados (Pytest; 105 rápidos e 9 de integração) cobrem o caso de referência da especificação (três partidas manuais → índice de Pollard exatamente 50%), proporções, tratamento de denominador zero, recorte vazio, pontuação por equipe/temporada (incluindo Flamengo 2019: 53/37/90/38), variáveis contextuais (viagem, clássico, estádio, descanso, tabela, eras), funções de associação (bootstrap, mudança de nível, matriz de correlação, vantagem por equipe), parser de cartões, filtros das abas, formatação pt-BR, integridade SHA-256 e regras de limpeza. Todos passam (`114 passed`). Complemento de verificação externa: a validação cruzada contra o OpenFootball atingiu 99,96% de concordância (seção 3.2).

**Tabela 4 — Síntese dos testes por grupo.**

| Grupo | O que verifica | Testes |
|---|---|---:|
| `test_metrics` | fórmulas, Pollard, agregações, equipe/temporada | 9 passed |
| `test_context` | viagem, clássico, estádio, descanso, tabela, eras, cobertura dos 43 clubes | 20 passed |
| `test_associations` | bootstrap, mudança de nível, grupos, equipe, split-half e correlações | 19 passed |
| `test_data_validation` | regras de limpeza e exclusões contabilizadas | 8 passed |
| `test_load_data` | leitura como texto e validação de colunas | 5 passed |
| `test_openfootball` | parser, virada de ano, time não mapeado | 5 passed |
| `test_metrics_indicadores` | indicadores derivados e extremos anuais | 3 passed |
| `test_context_tabela` | tabela antes da partida e desempates | 3 passed |
| `test_clean_data_pipeline` | esquema, deduplicação e resultado recalculado | 3 passed |
| `test_charts_composicao` | séries, rótulos pt-BR, IC e matriz | 6 passed |
| `test_formatting` | pt-BR e separador dos gráficos | 2 passed |
| `test_app` | abas Equipes e Contexto; filtro e recorte Flamengo 2019 | 3 passed |
| `test_integrity` | SHA-256 aceita/rejeita | 1 passed |
| `test_check_monografia_guard` | auditor rejeita número obsoleto, tabela de cartões e cabeçalho ausente | 3 passed |
| `test_validate_cross_excecao` | tolerância da exceção conhecida de data | 2 passed |
| `test_review_fixes` | regressões das revisões (download, exceção, CI, placares) | 9 passed |
| `test_bootstrap_checks` | bootstrap/check read-only, pins e instalação editável | 4 passed |
| `test_cards` | parser de cartões, normalização de times e desempates | 9 passed |
| **Total** | **105 rápidos + 9 de integração** | **114 passed** |

Fonte: Elaboração própria; detalhamento em Apêndice D.

---

# 5 RESULTADOS E DISCUSSÃO

## 5.1 Resultados gerais do período 2006–2024

No conjunto das 7.219 partidas analisadas, os mandantes venceram 49,0% dos jogos, contra 26,8% de empates e 24,1% de vitórias dos visitantes (**Figura 5**). Os mandantes marcaram em média 1,49 gol por partida, contra 1,00 dos visitantes (diferença média de +0,49 gol por jogo; **Figura 6**). Somados os pontos pelo critério 3/1/0, os mandantes totalizaram 12.554 pontos e os visitantes 7.166, resultando no índice de Pollard de **63,7%** — acima do limiar de neutralidade (50%), o que confirma a hipótese H1 para o período.

**Figura 5 — Distribuição dos resultados das 7.219 partidas da Série A, 2006–2024.**
(`figuras/fig1_distribuicao_geral.png`)
Legenda: mandante 49,0%; empates 26,8%; visitante 24,1%. Fonte: Elaboração própria, a partir da base validada.

**Figura 6 — Média de gols por partida de mandantes e visitantes por temporada, 2006–2024.**
(`figuras/fig4_gols_temporadas.png`)
Legenda: período — casa 1,49 × fora 1,00. Fonte: Elaboração própria, a partir da base validada.

## 5.2 Variação entre temporadas

O índice anual variou de **58,2% (2017; IC 95% 53,4–62,6)** a **69,5% (2018; IC 65,4–73,5)**, sem nenhum ano abaixo de 50% nem no limite inferior (**Figura 7**, **Figura 8**, Tabela 1). A amplitude de 11,3 p.p. entre dois anos adjacentes, porém, é um retrato de extremos: os ICs anuais têm largura média de cerca de 9 p.p. e se sobrepõem em boa parte da série. Mais informativo que a amplitude é a **mudança de nível**: o índice médio cai de 64,9% em 2006–2018 para 61,0% em 2019–2024 (diferença de 3,9 p.p.; IC 95% 2,1–5,6), e a comparação 2006–2016 vs. 2022–2024 repete o padrão (65,1% vs. 60,6%; diferença de 4,5 p.p.; IC 3,0–6,0 — com apenas três temporadas no segundo grupo, o IC por cluster é exploratório). O melhor ponto de quebra da série é **2019**; a mudança coincide com a estreia do VAR e antecede a pandemia, sem que o desenho permita separar os dois choques. A hipótese H2, portanto, se sustenta em uma forma mais forte que a simples não-constância: há uma queda de nível sustentada, não apenas oscilação anual (**Figura 9**).

A temporada 2017 combina o menor Pollard com o maior percentual de vitórias visitantes da série (28,9%); a de 2018, o maior Pollard com o menor percentual de vitórias visitantes (17,9%). O espelho entre os dois anos mostra que a oscilação passa sobretudo pelo desempenho dos visitantes, não pelos empates.

**Figura 7 — Índice de vantagem em casa de Pollard por temporada, 2006–2024.**
(`figuras/fig2_pollard_temporadas.png`)
Legenda: variação de 58,2% (2017) a 69,5% (2018); linha tracejada = 50% (neutralidade). Fonte: Elaboração própria, a partir da base validada.

**Figura 8 — Proporção de vitórias do mandante, empates e vitórias do visitante por temporada, 2006–2024.**
(`figuras/fig3_resultados_temporadas.png`)
Legenda: barras de 100% empilhadas. Fonte: Elaboração própria, a partir da base validada.

**Figura 9 — Série anual do índice de Pollard com IC 95% e médias pré/pós-2019, 2006–2024.**
(`figuras/fig9_serie_ic.png`)
Legenda: linha = Pollard anual; faixa = IC 95% por bootstrap de partidas; linhas tracejadas = médias 2006–2018 (64,9%) e 2019–2024 (61,0%); marcador vertical = 2019. Fonte: Elaboração própria, a partir da base validada.

**Tabela 1 — Indicadores por temporada, 2006–2024.**
(`figuras/tab1_indicadores_temporada.csv`; CSV com ponto decimal, texto com vírgula)

| Temporada | n | % V mandante | % Empates | % V visitante | Gols casa | Gols fora | Dif. gols | Pontos casa | Pontos fora | Pollard | IC 95% Pollard |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2006 | 380 | 50,26 | 25,53 | 24,21 | 1,59 | 1,12 | 0,47 | 670,00 | 373,00 | 64,24 | 59,83–68,53 |
| 2007 | 380 | 50,53 | 23,68 | 25,79 | 1,67 | 1,09 | 0,58 | 666,00 | 384,00 | 63,43 | 58,99–68,20 |
| 2008 | 380 | 54,74 | 25,26 | 20,00 | 1,73 | 0,99 | 0,74 | 720,00 | 324,00 | 68,97 | 64,70–73,25 |
| 2009 | 380 | 51,32 | 26,84 | 21,84 | 1,73 | 1,14 | 0,59 | 687,00 | 351,00 | 66,18 | 62,00–70,57 |
| 2010 | 380 | 47,11 | 31,05 | 21,84 | 1,53 | 1,04 | 0,48 | 655,00 | 367,00 | 64,09 | 59,72–68,24 |
| 2011 | 380 | 48,42 | 27,63 | 23,95 | 1,61 | 1,07 | 0,53 | 657,00 | 378,00 | 63,48 | 58,82–67,98 |
| 2012 | 380 | 48,16 | 27,63 | 24,21 | 1,47 | 1,00 | 0,47 | 654,00 | 381,00 | 63,19 | 58,68–67,68 |
| 2013 | 380 | 48,42 | 28,42 | 23,16 | 1,47 | 0,99 | 0,47 | 660,00 | 372,00 | 63,95 | 59,54–68,31 |
| 2014 | 380 | 51,84 | 24,21 | 23,95 | 1,42 | 0,84 | 0,58 | 683,00 | 365,00 | 65,17 | 60,67–69,63 |
| 2015 | 380 | 52,63 | 23,95 | 23,42 | 1,46 | 0,90 | 0,56 | 691,00 | 358,00 | 65,87 | 61,34–70,73 |
| 2016 | 379 | 53,30 | 24,80 | 21,90 | 1,49 | 0,92 | 0,57 | 700,00 | 343,00 | 67,11 | 62,82–71,39 |
| 2017 | 380 | 43,95 | 27,11 | 28,95 | 1,38 | 1,04 | 0,34 | 604,00 | 433,00 | 58,24 | 53,42–62,56 |
| 2018 | 380 | 53,16 | 28,95 | 17,89 | 1,38 | 0,79 | 0,59 | 716,00 | 314,00 | 69,51 | 65,41–73,52 |
| 2019 | 380 | 48,42 | 25,79 | 25,79 | 1,38 | 0,92 | 0,46 | 650,00 | 392,00 | 62,38 | 57,86–67,09 |
| 2020 | 380 | 45,00 | 28,42 | 26,58 | 1,41 | 1,07 | 0,34 | 621,00 | 411,00 | 60,17 | 55,64–64,67 |
| 2021 | 380 | 45,79 | 29,74 | 24,47 | 1,27 | 0,94 | 0,33 | 635,00 | 392,00 | 61,83 | 57,54–66,35 |
| 2022 | 380 | 44,21 | 28,42 | 27,37 | 1,41 | 0,98 | 0,43 | 612,00 | 420,00 | 59,30 | 54,70–63,80 |
| 2023 | 380 | 46,84 | 25,79 | 27,37 | 1,42 | 1,07 | 0,35 | 632,00 | 410,00 | 60,65 | 56,14–65,28 |
| 2024 | 380 | 47,37 | 26,58 | 26,05 | 1,41 | 1,03 | 0,38 | 641,00 | 398,00 | 61,69 | 57,14–66,28 |

Fonte: Elaboração própria, a partir da base validada.

Dois anos merecem registro metodológico. Em **2016** (n = 379), falta o confronto Chapecoense × Atlético-MG, cancelado após a tragédia do voo — documentado, sem imputação. Em **2020** (n = 380), a temporada estendeu-se até 25/02/2021, sem torcida. O índice de 60,2% (IC 55,6–64,7) não é o piso da série: 2017 (58,2%) e 2022 (59,3%; IC 54,7–63,8) são menores. A leitura correta é que 2020 faz parte do patamar pós-2019, não de uma anomalia isolada; a literatura do período (RIBEIRO et al., 2022) associa a queda ao conjunto torcida ausente + VAR + calendário atípico, sem atribuir causalidade isolada — posição adotada aqui.

## 5.3 Discussão frente à literatura

O valor do período (63,7%) é compatível com o patamar brasileiro reportado por Almeida et al. (2011) para a Série A em 2003–2009 (65 ± 2,3%): situa-se dentro do intervalo 62,7–67,3%, abaixo do qual este trabalho estende a série com granularidade anual. Essa compatibilidade é relevante porque as janelas se sobrepõem parcialmente (2006–2009 em comum) sem compartilhar fonte nem pipeline — duas medições independentes convergindo para a mesma faixa. A persistência acima de 50% em todas as 19 temporadas reforça o caráter estrutural do fenômeno no recorte, sem que se possa afirmar causa: torcida, arbitragem e clima não são medidos; da viagem, só a distância entre sedes; a força dos elencos é aproximada pela posição na tabela (ver Limitações, capítulo 6).

A granularidade anual revela o que o agregado esconde. A amplitude de 11,3 p.p. entre 2017 (58,2%) e 2018 (69,5%) é um retrato de dois extremos, não uma medida robusta de variação: os ICs anuais se sobrepõem em boa parte da série e a diferença entre anos adjacentes não é estável. O que a série mostra com mais força é a mudança de nível pós-2018 — 64,9% em 2006–2018 contra 61,0% em 2019–2024 (diferença de 3,9 p.p.; IC 2,1–5,6) — já descrita em §5.2. O espelho 2017/2018 — menor Pollard com maior percentual de vitórias visitantes (28,9%) e maior Pollard com menor percentual de visitantes vencedores (17,9%) — sugere que a oscilação passa sobretudo pelo desempenho dos visitantes, não pelos empates. Nenhum ano cai abaixo de 50%, de modo que H2 se sustenta descritivamente; a forma mais forte, porém, é a mudança de nível, não a amplitude.

A temporada 2020 (60,2%) merece leitura à luz de Ribeiro et al. (2022): disputada até 25/02/2021, sem torcida, com estreia do VAR na Série A em 2019 e calendário atípico. Os autores associam a queda do período pandêmico ao conjunto torcida ausente + VAR + calendário, sem atribuir causalidade isolada — posição mantida aqui. Duas cautelas: a escala de Ribeiro et al. (((H−A)/A)×100%) não é o índice de Pollard, de modo que seus valores não se comparam ponto a ponto com a Tabela 1; e 2020, embora baixo, permanece acima do neutro. O ponto descritivo mais forte não é "o piso da série sob condições extremas" — 2017 é menor —, e sim que nem a conjunção de estádios vazios, VAR e calendário atípico apagou a vantagem; ao mesmo tempo, 2022–2024 mostram que a queda não terminou com a pandemia.

## 5.4 Fatores contextuais associados

A Tabela 5 reúne o Pollard por contexto da partida, com n e IC 95%. As variáveis são descritivas e calculadas sem tocar em placar ou mando (`src/context.py`): distância entre cidades-sede (haversine; clássicos = 0), clássico, mesma unidade federativa, estádio mais frequente da equipe na temporada, diferença de descanso (apenas Série A) e posição relativa na tabela antes da partida. A Figura 10 resume os mesmos grupos. Nenhuma leitura abaixo é causal.

**Viagem e clássico.** Não há associação relevante com a distância: 63,4% nas curtas, 63,8% nas médias e 63,9% nas longas — diferença de 0,5 p.p., muito menor que a amplitude anual. A comparação mais informativa é o clássico: 458 partidas entre clubes da mesma cidade, com deslocamento zero, registram 58,2% (IC 53,99–62,45), contra 64,0% nos não clássicos (IC 62,95–65,05); a diferença é de −5,8 p.p. (IC −11,3 a −0,7, bootstrap por temporada). Mesmo sem viagem, o mandante mantém 8,2 p.p. de vantagem sobre o neutro. Uma fração da diferença é compatível com a viagem, mas não o grosso. O mesmo estado vs. estado diferente (62,1% vs. 63,8%; diferença −1,8 p.p.; IC −5,6 a 1,8) aponta na mesma direção, com incerteza que inclui zero. O resultado dialoga com Pollard, Silva e Medeiros (2008), que estimaram 0,1 gol de diferença a cada 1.000 km — efeito pequeno em gols, abaixo da resolução da régua de pontos.

**Estádio habitual.** Jogos no estádio mais frequente da equipe na temporada somam 64,1% (IC 63,04–65,15), contra 59,4% em outro estádio (IC 55,78–62,91); a diferença bruta é de 4,7 p.p. (IC 1,8–8,1). Parte disso pode refletir composição de adversários e público, não familiaridade. A comparação dentro de equipe-temporada — cada partida contra a média do próprio clube nos jogos em casa da temporada — reduz a diferença para 0,13 ponto por jogo (usual +0,012; outro −0,116). É uma diferença modesta, compatível com familiaridade e com público, mas insuficiente para responder pelos 13,7 p.p. do agregado.

**Descanso.** A relação não é monotônica: descanso igual 65,1%; mandante +1–2 dias 62,7%; mandante +3 dias 60,3%; visitante +1–2 dias 61,2%; visitante +3 dias 65,1%. Dentro de equipe-temporada, os desvios são pequenos e não ordenados (+0,024 no igual; −0,020 em casa +1–2; −0,099 em casa +3; −0,035 fora +1–2; +0,028 fora +3). O indicador cobre apenas partidas da Série A; não mede copa, Libertadores ou estaduais, e a primeira partida de cada clube na temporada não é tratada como descanso (entressafra). A leitura defensável é que não há evidência de que mais descanso do mandante aumente o índice; a afirmação anterior de "gradação" não se sustenta.

**Força na tabela.** O favorito (mandante ao menos 4 posições melhor) registra 73,3% (IC 71,66–74,99); o equilibrado, 62,8%; a zebra (mandante ao menos 4 posições pior), 55,6% (IC 53,91–57,47). A diferença favorito−zebra é de 17,7 p.p. (IC 14,9–20,6). Dentro de equipe-temporada, o favorito soma +0,081 ponto/jogo e a zebra −0,047. A força está associada à heterogeneidade entre confrontos, mas não há evidência de que explique o nível agregado: mesmo quando o mandante é pior, o índice fica 5,6 p.p. acima do neutro. Como o calendário é balanceado, a qualidade dos elencos não é suficiente para explicar, sozinha, por que os mandantes somam mais pontos no agregado.

**Era e pandemia.** O pré-2019 tem 64,9% (IC 63,64–66,08); o pós-2019, 61,0% (IC 59,21–62,89). As temporadas pandêmicas (2020–2021) têm 61,0% (IC 57,83–64,25) contra 64,0% das demais (IC 62,85–64,99; diferença −3,0 p.p.; IC −4,7 a −1,1 — com apenas duas temporadas no grupo pandêmico, o IC por cluster é exploratório). A queda, porém, não termina com a pandemia: 2022–2024 têm 60,6%. O desenho não separa VAR, pandemia, calendário e mudanças táticas; a conclusão é descritiva: há uma mudança de nível que coincide com um conjunto de choques, não com um deles isoladamente. Na mesma era, o índice acompanha a presença de público: 62,4% em 2019 (torcida cheia), 60,2% em 2020 (portões fechados) e 61,8% em 2021 (retorno parcial) — gradiente sugestivo, sem leitura causal.

**Heterogeneidade entre equipes.** A Tabela 6 mostra os extremos entre equipes com pelo menos cinco temporadas. Athletico-PR (1,01 ponto/jogo; IC 0,82–1,19), Juventude (0,96; 0,63–1,28), Náutico (0,95; 0,58–1,28), Sport (0,95; 0,72–1,17) e Coritiba (0,95; 0,72–1,17) têm as maiores diferenças casa−fora; Flamengo (0,61; 0,43–0,79), Figueirense (0,59; 0,30–0,85), Botafogo (0,58; 0,39–0,77), Chapecoense (0,57; 0,30–0,87) e Atlético-GO (0,36; 0,10–0,64) têm as menores. A correlação ítem-par entre temporadas ímpares e pares é 0,46: há alguma estabilidade, mas também muito ruído. O ranking não mede "força em casa" e sim dependência relativa do mando; clubes que vencem fora com frequência, como o Flamengo, aparecem com diferença menor. Amostras de uma temporada (Barueri, Ipatinga etc.) têm IC largo e não entram na tabela.

**Orçamento de explicações.** Os limites não são aditivos, porque os mecanismos se sobrepõem. A associação com viagem/clássico pode chegar a ~5,8 p.p.; o estádio habitual, a uma diferença de poucos pontos percentuais na comparação dentro de equipe-temporada; a força, a ~0 no agregado; a era/pandemia, a ~3–4 p.p., confundida com VAR e calendário. O clássico sem viagem mantém 8,2 p.p. acima do neutro e o mandante zebra mantém 5,6 p.p.; esses dois resultados, por si sós, mostram que viagem e força não explicam o nível. O resíduo que sobra para torcida, arbitragem, clima e gramado é grande. A conclusão é multifatorial: não há uma causa única nos dados; há um conjunto de associações modestas e um resíduo que este desenho não atribui.

**Tabela 5 — Pollard por contexto da partida, 2006–2024.**

| Dimensão | Grupo | n | Pollard (IC 95%) |
|---|---|---:|---|
| Geral | Período 2006–2024 | 7.219 | 63,66 (62,63–64,70) |
| Clássico | Clássico (mesma cidade) | 458 | 58,23 (53,99–62,45) |
| Clássico | Não clássico | 6.761 | 64,02 (62,95–65,05) |
| Distância | Curta (<500 km) | 2.670 | 63,37 (61,73–65,06) |
| Distância | Média (500–1.499 km) | 3.137 | 63,80 (62,28–65,40) |
| Distância | Longa (≥1.500 km) | 1.412 | 63,90 (61,74–66,18) |
| Mesmo estado | Mesmo estado | 746 | 62,07 (58,75–65,24) |
| Mesmo estado | Estado diferente | 6.473 | 63,84 (62,79–64,89) |
| Estádio | Estádio habitual | 6.543 | 64,10 (63,04–65,15) |
| Estádio | Outro estádio | 676 | 59,40 (55,78–62,91) |
| Descanso | Igual | 3.452 | 65,14 (63,63–66,59) |
| Descanso | Casa +1–2 dias | 1.493 | 62,68 (60,36–64,92) |
| Descanso | Casa +3 dias | 263 | 60,31 (54,83–65,55) |
| Descanso | Fora +1–2 dias | 1.554 | 61,20 (59,02–63,51) |
| Descanso | Fora +3 dias | 263 | 65,13 (60,03–70,31) |
| Força na tabela | Favorito | 2.323 | 73,34 (71,66–74,99) |
| Força na tabela | Equilibrado | 2.289 | 62,81 (60,98–64,63) |
| Força na tabela | Zebra | 2.607 | 55,65 (53,91–57,47) |
| Era | Pré-2019 | 4.939 | 64,88 (63,64–66,08) |
| Era | 2019+ | 2.280 | 61,01 (59,21–62,89) |
| Pandemia | Demais temporadas | 6.459 | 63,97 (62,85–64,99) |
| Pandemia | Pandemia (2020–2021) | 760 | 61,00 (57,83–64,25) |

Fonte: Elaboração própria, a partir da base validada. IC 95% por bootstrap de partidas (2.000 reamostragens por grupo; 3.000 para o indicador geral). As linhas de descanso somam 7.025 partidas porque 194 partidas têm ao menos um clube em sua primeira partida da temporada; o intervalo de entressafra não foi tratado como descanso.

**Tabela 6 — Extremos da vantagem casa−fora por equipe (pelo menos cinco temporadas), 2006–2024.**

| Equipe | n | Casa − fora (pontos/jogo; IC 95%) |
|---|---:|---|
| Athletico-PR | 684 | 1,01 (0,82–1,19) |
| Juventude | 190 | 0,96 (0,63–1,28) |
| Nautico | 190 | 0,95 (0,58–1,28) |
| Sport | 418 | 0,95 (0,72–1,17) |
| Coritiba | 456 | 0,95 (0,72–1,17) |
| Flamengo | 722 | 0,61 (0,43–0,79) |
| Figueirense | 304 | 0,59 (0,30–0,85) |
| Botafogo-RJ | 646 | 0,58 (0,39–0,77) |
| Chapecoense | 265 | 0,57 (0,30–0,87) |
| Atletico-GO | 304 | 0,36 (0,10–0,64) |

Fonte: Elaboração própria, a partir da base validada. Lista completa em `figuras/tab6_equipes.csv`. A correlação ítem-par entre temporadas ímpares e pares é 0,46.

**Figura 10 — Pollard por contexto da partida (clássico, distância, mesma UF, estádio, descanso, força, era e pandemia), 2006–2024.**
(`figuras/fig10_contexto.png`)
Legenda: barras = Pollard do grupo; hastes = IC 95%; linha tracejada = 50% (neutralidade). Fonte: Elaboração própria, a partir da base validada.

## 5.5 Matriz de correlação

A Tabela 7 e a Figura 11 apresentam a matriz de Spearman por equipe-temporada. As correlações com os componentes do próprio HA são mecânicas — casa +0,57, fora −0,46 — e servem apenas para mostrar a composição do indicador; a leitura substantiva está nas variáveis de contexto. A distância média percorrida como visitante tem correlação −0,01, essencialmente nula. O estádio habitual tem +0,10, fraca. A temporada tem −0,19, compatível com a queda de nível pós-2018. Pontos (+0,08) e posição final (−0,08) também são praticamente nulos: a vantagem casa−fora não é um subproduto da força do elenco. Os gols seguem o mesmo padrão dos pontos: casa +0,35, fora −0,30.

No nível de partida, o saldo de gols correlaciona-se +0,19 com a diferença de posição na tabela, +0,03 com o estádio habitual, +0,01 com a distância, +0,01 com a diferença de descanso, −0,04 com o clássico, −0,05 com a era VAR e −0,03 com a pandemia. A única associação não trivial é a diferença de posição; as demais são fracas. A matriz reforça o padrão descritivo do capítulo: viagem e força não explicam o nível; o estádio habitual tem associação fraca; a temporada capta a mudança de nível. Torcida e arbitragem não entram na matriz porque não são medidas.

Como em toda correlação, associação não é causa. No nível de partida, as observações não são independentes (há dependência dentro de temporada, clube e confronto), de modo que os coeficientes são exploratórios; por isso a tabela principal é a de equipe-temporada, com 380 observações.

**Tabela 7 — Correlações de Spearman com a vantagem casa−fora por equipe-temporada, 2006–2024.**

| Variável | rho com HA | n |
|---|---:|---:|
| Casa pts/jogo | 0,57 | 380 |
| % vitórias casa | 0,54 | 380 |
| Fora pts/jogo | −0,46 | 380 |
| % vitórias fora | −0,45 | 380 |
| Gols casa/jogo | 0,35 | 380 |
| Gols fora/jogo | −0,30 | 380 |
| Temporada | −0,19 | 380 |
| % estádio habitual | 0,10 | 380 |
| Posição final | −0,08 | 380 |
| Pontos | 0,08 | 380 |
| Distância média | −0,01 | 380 |

Fonte: Elaboração própria, a partir da base validada. HA = pontos/jogo em casa − fora. Spearman com pares completos; n = 380 equipe-temporadas. As quatro primeiras linhas são componentes diretos do HA (pontos e vitórias); as duas seguintes (gols) são correlatos de desempenho; as linhas de contexto são distância, estádio, temporada, posição e pontos. A matriz completa (12×12) está em `figuras/matriz_equipe.csv`.

**Figura 11 — Matriz de correlação por equipe-temporada (Spearman), 2006–2024.**
(`figuras/fig11_correlacoes_equipe.png`)
Legenda: azul = correlação positiva; vermelho = negativa; intensidade proporcional ao rho; diagonal = 1. Fonte: Elaboração própria, a partir da base validada.

## 5.6 Público e arbitragem: evidência externa

A base principal não mede público nem arbitragem; por isso, a matriz da seção 5.5 não inclui esses canais. Para reduzir essa lacuna, foi montada uma base externa a partir da Base dos Dados/Transfermarkt (2006–2024) e do FBref (2024), unida à base do TCC por temporada, mandante, visitante e placar. A cobertura é de 6.618 partidas com registro de público (91,7% do total; 96,8% em 2007–2024) e 6.821 com árbitro (94,5%). O público não entra na matriz principal por três razões: 2006 não tem público, 2008 tem 217 zeros tratados como falha de registro e 2024 foi completado por outra fonte; a cobertura, portanto, não é homogênea nem aleatória. A análise é descritiva e não afirma causalidade.

**Tabela 8 — Público e índice de Pollard por bloco, 2007–2024.**

| Bloco | Jogos | Com registro | Público médio | Pollard (IC 95%) |
|---|---:|---:|---:|---:|
| 2007–2018 | 4.559 | 4.342 | 16.574 | 64,94 (63,66–66,21) |
| 2019 | 380 | 380 | 22.649 | 62,38 (57,80–66,95) |
| 2020 (portões fechados) | 380 | 380 | 0 | 60,17 (55,64–64,69) |
| 2021 (retorno parcial) | 380 | 380 | 6.524 | 61,83 (57,51–66,31) |
| 2022–2024 | 1.140 | 1.136 | 25.291 | 60,55 (57,90–63,26) |
| Total 2007–2024 | 6.839 | 6.618 | 16.890 | 63,63 (62,56–64,62) |

Fonte: Elaboração própria, a partir da base validada e da base externa (Base dos Dados/Transfermarkt e FBref). IC 95% por bootstrap de partidas (3.000 reamostragens); não considera a dependência dentro de temporada. O público médio usa apenas os jogos com registro; em 2020–2021, os zeros são registros reais de portões fechados; em 2008, 217 zeros foram tratados como ausentes.

O público médio sobe de 16.574 em 2007–2018 para 22.649 em 2019, cai a zero em 2020 e retorna a 25.291 em 2022–2024. O Pollard, porém, não acompanha essa trajetória: cai de 64,94% para 62,38% já em 2019, antes dos portões fechados; chega a 60,17% em 2020 e fica em 60,55% em 2022–2024, com público de volta. O retorno da torcida não devolveu o índice ao patamar pré-2019. A leitura é compatível com a mudança de nível da seção 5.2 e reforça a cautela contra atribuir a queda à torcida isoladamente: o declínio começa antes de 2020 e persiste depois.

**Tabela 9 — Associações do público com desempenho e vantagem de casa.**

| Nível | Relação | Spearman | n |
|---|---|---:|---:|
| Equipe-temporada | HA × público médio | 0,068 | 360 |
| Equipe-temporada | HA × público médio, sem 2020–2021 | −0,010 | 320 |
| Equipe-temporada | Pontos × público médio | 0,461 | 360 |
| Partida | Saldo de gols × público (bruto) | 0,079 | 6.618 |
| Partida | Saldo × público, controlando equipe-temporada e rank pré-jogo | −0,042 | 6.618 |

Fonte: Elaboração própria, a partir da base validada e da base externa. HA = pontos/jogo em casa − fora. Spearman com pares completos; n = 360 equipe-temporadas com registro (2006 não tem público) e 6.618 partidas. No nível de partida, o controle é a diferença de posição na tabela antes do jogo e a média da própria equipe na temporada.

No nível equipe-temporada, o público médio é um proxy forte de força do clube: a correlação com pontos é 0,461, e com o HA é 0,068; sem as temporadas pandêmicas, −0,010. Clubes com mais torcida não são os que mais dependem do mando. No nível de partida, a correlação bruta entre público e saldo de gols é 0,079, mas cai para −0,042 quando se compara o mesmo clube na mesma temporada e se controla a diferença de posição pré-jogo. A associação bruta é, portanto, composição de confrontos: jogos de maior público tendem a ser contra adversários mais fortes. Entre as partidas acima e abaixo da mediana de público da própria equipe-temporada, o grupo de maior público tem adversário médio na posição 9,82 contra 11,53, e o mandante chega relativamente mais fraco (rank diff −0,76 contra +0,09); o saldo médio é 0,429 contra 0,591. Isso não refuta a hipótese da torcida; mostra que a variação observada de público não é um experimento limpo. O contraste de 2020 é mais informativo, e nele a vantagem cai, mas não desaparece.

**Tabela 10 — Público médio e desempenho por quartil de público (times com pelo menos cinco temporadas), 2007–2024.**

| Quartil | Times | Público médio | Pontos/temporada | HA | Casa pts/jogo | Fora pts/jogo |
|---|---:|---:|---:|---:|---:|---:|
| Q1 (menor) | 7 | 6.461 | 43,1 | 0,657 | 1,463 | 0,806 |
| Q2 | 7 | 12.960 | 46,5 | 0,815 | 1,632 | 0,817 |
| Q3 | 7 | 18.074 | 52,7 | 0,762 | 1,769 | 1,007 |
| Q4 (maior) | 7 | 24.939 | 59,4 | 0,731 | 1,930 | 1,199 |

Fonte: Elaboração própria, a partir da base validada e da base externa. 28 equipes com pelo menos cinco temporadas; HA = pontos/jogo em casa − fora. Spearman público × pontos = 0,786; público × HA = 0,043. O público médio usa os jogos em casa com registro.

Os pontos sobem de 43,1 no Q1 para 59,4 no Q4, enquanto o HA fica entre 0,657 e 0,815, sem ordem monotônica: o Q4 tem 0,731, abaixo do Q2 (0,815). O público separa clubes grandes de pequenos, não clubes mais ou menos dependentes do mando. Flamengo (Q4) tem HA 0,59; Santos (Q2), 0,86; Atlético-GO (Q1), 0,36. A correlação entre público e pontos é 0,786; entre público e HA, 0,043.

**Figura 12 — Público médio, vantagem casa−fora e pontos médios por temporada por equipe (2007–2024).**
(`figuras/fig12_publico_ha.png`)
Legenda: cada ponto é uma equipe com pelo menos cinco temporadas; eixo x = público médio dos jogos em casa; painel esquerdo = HA (pontos/jogo em casa − fora); painel direito = pontos médios por temporada da equipe. Linhas = ajuste linear; ρ = Spearman. Fonte: Elaboração própria, a partir da base validada e da base externa.

A Figura 12 repete o padrão: a reta do HA é praticamente horizontal, enquanto a de pontos é ascendente.

**Arbitragem.** A base identifica 6.821 partidas com árbitro e 177 árbitros (nomes normalizados entre as fontes), com mediana de 14 jogos e máximo de 284. A taxa de vitória do mandante é 48,9%. Entre os 50 árbitros com pelo menos 40 jogos, a taxa varia de 40,8% a 67,4%, mas apenas 1 fica fora de ±2 desvios-padrão (esperado sob a hipótese nula: 2,3); a variação é compatível com ruído. Mais importante: a base registra quem apitou, não o que decidiu. Sem pênaltis e faltas por árbitro, o teste do viés arbitral permanece parcial; as faltas da Base dos Dados só existem a partir de 2018 e têm lacunas. A identidade do árbitro, sozinha, não mede viés; a extensão de cartões da seção 5.7 dá um passo adicional, mas ainda não cobre pênaltis nem decisões discricionárias.

**Síntese.** A evidência externa estreita o orçamento de explicações. O público não é o principal correlato da vantagem casa−fora no corte transversal; seu poder descritivo está em separar clubes grandes de pequenos. A Tabela 10 e a Figura 12 mostram que os pontos sobem com o público, mas o HA não. O contraste de 2020 sugere que a torcida contribui, mas não responde por todo o fenômeno, e o retorno do público em 2022–2024 não restaurou o patamar anterior. A arbitragem permanece parcialmente fora do alcance: a seção 5.7 mede cartões, mas não pênaltis ou decisões discricionárias. A conclusão multifatorial da seção 5.4 permanece: há associações modestas e um resíduo grande, que este desenho não atribui.

## 5.7 Cartões: um canal de arbitragem

A base principal não registra cartões; para aproximar o canal da arbitragem, foi montada uma base externa com os borderôs da CBF compilados pelo projeto BrazilianFootball/Data (licença MIT), cobrindo 2013–2024. A junção usa temporada, data, mandante, visitante e placar, com fallback por equipes e placar para jogos remarcados; a data canônica é sempre a da base do TCC. A cobertura é de 4.559 partidas de 2013–2024 (100% das partidas elegíveis), com um único cartão não atribuído, em 2022, por formato quebrado. As temporadas 2006–2012 não têm cartões nessa fonte, de modo que a extensão não cobre a série inteira.

Para cada partida, contaram-se amarelos e vermelhos de cada lado; a diferença casa−fora é a unidade descritiva. A Tabela 11 reporta a média por temporada e o IC 95% por bootstrap de partidas (4.000 reamostragens). Para o contraste 2019→2020, estimou-se `yellow_diff = post + efeitos fixos de mandante + efeitos fixos de visitante`, em que `post` indica 2020. Como as mesmas equipes se repetem, o erro-padrão usa a maior variância one-way clusterizada por mandante e por visitante — aproximação conservadora de Cameron e Miller (2015) — e o IC usa 1,96 EP. O desenho é quase-experimental e não isola torcida de pandemia, calendário, protocolos e VAR.

**Tabela 11 — Cartões por temporada, diferença casa−fora e IC 95%, 2013–2024.**

| Temporada | Jogos | Amarelos casa | Amarelos fora | Diferença (IC 95%) | Vermelhos casa | Vermelhos fora |
|---|---:|---:|---:|---|---:|---:|
| 2013 | 380 | 2,06 | 2,37 | −0,31 (−0,46 a −0,16) | 0,04 | 0,09 |
| 2014 | 380 | 2,14 | 2,31 | −0,16 (−0,34 a +0,01) | 0,09 | 0,12 |
| 2015 | 380 | 2,22 | 2,72 | −0,50 (−0,68 a −0,32) | 0,08 | 0,19 |
| 2016 | 379 | 2,06 | 2,50 | −0,44 (−0,61 a −0,27) | 0,07 | 0,15 |
| 2017 | 380 | 2,13 | 2,60 | −0,46 (−0,66 a −0,28) | 0,08 | 0,10 |
| 2018 | 380 | 2,30 | 2,55 | −0,25 (−0,41 a −0,07) | 0,09 | 0,16 |
| 2019 | 380 | 2,10 | 2,28 | −0,18 (−0,36 a +0,01) | 0,09 | 0,16 |
| 2020 | 380 | 2,24 | 2,13 | +0,11 (−0,06 a +0,29) | 0,13 | 0,14 |
| 2021 | 380 | 2,21 | 2,25 | −0,04 (−0,22 a +0,14) | 0,10 | 0,10 |
| 2022 | 380 | 2,22 | 2,62 | −0,41 (−0,60 a −0,22) | 0,11 | 0,16 |
| 2023 | 380 | 2,54 | 2,72 | −0,18 (−0,36 a +0,00) | 0,14 | 0,12 |
| 2024 | 380 | 2,42 | 2,71 | −0,28 (−0,47 a −0,10) | 0,16 | 0,16 |

Fonte: Elaboração própria, a partir da base validada e de BrazilianFootball/Data (MIT). IC 95% por bootstrap de partidas (4.000 reamostragens); a diferença é casa−fora. A coluna de jogos usa a base do TCC; 2016 tem 379 partidas. Cartões não atribuídos: 1 em 2022.

Em 2019, o mandante recebia 0,18 amarelo a menos que o visitante; em 2020, com portões fechados, a diferença passou a +0,11. A mudança bruta é +0,29. Com efeitos fixos de equipe, a estimativa é +0,35 (EP 0,190; IC 95% −0,03 a +0,72; n = 760). Restrita às 16 equipes presentes nos dois anos, +0,34 (EP 0,194; IC 95% −0,04 a +0,72; n = 480). O sinal é compatível com pressão da torcida sobre a arbitragem, mas o intervalo inclui zero: a evidência é sugestiva, não conclusiva ao nível de 5%.

**Figura 13 — Cartões amarelos casa−fora por temporada, com IC 95% e destaque para 2020 (2013–2024).**
(`figuras/fig13_cartoes.png`)
Legenda: linha azul = diferença média de amarelos casa−fora; faixa = IC 95% bootstrap; área vermelha = 2020, sem torcida. Fonte: Elaboração própria, a partir da base validada e de BrazilianFootball/Data (MIT).

A Figura 13 mostra que a diferença negativa é mais consistente em 2015–2018, encolhe em 2019 e cruza zero em 2020; depois oscila. O contraste de 2020 é o ponto mais informativo, mas também o mais confundido: a temporada teve calendário condensado, protocolos sanitários e ausência de torcida, e o VAR já estava em uso desde 2019. Cartões, além disso, são decisão do árbitro e também comportamento do jogador; a base não separa amarelos por reclamação, falta tática ou jogo perigoso, nem mede pênaltis.

**Síntese.** A extensão de cartões acrescenta um canal que a matriz principal não cobria, mas com poder limitado: o efeito estimado é positivo e modesto, e o IC inclui zero. Ela não muda a conclusão multifatorial; apenas mostra que a arbitragem não é invisível aos dados.

## 5.8 Resposta às perguntas de pesquisa

1. Proporção no período: 49,0% vitórias mandantes, 26,8% empates, 24,1% visitantes.
2. Sim: mandantes marcaram mais (1,49 vs. 1,00 por jogo, em todas as temporadas).
3. O índice de Pollard foi de 63,7% no período, com oscilação anual de 58,2% a 69,5% e uma mudança de nível pós-2018: 64,9% em 2006–2018 contra 61,0% em 2019–2024 (diferença de 3,9 p.p.; IC 2,1–5,6).
4. Sim, há diferenças descritivas relevantes entre temporadas e clubes; os extremos anuais são 2017 e 2018, e a Tabela 6 mostra a heterogeneidade entre equipes. A amplitude de 11,3 p.p. é um retrato de extremos; a mudança de nível é a leitura mais robusta.
5. O mando cresce com a viagem? Não de forma relevante: 63,4%–63,9% nas três faixas e 58,2% nos clássicos sem viagem. O estádio habitual mostra 4,7 p.p. de diferença bruta (0,13 ponto/jogo na comparação dentro de equipe-temporada). O descanso não é monotônico. A força na tabela está associada à heterogeneidade (favorito 73,3% vs. zebra 55,6%), mas não há evidência de que explique o nível agregado; mesmo a zebra fica acima de 50%.
6. Por que a vantagem é grande? Os dados permitem dizer o que **não** é o principal: viagem, descanso e qualidade dos elencos não explicam o agregado. O estádio habitual está associado a uma diferença modesta. A torcida é aproximada pelo público externo, mas não medida diretamente; a arbitragem é conhecida pela identidade e, a partir de 2013, pelos cartões. O resíduo é grande e a conclusão é multifatorial.
7. O que a matriz de correlação acrescenta? Por equipe-temporada, o HA correlaciona-se +0,57 com o desempenho em casa e −0,46 com o desempenho fora (componentes mecânicos), mas apenas −0,01 com a distância média, +0,10 com o estádio habitual, +0,08 com pontos e −0,08 com posição. No nível de partida, a maior associação contextual é com a diferença de posição (+0,19); distância, descanso, clássico, estádio e era ficam entre −0,05 e +0,03.
8. O que a extensão de cartões acrescenta? Em 2019 o mandante recebia 0,18 amarelo a menos; em 2020, +0,11. A mudança com efeitos fixos de equipe é +0,35, mas o IC 95% (−0,03 a +0,72) inclui zero. O resultado é sugestivo do canal arbitral, não conclusivo; pênaltis e decisões discricionárias seguem fora do alcance.

---

# 6 CONCLUSÃO

## 6.1 Resposta à pergunta

No período 2006–2024 (7.219 partidas), os mandantes somaram mais pontos que os visitantes em todas as temporadas: índice de Pollard geral de 63,7% (IC 95% 62,6–64,7), variando de 58,2% (2017) a 69,5% (2018). Mandantes venceram 49,0% dos jogos e marcaram 1,49 gol por partida, contra 24,1% e 1,00 dos visitantes. Respondendo diretamente à pergunta de pesquisa: a magnitude da vantagem de jogar em casa na Série A foi de 13,7 pontos percentuais acima da neutralidade no agregado do período. As hipóteses se confirmam no plano descritivo: H1, porque 63,7% supera 50%; a diferença acumulada entre mandantes e visitantes foi de 5.388 pontos (12.554 vs. 7.166), e a margem sobre o limiar de 50% é de 2.694 pontos; H2, porque a série anual oscila de 58,2% a 69,5% sem jamais tocar o neutro. A forma mais forte de H2, porém, é a mudança de nível: 64,9% em 2006–2018 contra 61,0% em 2019–2024 (diferença de 3,9 p.p.; IC 2,1–5,6), com 2022–2024 em 60,6%. Nenhuma temporada inverteu o mando, nem mesmo 2020 sob estádios vazios; mas a vantagem não é uma constante — ela caiu de patamar e não voltou ao nível anterior.

As hipóteses contextuais H3–H5 também se sustentam descritivamente: a viagem não é o principal (clássicos sem deslocamento ainda têm 58,2%; as faixas de distância ficam entre 63,4% e 63,9%), o estádio habitual mostra 4,7 p.p. de diferença bruta (0,13 ponto/jogo na comparação dentro de equipe-temporada) e a mudança de nível pós-2018 é o padrão mais robusto da série. A força na tabela está associada à heterogeneidade entre confrontos (favorito 73,3% vs. zebra 55,6%), mas não há evidência de que explique o nível agregado. Não há uma causa única nos dados: há associações modestas e um resíduo grande, que a literatura associa a torcida, arbitragem, clima e gramado. A base externa aproxima a torcida pelo público: o público médio acompanha a força do clube (0,46 com pontos), não o HA (0,07; −0,01 sem 2020–2021); os pontos sobem de 43,1 para 59,4 do menor para o maior quartil de público, enquanto o HA fica entre 0,66 e 0,82, sem tendência. O contraste de 2020 mostra queda sem desaparecimento; a arbitragem é conhecida pela identidade do árbitro e, em 2013–2024, pelos cartões, mas não por pênaltis ou decisões discricionárias. A extensão de cartões encontra +0,35 na mudança casa−fora em 2020, com IC 95% −0,03 a +0,72: o canal segue sugestivo, não conclusivo. A matriz de correlação reforça o quadro: por equipe-temporada, o HA tem correlação quase nula com distância média (−0,01), pontos (0,08) e posição (−0,08), fraca com estádio habitual (0,10) e negativa moderada com a temporada (−0,19); no nível de partida, a maior associação contextual é a diferença de posição (+0,19), e as demais ficam entre −0,05 e +0,03.

## 6.2 Contribuição

Série anual homogênea de 19 temporadas, tratamento documentado e auditado, validação cruzada externa de 99,96%, uma decomposição descritiva dos fatores associados, uma aproximação externa de público, uma extensão de cartões (2013–2024) e uma matriz de correlação por equipe-temporada e por partida e um dashboard reutilizável para exploração — artefato que permanece útil após a defesa. Para a área de Sistemas de Informação, a contribuição é o encadeamento completo dado → indicador → decisão assistida: pipeline reproduzível com verificação de integridade, métricas puras e testadas, visualização em português, intervalos de confiança e rastreabilidade de cada requisito até sua evidência (Tabela 3). Para a literatura sobre vantagem em casa no Brasil, a contribuição é a série anual contínua mais longa com base auditada e validação externa, acompanhada de uma leitura que separa o que os dados permitem dizer (viagem não é o principal; estádio e força modulam; há mudança de nível pós-2018) do que eles não permitem (atribuir a queda ao VAR, à pandemia ou à torcida).

## 6.3 Limitações

A análise é observacional, baseada em placar e mando nominal: a torcida não é medida diretamente, a arbitragem é conhecida pela identidade do árbitro e, em 2013–2024, pelos cartões, e elenco e clima não são medidos. O público externo cobre 91,7% das partidas (96,8% em 2007–2024), com 2006 ausente, 217 zeros de 2008 tratados como falha e 2024 completado pelo FBref; por isso não entra na matriz principal. A base de público é um proxy, não uma medida de torcida: pode misturar pagante e total e depende de adversário, fase e preço. A análise contextual acrescenta proxies, não medições diretas: distância entre cidades-sede (não modo, tempo ou fadiga de viagem), estádio mais frequente da equipe na temporada (não o estádio próprio em todos os jogos), descanso apenas entre partidas da Série A (não copa, Libertadores ou estaduais) e posição na tabela antes da partida (não expectativa pré-jogo). O mando nominal nem sempre corresponde ao estádio habitual; o estádio alternativo confunde familiaridade e público. A posição na tabela antes da partida usa a ordem (data, rodada, match_id); em jogos da mesma rodada no mesmo dia, a ordem é arbitrária e resultados anteriores da mesma rodada podem entrar na posição. A mudança de nível pós-2018 coincide com a estreia do VAR e a pandemia; o desenho não separa os choques. A vantagem por equipe tem correlação ítem-par de 0,46: parte da variação é ruído, e rankings de clubes com poucas temporadas não são estáveis. A matriz de correlação é descritiva e não usa p-valores; no nível de partida, as observações não são independentes (dependência dentro de temporada, clube e confronto), de modo que seus coeficientes são exploratórios. A matriz por equipe-temporada tem 380 observações e é a leitura principal. A base histórica pode conter omissões (o relatório de qualidade integra o trabalho); não há inferência causal nem valor preditivo. A extensão de cartões cobre 2013–2024, não 2006–2012; um cartão ficou sem atribuição em 2022. Cartões refletem arbítrio e comportamento do jogador, e 2020 concentra pandemia, calendário e protocolos; o IC do contraste inclui zero, de modo que o canal arbitral é sugestivo, não conclusivo. Pênaltis e decisões discricionárias não são observados. Acrescentam-se três limites de escopo. Primeiro, o recorte exclui 2003–2005 (formato com mais de 20 clubes) e 2025 (temporada incompleta na data de acesso), de modo que nada se afirma fora de 2006–2024. Segundo, a fonte primária não tem licença explícita, o que restringe a redistribuição do bruto e condiciona a reprodução ao download pinado — limitação jurídica, não técnica, mitigada pelo plano B documentado. Terceiro, a validação externa cobre apenas 2018–2024 (limite do OpenFootball); as temporadas 2006–2017 dependem da auditoria interna, rigorosa mas de fonte única.

## 6.4 Trabalhos futuros

A agenda imediata é ampliar a cobertura de público (borderôs da CBF para 2006, 2008 e os jogos faltantes de 2024) e completar as decisões de arbitragem: a extensão de cartões já cobre 2013–2024, mas faltam 2006–2012, pênaltis e faltas por árbitro. O piloto 2019–2020 já compara cartões do mandante e do visitante com e sem torcida; acrescentar pênaltis fecharia o canal. Outra frente é usar odds ou Elo como controle de expectativa pré-jogo, para separar vantagem de mando de qualidade esperada. Com público mais completo e decisões de arbitragem, a matriz de correlação pode incorporar essas variáveis e testar se elas deslocam as associações hoje quase nulas de distância e força. A extensão às Séries B–D, na linha de Almeida et al. (2011), verificaria se a hierarquia entre divisões persiste duas décadas depois, com a mesma régua. E a atualização anual do pipeline é a extensão mais barata: o fluxo aceita novas temporadas sem mudança de código, bastando refazer o download pinado e reconstruir — o que manteria a série viva a cada dezembro.

---

# REFERÊNCIAS

ALMEIDA, L. G.; OLIVEIRA, M. L.; SILVA, C. D. Uma análise da vantagem de jogar em casa nas duas principais divisões do futebol profissional brasileiro. *Revista Brasileira de Educação Física e Esporte*, v. 25, n. 1, p. 49–54, 2011. DOI: 10.1590/S1807-55092011000100006 (CC BY-NC 4.0).

BASE DOS DADOS. *Brasileirão Série A*. Tabela `basedosdados.mundo_transfermarkt_competicoes.brasileirao_serie_a`, elaborada a partir do Transfermarkt. Disponível em: https://basedosdados.org/dataset/c861330e-bca2-474d-9073-bc70744a1b23. Acesso em: 20 nov. 2026.

BRAZILIANFOOTBALL/DATA. *BrazilianFootball/Data*: results and match cards from Brazilian football. GitHub, commit `0dd1bc5`. DOI: 10.5281/zenodo.15207727. Disponível em: https://github.com/BrazilianFootball/Data. Acesso em: 20 nov. 2026. (MIT).

CAMERON, A. C.; MILLER, D. L. A practitioner's guide to cluster-robust inference. *Journal of Human Resources*, v. 50, n. 2, p. 317–372, 2015. DOI: 10.3368/jhr.50.2.317.

DUQUE, A. *Brasileirao_Dataset* — Campeonato Brasileiro de Futebol, 2003–2024. GitHub, commit `15f027c`. Disponível em: https://github.com/adaoduque/Brasileirao_Dataset. Acesso em: 28 out. 2026. (sem licença explícita; uso conforme arquivo de proveniência).

EFRON, B.; TIBSHIRANI, R. J. *An introduction to the bootstrap*. New York: Chapman & Hall, 1993.

FBREF. *2024 Série A Scores & Fixtures*. Sports Reference. Disponível em: https://fbref.com/en/comps/24/2024/schedule/2024-Serie-A-Scores-and-Fixtures. Acesso em: 20 nov. 2026.

FEW, S. *Information dashboard design*: the effective visual communication of data. Sebastopol: O'Reilly Media, 2006. Cap. 1 (§1.3.1), Cap. 3 e Cap. 5 (§5.1).

GIL, A. C. *Métodos e técnicas de pesquisa social*. 6. ed. São Paulo: Atlas, 2008.

MATOS, R. M.; AMARO, N.; POLLARD, R. How best to quantify home advantage in team sports. *RICYDE*, v. 16, n. 59, p. 12–23, 2020. DOI: 10.5232/ricyde2020.05902 (acesso aberto).

NEAVE, N.; WOLFSON, S. Testosterone, territoriality, and the 'home advantage'. *Physiology & Behavior*, v. 78, n. 2, p. 269–275, 2003. DOI: 10.1016/S0031-9384(02)00969-1.

NEVILL, A. M.; BALMER, N. J.; WILLIAMS, A. M. The influence of crowd noise and experience upon refereeing decisions in football. *Psychology of Sport and Exercise*, v. 3, n. 4, p. 261–272, 2002. DOI: 10.1016/S1469-0292(01)00033-4.

OPENFOOTBALL. South America (Brazil). Domínio público, CC0-1.0, commit `f51b2dc`. Disponível em: https://github.com/openfootball/south-america. Acesso em: 28 out. 2026.

POLLARD, R. Home advantage in soccer: a retrospective analysis. *Journal of Sports Sciences*, v. 4, n. 3, p. 237–248, 1986. DOI: 10.1080/02640418608732122. (Original em paywall — citado via *apud* ALMEIDA et al., 2011; método documentado em MATOS; AMARO; POLLARD, 2020.)

POLLARD, R.; SILVA, C. D.; MEDEIROS, N. C. Home advantage in football in Brazil: differences between teams and the effects of distance traveled. *Brazilian Journal of Soccer Science*, v. 1, n. 1, p. 3–10, 2008. Disponível em: https://rbf.ufv.br/index.php/RBFutebol/article/view/6. Acesso em: 6 nov. 2026.

RIBEIRO, L. C. et al. Did the absence of crowd support during the Covid-19 pandemic affect the home advantage in Brazilian elite soccer? *Journal of Human Kinetics*, v. 81, p. 251–258, 2022. DOI: 10.2478/hukin-2022-0047. PMC8884879.

SHARDA, R.; DELEN, D.; TURBAN, E. *Business intelligence e análise de dados para gestão do negócio*. 4. ed. Porto Alegre: Bookman, 2019. Cap. 2 (§§2.8, 2.9, 2.11) e Cap. 3.

SILVA, C. D.; MOREIRA, D. G. A vantagem em casa no futebol: comparação entre o Campeonato Brasileiro e as principais ligas nacionais do mundo. *Revista Brasileira de Cineantropometria e Desempenho Humano*, v. 10, n. 2, p. 184–188, 2008. DOI: 10.1590/1980-0037.2008v10n2p184 (CC BY 4.0).

STREAMLIT. *Documentação oficial*. Acesso em: 4 nov. 2026. https://docs.streamlit.io/

> Nota: NEVILL; HOLDER (1999) segue citado apenas via *apud* ALMEIDA et al. (2011) (original não consultado); a entrada de NEVILL et al. (2002) acima é obra distinta, sobre ruído da torcida e arbitragem.

## APÊNDICE A — Dicionário de dados

Base limpa `data/processed/matches_processed.csv`, gerada por `scripts/build_processed.py` a partir de `data/raw/campeonato-brasileiro-full.csv` (ver `data/raw/FONTE.md` e `docs/auditoria_fase1.md`). Uma linha por partida válida, Série A 2006–2024.

| Coluna | Tipo | Obrigatório | Descrição |
|---|---|---:|---|
| `match_id` | texto | Sim | ID original da partida na fonte (`ID`). Chave única. |
| `season` | inteiro | Sim | Temporada atribuída por intervalo entre partidas (não por ano civil — a temporada 2020 termina em 25/02/2021). 2006–2024. |
| `date` | data ISO (`YYYY-MM-DD`) | Sim | Data da partida. |
| `round` | inteiro | Sim | Rodada **original** da fonte (`rodata`, com typo no original). Jogos reagendados mantêm a rodada original. |
| `home_team` | texto | Sim | Clube designado mandante (nome da fonte, sem acentos). |
| `away_team` | texto | Sim | Clube designado visitante. Diferente de `home_team` em todas as linhas. |
| `home_goals` | inteiro ≥ 0 | Sim | Gols do mandante. Nunca preenchido a partir de ausente. |
| `away_goals` | inteiro ≥ 0 | Sim | Gols do visitante. |
| `result` | `H`/`D`/`A` | Sim | Resultado recalculado do placar: vitória mandante / empate / vitória visitante. |
| `home_points` | 0/1/3 | Sim | Pontos do mandante (3/1/0). |
| `away_points` | 0/1/3 | Sim | Pontos do visitante. |
| `stadium` | texto | Não | Arena da fonte (espaços removidos na limpeza). |
| `source` | texto | Sim | Rastreabilidade: `Brasileirao_Dataset commit 15f027c (acesso 2026-10-28)`. |

Regras aplicadas: data inválida, placar ausente/não-numérico/negativo/fracionário, mandante = visitante ou clube vazio → linha excluída e contabilizada em `quality_report.json`; placar ausente **nunca** vira 0–0; duplicatas (`match_id`, linha integral ou tripla data/mandante/visitante) mantêm a primeira e registram o resto (zero ocorrências na base atual); `result` e pontos vêm do placar, com o campo `vencedor` da fonte servindo só para auditoria; filtro de recorte 2006–2024 (1.566 linhas de 2003–2005 e 2025 excluídas).

Casos conhecidos: **2016:** 379 partidas (falta Chapecoense × Atlético-MG, rodada 38, cancelada); **2020:** 380 partidas de 08/08/2020 a 25/02/2021 (COVID-19); **aliases:** nenhum aplicado — Barueri (só 2009) e Grêmio Prudente (só 2010) são a mesma franquia renomeada entre temporadas, mantidas separadas por temporada; nomes sem acento na fonte (ex.: `Gremio`, `Ceara`, `Sao Paulo`) preservados.

## APÊNDICE B — Relatório de qualidade da base

Auditoria da base bruta (`docs/auditoria_fase1.md`, script `scripts/audit_fase1.py`, somente leitura): 8.785 linhas lidas (2003–2025); zero datas não interpretáveis, zero placares ausentes no recorte, zero gols negativos, zero duplicatas, zero divergências entre o campo `vencedor` e o recálculo pelo placar.

Pipeline de limpeza (`src/clean_data.py`, via `scripts/build_processed.py`): **8.785 lidas, 1.566 excluídas** (`fora_do_recorde_2006_2024`), **7.219 mantidas**. Cobertura por temporada: 380 em todas, exceto **2016 com 379** (`seasons_below_expected: {2016: 1}` — Chapecoense × Atlético-MG cancelada). Temporada 2020 de 2020-08-08 a 2021-02-25, atribuída por intervalo, não por ano civil.

Base externa (seção 5.6): **6.618 partidas com registro de público** (91,7%; 96,8% em 2007–2024) e **6.821 com árbitro** (94,5%). 2006 não tem público; 2008 tem 217 zeros tratados como falha de registro; 2020 tem 380 zeros reais e 2021, 218; 2024 foi completado pelo FBref (376/380). O relatório completo, com regras e limitações, está em `docs/analise_publico_arbitragem.md`.

Cartões (seção 5.7): **4.559 partidas de 2013–2024** (100% das elegíveis), com **1 cartão não atribuído** em 2022; 2006–2012 não têm cartões nessa fonte. A junção usa data, equipes e placar, com fallback para jogos remarcados; a data canônica é a da base do TCC. O relatório está em `docs/analise_cartoes.md`.

## APÊNDICE C — Validações executadas

Validação cruzada contra o OpenFootball (domínio público, CC0-1.0; `python3 scripts/validate_cross.py`), 2018–2024:

| Ano | Base | OF | Em ambas | Placar igual | Diverg. placar |
|---|---:|---:|---:|---:|---:|
| 2018 | 380 | 380 | 380 | 380 | 0 |
| 2019 | 380 | 380 | 380 | 380 | 0 |
| 2020 | 380 | 380 | 380 | 380 | 0 |
| 2021 | 380 | 380 | 380 | 380 | 0 |
| 2022 | 380 | 380 | 380 | 380 | 0 |
| 2023 | 380 | 380 | 379 | 379 | 0 |
| 2024 | 380 | 380 | 380 | 380 | 0 |

**2.659 de 2.660 partidas idênticas (99,96%), zero divergências de placar ou mando.** A única exceção é de data e explicada: Botafogo-RJ × Athletico-PR 1–1, 28ª rodada de 2023 (base: 22/10/2023; OpenFootball: 21/10/2023 — jogo de dois dias no Nilton Santos, iniciado em 21/10 e concluído em 22/10).

Validação dos campeões (`python3 scripts/validate_champions.py`, recálculo pontos → vitórias → saldo a partir da base processada): **PASS — 19/19 campeões oficiais** (ex.: Flamengo 90 em 2019; Flamengo 71 × Internacional 70 em 2020; Palmeiras 70 × Botafogo 68 em 2023).

Validação dos cartões (`scripts/build_cards.py` e `scripts/analyze_cards.py`): **4.559/4.559 partidas** de 2013–2024, **1 cartão não atribuído**; a Tabela 11 e a Figura 13 são reproduzidas pelo pipeline. A conferência de consistência da junção detectou uma divergência de placar na fonte (Internacional × Atlético-MG, 2019: 0–0 na fonte, 2–1 na base), resolvida pela data canônica e registrada em `QUALITY.json`.

## APÊNDICE D — Casos de teste e instruções de execução

Suíte Pytest (`python3 -m pytest tests/ -q`): **114 passed** (105 rápidos + 9 de integração).

- `tests/test_metrics.py`: caso de referência de três partidas (Pollard exatamente 50%); tudo-mandante acima de 50% e tudo-visitante abaixo; proporções somam 100; Pollard indefinido sem pontos; recorte vazio não quebra; agregação `by_season`; `team_season` separa pontos de casa e fora; Flamengo 2019 (53/37/90/38); `teams_in_season` respeita a temporada.
- `tests/test_context.py` (20): haversine (São Paulo–Rio ≈ 360 km; zero na mesma cidade); clássicos locais com viagem zero; distância interestadual na faixa esperada; descanso em dias (incluindo estreia sem anterior e jogo no mesmo dia); pontos e posição antes da partida; flags de era; mesma UF, região, estádio habitual, faixas de descanso e de posição; cobertura dos 43 clubes e somas da base real (7.219).
- `tests/test_associations.py` (19): bootstrap de Pollard, IC anual, diferença por cluster de temporada, ponto de quebra, grupos, vantagem por equipe, desvio dentro de equipe-temporada, split-half, features de equipe-temporada e partida, matriz de correlação e cobertura da base real.
- `tests/test_data_validation.py`: placar ausente não vira zero; gols negativos rejeitados; mandante igual a visitante rejeitado; fora do recorte excluído; `match_id` duplicado mantém o primeiro; resultado recalculado do placar; `_strip` apara dtype `string`; clube ausente rejeitado.
- `tests/test_app.py`: aba Equipes filtra temporada e confere Flamengo 2019 (53/37/90/38); aba Equipes respeita o filtro global; aba Contexto existe e calcula grupos.
- `tests/test_charts_composicao.py`: séries, rótulos pt-BR, IC dos grupos, ranking por equipe e heatmap de correlação.
- `tests/test_formatting.py`: formatação pt-BR (`49,0%`, `63,66%`, `—`, `1,49`, `+0,49`); gráfico usa separador pt-BR (`,.`).
- `tests/test_integrity.py`: `verify_sha256` aceita hash correto e rejeita incorreto.
- `tests/test_cards.py` (9): normalização de times e aliases; parser de cartões; regra da última menção; desempate por UF e por especificidade; cartão não atribuído; `parse_resultado` e `parse_data`.

Execução (conforme `README.md`):

```bash
python3 -m pip install -r requirements-lock.txt  # versões exatas do ambiente validado
python3 scripts/fetch_raw.py         # baixa o bruto (não versionado, plano B)
python3 scripts/fetch_raw.py --check # confere o SHA-256 das cópias locais
python3 scripts/build_processed.py   # gera data/processed/
python3 scripts/analyze_context.py   # gera tab5, tab6 e contexto.json
python3 scripts/make_figures.py      # gera figuras e tab1
PYTHONPATH=src python3 scripts/fetch_cards.py    # cartões 2013–2024 (MIT)
PYTHONPATH=src python3 scripts/build_cards.py    # junta cartões à base
PYTHONPATH=src python3 scripts/analyze_cards.py  # Tabela 11 e Figura 13
python3 -m pytest tests/ -q          # 114 testes (105 rápidos + 9 de integração)
python3 scripts/validate_cross.py    # validação OpenFootball 2018–2024
python3 -m streamlit run app.py
```
