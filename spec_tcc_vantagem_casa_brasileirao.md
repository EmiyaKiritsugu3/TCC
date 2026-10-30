# Especificação do TCC

## Análise estatística da vantagem de jogar em casa no Campeonato Brasileiro Série A: desenvolvimento de um dashboard interativo para análise de resultados históricos

**Curso:** Sistemas de Informação  
**Área:** análise de dados, estatística aplicada e sistemas de apoio à decisão  
**Tipo de trabalho:** pesquisa quantitativa aplicada, com desenvolvimento de software  
**Versão:** 1.0 — proposta inicial a validar com o orientador

---

## 1. Resumo da proposta

O trabalho propõe desenvolver um dashboard interativo para analisar a vantagem de jogar em casa no Campeonato Brasileiro Série A, usando resultados históricos das temporadas de 2006 a 2024. A aplicação organizará os dados das partidas, calculará indicadores estatísticos e apresentará visualizações que permitam comparar o desempenho dos mandantes e visitantes entre temporadas e equipes.

A análise usará principalmente a proporção de vitórias, empates e derrotas, os gols marcados em casa e fora, os pontos conquistados e o índice de vantagem em casa de Pollard. O produto será implementado em Python, com Pandas para tratamento dos dados, Plotly para gráficos e Streamlit para a interface web.

O objetivo não é prever resultados futuros nem identificar causas definitivas da vantagem em casa. O foco é produzir uma análise histórica reproduzível e um sistema simples para explorar dados esportivos.

## 2. Título

**Título recomendado:** Análise estatística da vantagem de jogar em casa no Campeonato Brasileiro Série A: desenvolvimento de um dashboard interativo para análise de resultados históricos.

**Título alternativo, mais curto:** Análise da vantagem de jogar em casa no Brasileirão Série A por meio de um dashboard interativo.

## 3. Contexto e problema de pesquisa

No futebol, a vantagem de jogar em casa é geralmente investigada comparando resultados e pontos obtidos quando uma equipe atua como mandante e como visitante. A literatura já estudou o fenômeno no futebol brasileiro, inclusive por meio do aproveitamento percentual de pontos e de comparações entre temporadas.

A proposta é construir uma aplicação capaz de organizar dados históricos e permitir a exploração integrada de indicadores, com um recorte temporal definido e procedimentos de limpeza e cálculo documentados.

**Problema de pesquisa:** Qual foi a magnitude da vantagem de jogar em casa no Campeonato Brasileiro Série A entre 2006 e 2024, e como os indicadores de desempenho dos mandantes e visitantes variaram entre as temporadas?

### 3.1 Perguntas secundárias

1. Qual foi a proporção de vitórias dos mandantes, empates e vitórias dos visitantes no período?
2. Os mandantes marcaram, em média, mais gols por partida que os visitantes?
3. Como o índice de vantagem em casa variou de temporada para temporada?
4. Existem diferenças descritivas entre os indicadores de cada temporada e de cada clube?

Essas perguntas são descritivas. O sistema não deverá afirmar que jogar em casa, por si só, causa os resultados observados.

## 4. Justificativa

O tema é adequado a Sistemas de Informação porque envolve aquisição e tratamento de dados, definição de indicadores, visualização interativa e desenvolvimento de um sistema de apoio à análise. A dimensão matemática é relevante, mas pode ficar limitada a estatística descritiva, proporções, médias e um índice publicado na literatura.

A proposta também é viável por utilizar dados secundários sobre resultados de partidas, sem entrevistas, recrutamento de participantes ou dependência de informações privadas. O dashboard oferece uma forma prática de explorar os dados sem exigir que o usuário programe ou execute cálculos manualmente.

A contribuição pretendida não é alegar que a vantagem em casa é um fenômeno inédito. A contribuição será combinar um recorte histórico definido, um fluxo de tratamento documentado, múltiplos indicadores e uma interface interativa reproduzível. A originalidade e o recorte final deverão ser confirmados após a revisão bibliográfica e a avaliação do orientador.

## 5. Objetivos

### 5.1 Objetivo geral

Desenvolver um dashboard interativo para analisar estatisticamente a vantagem de jogar em casa no Campeonato Brasileiro Série A, considerando as temporadas de 2006 a 2024.

### 5.2 Objetivos específicos

1. Identificar uma fonte de dados históricos de partidas e documentar sua procedência.
2. Padronizar os dados e verificar sua completude e consistência.
3. Calcular indicadores de resultados, gols, pontos e vantagem em casa.
4. Comparar os indicadores entre temporadas e, de forma secundária, entre equipes.
5. Construir visualizações interativas para explorar os indicadores calculados.
6. Testar os cálculos e verificar se os resultados apresentados pelo dashboard correspondem à base validada.
7. Discutir os resultados e as limitações de uma análise baseada exclusivamente em placares e designação de mandante/visitante.

## 6. Hipótese e definição operacional

**Hipótese principal (H1):** no conjunto de partidas analisado, o índice de vantagem em casa de Pollard será superior a 50%, indicando que os mandantes obtiveram mais pontos que os visitantes, em termos agregados.

**Hipótese exploratória (H2):** o índice de vantagem em casa não permaneceu constante entre as temporadas de 2006 e 2024.

H1 será avaliada por meio do índice calculado para o período completo. H2 será investigada inicialmente com gráficos temporais e comparação descritiva por temporada. Não é obrigatório incluir testes estatísticos inferenciais; caso o orientador exija um teste de tendência, poderá ser considerada a correlação de Spearman entre temporada e índice anual, deixando explícito que se trata de análise exploratória.

## 7. Escopo

### 7.1 Incluído

- Campeonato Brasileiro masculino Série A.
- Temporadas completas de 2006 a 2024.
- Partidas com placar final válido.
- Análise agregada do campeonato por temporada.
- Comparação de indicadores por equipe dentro de uma temporada, como funcionalidade secundária.
- Dashboard em português, com filtros e gráficos.
- Documentação da fonte, dicionário de dados, regras de limpeza e fórmulas utilizadas.

### 7.2 Fora do escopo

- Previsão de resultados ou desenvolvimento de inteligência artificial.
- Apostas esportivas, odds ou recomendações de apostas.
- Séries B, C e D.
- Dados detalhados de jogadores, escalações, posse de bola, cartões e finalizações.
- Avaliação causal do efeito da torcida, arbitragem, viagem, clima ou qualidade do elenco.
- Atualização automática do campeonato em andamento.
- Cadastro de usuários, login, perfis, banco de dados remoto ou API própria.
- Aplicativo móvel nativo.

### 7.3 Justificativa do período

O recorte de 2006 a 2024 foi escolhido como ponto inicial porque, desde 2006, a Série A passou a adotar o formato de 20 clubes em pontos corridos, com jogos em casa e fora. São 19 temporadas. Se todos os calendários estiverem completos, espera-se uma referência de 380 partidas por temporada, ou 7.220 partidas no período. Essa quantidade é uma verificação esperada, não um número a assumir sem auditoria dos dados.

O ano de 2025 e a temporada de 2026 ficam fora do escopo inicial para manter um conjunto fechado de temporadas completas e reduzir riscos de dados em atualização.

## 8. Dados necessários

### 8.1 Campos mínimos da base de partidas

| Campo lógico | Tipo | Obrigatório | Uso |
|---|---|---:|---|
| `match_id` | texto ou inteiro | Não, mas recomendado | Identificação da partida e verificação de duplicatas |
| `season` | inteiro | Sim | Filtro e agrupamento por temporada |
| `date` | data | Recomendado | Auditoria e ordenação cronológica |
| `home_team` | texto | Sim | Clube designado como mandante |
| `away_team` | texto | Sim | Clube designado como visitante |
| `home_goals` | inteiro não negativo | Sim | Placar do mandante |
| `away_goals` | inteiro não negativo | Sim | Placar do visitante |
| `source` | texto/metadata | Sim no projeto | Rastreabilidade da origem dos dados |

Os nomes exatos das colunas poderão variar conforme o arquivo de origem. O processo de importação deverá convertê-los para os nomes lógicos acima.

### 8.2 Fonte inicial sugerida

O repositório público `adaoduque/Brasileirao_Dataset` disponibiliza CSVs históricos do Campeonato Brasileiro, incluindo o arquivo `campeonato-brasileiro-full.csv`, com data, mandante, visitante e placares. Link: https://github.com/adaoduque/Brasileirao_Dataset

Esse repositório é uma fonte candidata, não uma garantia de dados perfeitos ou de licença irrestrita. Antes da adoção final:

1. Verificar se existe licença explícita e quais condições se aplicam. A presença de um arquivo público no GitHub, por si só, não deve ser interpretada como autorização automática para redistribuí-lo.
2. Registrar o autor/repositório, versão ou commit utilizado e data de acesso.
3. Verificar a cobertura das temporadas de 2006 a 2024, a existência de placares ausentes e duplicatas.
4. Quando possível, confrontar totais e partidas selecionadas com fontes oficiais, como a CBF.
5. Não redistribuir os CSVs brutos no repositório público do TCC sem confirmar as condições de uso. O código e os dados derivados devem ser publicados apenas conforme a licença e as regras aplicáveis.

## 9. Metodologia acadêmica

### 9.1 Classificação da pesquisa

- **Natureza:** aplicada, pois resulta em um artefato de software.
- **Abordagem:** quantitativa.
- **Objetivos:** exploratórios e descritivos.
- **Procedimentos:** pesquisa documental e análise de dados secundários, seguida do desenvolvimento e teste de um dashboard.
- **Unidade de análise:** partida, agregada por temporada e, secundariamente, por equipe.

### 9.2 Etapas da pesquisa

1. **Revisão bibliográfica:** estudar o conceito de vantagem em casa, o índice de Pollard e trabalhos sobre futebol brasileiro.
2. **Escolha da fonte:** conferir procedência, cobertura e condições de uso dos dados.
3. **Auditoria inicial:** inspecionar colunas, quantidade de registros, temporadas disponíveis, placares ausentes e duplicatas.
4. **Limpeza e padronização:** normalizar datas, nomes de times e placares; excluir registros inválidos mediante regras documentadas.
5. **Construção dos indicadores:** implementar fórmulas e comparar resultados por temporada.
6. **Desenvolvimento do dashboard:** criar filtros, indicadores, tabelas e gráficos.
7. **Testes:** conferir as fórmulas com casos pequenos criados manualmente e validar os agregados contra a base processada.
8. **Análise e discussão:** responder às perguntas de pesquisa e registrar limitações.
9. **Documentação:** preparar relatório, instruções de execução, dicionário de dados e referências.

### 9.3 Critérios de inclusão e exclusão

**Incluir:** partidas da Série A entre as temporadas de 2006 e 2024 que tenham mandante, visitante e placar final válido.

**Excluir:** partidas de outras competições; registros sem placar final; linhas duplicadas confirmadas; registros com gols negativos ou valores impossíveis de interpretar; partidas cuja identificação de mandante/visitante esteja ausente.

Não excluir uma partida apenas por parecer incomum. Casos suspeitos deverão ser registrados em um relatório de qualidade e investigados antes de qualquer decisão.

## 10. Indicadores e fórmulas

### 10.1 Classificação do resultado

Para cada partida:

- **Vitória do mandante:** `home_goals > away_goals`.
- **Empate:** `home_goals == away_goals`.
- **Vitória do visitante:** `home_goals < away_goals`.

### 10.2 Pontos por partida

Conforme o sistema de pontuação usual do campeonato:

- Vitória: 3 pontos.
- Empate: 1 ponto para cada equipe.
- Derrota: 0 pontos.

Os pontos do mandante e do visitante serão calculados a partir do placar, e não de um campo de vencedor possivelmente inconsistente.

### 10.3 Indicadores obrigatórios

**A. Proporção de vitórias do mandante**

\[
P(V_m)=\frac{N_{V_m}}{N_{partidas}}\times100
\]

**B. Proporção de empates**

\[
P(E)=\frac{N_E}{N_{partidas}}\times100
\]

**C. Proporção de vitórias do visitante**

\[
P(V_v)=\frac{N_{V_v}}{N_{partidas}}\times100
\]

As três proporções devem somar aproximadamente 100%, admitindo apenas diferença de arredondamento.

**D. Média de gols do mandante**

\[
\bar G_m=\frac{\sum home\_goals}{N_{partidas}}
\]

**E. Média de gols do visitante**

\[
\bar G_v=\frac{\sum away\_goals}{N_{partidas}}
\]

**F. Diferença média de gols**

\[
D_G=\frac{\sum(home\_goals-away\_goals)}{N_{partidas}}
\]

**G. Pontos totais do mandante e do visitante**

Somar os pontos atribuídos a cada lado de todas as partidas selecionadas. Esses números são pontos conquistados na posição de mandante ou visitante, não pontos de tabela de um único clube.

**H. Índice de vantagem em casa de Pollard**

\[
VC=\frac{P_m}{P_m+P_v}\times100
\]

Em que:

- `P_m` = soma dos pontos conquistados pelos mandantes nas partidas do recorte.
- `P_v` = soma dos pontos conquistados pelos visitantes nas mesmas partidas.

Interpretação:

- **50%:** os mandantes e visitantes conquistaram a mesma quantidade de pontos agregados.
- **Acima de 50%:** os mandantes conquistaram mais pontos.
- **Abaixo de 50%:** os visitantes conquistaram mais pontos.

Se `P_m + P_v` for zero, o índice deverá ser tratado como indefinido, e não como zero.

O dashboard deve exibir a fórmula e uma explicação simples do índice. Não misturar essa fórmula com outras definições de “home advantage” usadas na literatura, pois podem produzir escalas diferentes.

### 10.4 Indicadores secundários, se houver tempo

- Mediana e desvio padrão dos gols por lado.
- Índice de Pollard por temporada.
- Índice de Pollard por equipe e temporada, calculado com os pontos obtidos em casa e fora pela equipe.
- Correlação de Spearman entre ano e índice anual, como análise exploratória opcional, caso o orientador solicite uma medida de tendência.

Os indicadores secundários não devem aumentar o escopo antes de a versão mínima estar concluída.

## 11. Requisitos funcionais do dashboard

### RF01 — Carregar dados validados

O sistema deve carregar a base processada e informar um erro legível se o arquivo estiver ausente, vazio ou sem as colunas obrigatórias.

### RF02 — Filtrar temporadas

O usuário deve selecionar uma temporada específica ou um intervalo de temporadas. Todos os indicadores e gráficos dependentes devem respeitar o filtro.

### RF03 — Apresentar indicadores gerais

O dashboard deve mostrar pelo menos: partidas analisadas, percentual de vitórias dos mandantes, percentual de empates, percentual de vitórias dos visitantes, média de gols do mandante, média de gols do visitante e índice de Pollard.

### RF04 — Comparar temporadas

O sistema deve apresentar uma série temporal do índice de Pollard e permitir comparação das proporções de resultados entre as temporadas selecionadas.

### RF05 — Comparar gols

O sistema deve exibir a média de gols dos mandantes e visitantes ao longo das temporadas.

### RF06 — Consultar equipe

Como função secundária, o usuário deve poder selecionar uma equipe e temporada para comparar resultados e pontos conquistados em casa e fora, quando houver dados suficientes.

### RF07 — Exibir tabela de partidas

O sistema deve apresentar uma tabela com temporada, data, mandante, placar e visitante, sujeita aos filtros aplicados.

### RF08 — Explicar os indicadores

Cada indicador deve ter rótulo, unidade, descrição e, quando aplicável, fórmula acessível por texto de ajuda ou seção de metodologia.

### RF09 — Apresentar informações sobre os dados

Deve existir uma seção que informe fonte, período, quantidade de partidas válidas, registros excluídos e alertas de qualidade conhecidos.

### RF10 — Tratar filtros sem resultados

Quando os filtros não retornarem partidas, o sistema deve exibir uma mensagem clara, sem quebrar ou mostrar métricas enganosas.

### RF11 — Exportar resultados filtrados (opcional)

Se houver tempo, permitir baixar como CSV a tabela filtrada e/ou um resumo por temporada. A exportação dos dados brutos deverá respeitar as condições de uso da fonte original.

## 12. Organização das telas

### Tela 1 — Visão geral

- Filtros de temporada.
- Cartões de indicadores principais.
- Gráfico de distribuição de vitórias do mandante, empates e vitórias do visitante.
- Comparação da média de gols em casa e fora.
- Nota breve explicando o significado do índice de Pollard.

### Tela 2 — Evolução histórica

- Gráfico de linhas do índice de Pollard por temporada.
- Gráfico de barras empilhadas ou linhas para resultados por temporada.
- Gráfico comparativo da média de gols em casa e fora.
- Destaques descritivos calculados a partir dos dados, sem texto causal automático.

### Tela 3 — Equipes e partidas

- Seleção de temporada e equipe.
- Indicadores de desempenho da equipe em casa e fora.
- Tabela de partidas com os placares.
- A comparação entre equipes deve ser contextualizada pela temporada; não misturar clubes em temporadas diferentes sem explicitar essa escolha.

### Tela 4 — Metodologia e qualidade dos dados

- Fonte e data de acesso.
- Período analisado.
- Dicionário resumido de variáveis.
- Fórmula de Pollard.
- Quantidade esperada e observada de partidas por temporada.
- Resumo das regras de limpeza e limitações conhecidas.

As telas podem ser organizadas em páginas do Streamlit ou abas. A ordem acima é conceitual; não há exigência de interface complexa.

## 13. Requisitos não funcionais

- **RNF01 — Simplicidade:** executar localmente com poucos comandos e sem conta de usuário.
- **RNF02 — Reprodutibilidade:** os indicadores devem ser recalculados a partir de uma base de entrada versionada e regras de transformação documentadas.
- **RNF03 — Consistência:** todos os gráficos e cartões devem usar o mesmo conjunto de dados filtrado.
- **RNF04 — Usabilidade:** labels e explicações em português, com números formatados e unidades explícitas.
- **RNF05 — Robustez:** entradas inválidas e ausência de dados devem gerar mensagens claras.
- **RNF06 — Manutenibilidade:** funções de limpeza, cálculo e visualização devem ficar separadas no código.
- **RNF07 — Portabilidade:** funcionar em ambiente Python compatível com as versões documentadas no `requirements.txt`.
- **RNF08 — Privacidade:** o projeto não necessita de dados pessoais nem de autenticação.

## 14. Arquitetura técnica recomendada

**Stack mínima:**

- Python 3.11 ou versão compatível verificada durante a implementação.
- Pandas para importação, transformação e agregação.
- Plotly Express/Graph Objects para gráficos.
- Streamlit para interface e filtros.
- Pytest para testes automatizados dos cálculos e validações.

Não é necessário utilizar banco de dados relacional, autenticação, API de backend ou framework frontend separado. Uma base CSV local é suficiente para esse escopo.

### 14.1 Pipeline

1. **Dados brutos:** cópia local preservada, quando a licença permitir, ou instruções de obtenção da fonte.
2. **Transformação:** script padroniza colunas, tipos, nomes e temporadas; identifica duplicatas e registros incompletos.
3. **Dados processados:** tabela limpa com uma linha por partida válida.
4. **Cálculos:** funções separadas calculam os indicadores por temporada, período e equipe.
5. **Interface:** o Streamlit aplica filtros e exibe métricas e gráficos a partir das tabelas calculadas.

### 14.2 Estrutura de pastas sugerida

```text
TCC-brasileirao-home-advantage/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/              # opcional, respeitando a licença da fonte
│   └── processed/
├── src/
│   ├── load_data.py
│   ├── clean_data.py
│   ├── metrics.py
│   └── charts.py
├── tests/
│   ├── test_metrics.py
│   └── test_data_validation.py
└── docs/
    ├── data_dictionary.md
    └── methodology.md
```

A estrutura poderá ser simplificada para um protótipo inicial, mas é recomendável manter as fórmulas fora do arquivo da interface para facilitar os testes.

## 15. Regras de tratamento e validação dos dados

1. Preservar uma cópia imutável da fonte bruta quando permitido.
2. Padronizar nomes de colunas para o esquema lógico.
3. Converter a data para um formato consistente e a temporada para inteiro.
4. Converter placares para inteiros não negativos; placares ausentes não devem virar zero.
5. Normalizar nomes de clubes, preservando uma tabela de aliases quando existirem diferenças ortográficas.
6. Verificar registros duplicados usando identificador original, quando disponível, e revisão de combinações de data, mandante, visitante e placar.
7. Não apagar duplicatas ou valores suspeitos silenciosamente: gerar um resumo dos casos analisados e das decisões tomadas.
8. Filtrar apenas temporadas de 2006 a 2024 e jogos da Série A.
9. Verificar que cada partida tenha mandante e visitante diferentes.
10. Recalcular o resultado a partir do placar e verificar divergências com o campo de vencedor, caso exista.
11. Contar partidas por temporada. Para uma temporada regular completa de 20 clubes em turno e returno, a referência esperada é 380 partidas; discrepâncias precisam ser investigadas.
12. Registrar quantas linhas foram carregadas, mantidas, excluídas e por qual motivo.

## 16. Plano de testes e critérios de aceitação

### 16.1 Testes de unidade para os cálculos

Criar uma pequena base de teste com três partidas:

| Mandante | Placar | Visitante | Pontos do mandante | Pontos do visitante |
|---|---:|---|---:|---:|
| A | 2–0 | B | 3 | 0 |
| C | 1–1 | D | 1 | 1 |
| E | 0–2 | F | 0 | 3 |

Nesse exemplo, o total de pontos dos mandantes é 4 e o total dos visitantes é 4. O índice de Pollard deve ser exatamente 50%. As proporções de vitória do mandante, empate e vitória do visitante devem ser 1/3 cada.

Criar outros testes para verificar que:

- uma série de vitórias dos mandantes produz índice acima de 50%;
- uma série de vitórias dos visitantes produz índice abaixo de 50%;
- as três proporções de resultados somam 100%, antes do arredondamento;
- placares ausentes não são tratados como 0–0;
- valores negativos de gols são rejeitados;
- filtros por temporada e equipe retornam apenas os dados correspondentes;
- denominadores iguais a zero são tratados explicitamente;
- campos obrigatórios ausentes geram erro compreensível.

### 16.2 Critérios de aceitação do produto

O sistema será considerado concluído quando:

1. for possível iniciar a aplicação com as instruções do README;
2. a aplicação carregar a base validada sem erros;
3. filtros de temporada atualizarem todos os indicadores relacionados;
4. os indicadores da interface corresponderem aos resultados calculados independentemente;
5. a evolução por temporada estiver visível em gráficos legíveis;
6. a metodologia, a fonte e as limitações estiverem disponíveis na interface ou documentação;
7. os testes principais passarem;
8. houver um registro de qualidade dos dados que explique eventuais diferenças em relação às 380 partidas esperadas por temporada.

## 17. Plano de execução sugerido

A duração real dependerá do calendário do curso e do orientador. Para controlar o escopo, organizar o trabalho por entregas em vez de depender de uma previsão rígida de semanas.

| Etapa | Entrega verificável |
|---|---|
| 1. Aprovação do recorte | Título, pergunta, objetivos e escopo aprovados pelo orientador |
| 2. Revisão bibliográfica | Referências fichadas e definições de vantagem em casa comparadas |
| 3. Auditoria dos dados | Fonte escolhida, relatório de cobertura e problemas encontrados |
| 4. Base limpa | Script de transformação, dados documentados e dicionário de variáveis |
| 5. Métricas | Funções testadas e tabela de indicadores por temporada |
| 6. Dashboard mínimo | Visão geral, filtros e gráficos principais funcionando |
| 7. Testes e refinamento | Testes executados, erros corrigidos e acessibilidade básica revisada |
| 8. Análise dos resultados | Gráficos finais, respostas às perguntas e limitações discutidas |
| 9. Escrita e apresentação | Monografia, instruções de execução, demonstração e slides |

## 18. Riscos e formas de mitigação

| Risco | Mitigação |
|---|---|
| Dados incompletos ou duplicados | Auditar antes de desenvolver o dashboard; documentar exclusões |
| Licença ou proveniência pouco clara | Confirmar licença e fonte; não redistribuir dados brutos sem autorização adequada |
| Tema parecido com estudos anteriores | Fazer revisão de literatura e delimitar contribuição como sistema reproduzível e análise longitudinal |
| Escopo crescer demais | Adiar previsões, mapas, dados de jogadores e atualizações automáticas |
| Indicadores interpretados como causas | Explicitar que a análise é observacional e baseada em resultados, sem medir todos os fatores explicativos |
| Gráficos divergirem entre si | Usar uma única camada de cálculo e testes automatizados |
| Mudanças de nome de clubes prejudicarem filtros | Manter dicionário de aliases e limitar comparações temporais quando a identidade não for inequívoca |

## 19. Limitações a declarar na monografia

- O estudo observa resultados e a designação de mandante/visitante, mas não mede diretamente a presença ou intensidade da torcida.
- Um jogo designado como mandante não garante, por si só, que tenha sido disputado no estádio habitual da equipe.
- Qualidade dos elencos, lesões, arbitragem, distância de viagem, mudanças de treinador e outros fatores não são controlados pelo modelo básico.
- Os dados históricos podem conter omissões ou inconsistências; por isso, o relatório de validação é parte essencial do trabalho.
- Resultados descritivos não demonstram causalidade nem permitem afirmar que o mesmo padrão continuará no futuro.
- O dashboard é uma ferramenta de exploração analítica, não um modelo de previsão de partidas.

## 20. Estrutura sugerida da monografia

1. **Introdução:** contexto, problema, justificativa, objetivos e delimitação.
2. **Referencial teórico:** vantagem em casa, análise de dados, estatística descritiva e visualização de informação.
3. **Metodologia:** classificação da pesquisa, fonte, critérios de inclusão, preparação dos dados e fórmulas.
4. **Análise e desenvolvimento do sistema:** arquitetura, requisitos, tratamento dos dados, cálculos e implementação do dashboard.
5. **Resultados e discussão:** indicadores do período, diferenças entre temporadas, interpretação e comparação com literatura.
6. **Conclusão:** resposta à pergunta, contribuição, limitações e possibilidades de continuação.
7. **Referências.**
8. **Apêndices, se necessários:** dicionário de dados, casos de teste e instruções para execução.

## 21. Resultado esperado

Ao final, espera-se entregar:

- um dashboard web funcional para análise histórica;
- um script reproduzível de tratamento e validação dos dados;
- funções documentadas para o cálculo dos indicadores;
- testes automatizados dos principais cálculos;
- uma monografia que explique a metodologia, discuta os resultados e reconheça as limitações;
- instruções para executar a aplicação e reproduzir a análise.

Não se deve antecipar uma conclusão numérica antes de importar e validar a base definitiva.

## 22. Referências iniciais para a revisão bibliográfica

1. **Pollard, R. (1986).** *Home advantage in soccer: a retrospective analysis.* Journal of Sports Sciences, 4(3), 237–248. DOI: https://doi.org/10.1080/02640418608732122
2. **Silva, C. D.; Moreira, D. G. (2008).** *A vantagem em casa no futebol: comparação entre o Campeonato Brasileiro e as principais ligas nacionais do mundo.* Revista Brasileira de Cineantropometria e Desempenho Humano. DOI: https://doi.org/10.1590/1980-0037.2008v10n2p184
3. **Almeida, L. G.; Oliveira, M. L.; Silva, C. D. (2011).** *Uma análise da vantagem de jogar em casa nas duas principais divisões do futebol profissional brasileiro.* Revista Brasileira de Educação Física e Esporte, 25(1), 49–54. DOI: https://doi.org/10.1590/S1807-55092011000100006
4. **Ribeiro, L. C. et al. (2022).** *Did the Absence of Crowd Support During the Covid-19 Pandemic Affect the Home Advantage in Brazilian Elite Soccer?* Journal of Human Kinetics, 81, 251–258. DOI: https://doi.org/10.2478/hukin-2022-0047. Texto em acesso aberto: https://pmc.ncbi.nlm.nih.gov/articles/PMC8884879/
5. **Adão Duque.** *Brasileirao_Dataset — Campeonato Brasileiro de Futebol, 2003–2024.* Repositório de dados no GitHub: https://github.com/adaoduque/Brasileirao_Dataset. Consultar a página, os metadados e as condições de uso vigentes no momento da pesquisa.
6. **Streamlit.** Documentação oficial: https://docs.streamlit.io/

Esta é uma lista inicial. A redação final deverá consultar os textos completos, confirmar todos os dados bibliográficos e seguir as normas e orientações adotadas pelo curso.

## 23. Decisões que precisam de validação do orientador

1. Aprovação do recorte 2006–2024 e do título.
2. Aceitação do dashboard como artefato central de Sistemas de Informação, acompanhado da pesquisa quantitativa.
3. Confirmação da fonte de dados e das condições de uso.
4. Decisão sobre a inclusão da análise exploratória de tendência (por exemplo, Spearman) ou manutenção de estatística descritiva.
5. Formato exigido pelo curso para projeto, TCC e avaliação do software.

**Recomendação de escopo:** concluir primeiro a auditoria dos dados, os indicadores de Pollard e o dashboard mínimo. Só adicionar métodos, filtros ou telas secundárias depois que esse núcleo estiver validado.
