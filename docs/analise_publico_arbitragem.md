# Público e arbitragem: análise descritiva da base externa

**Data:** 20/11/2026  
**Pergunta:** as variáveis externas de público e arbitragem acrescentam
informação à vantagem de casa medida no TCC, ou apenas repetem força do
clube e composição de confrontos?

Este relatório é técnico e exploratório. Nada aqui afirma causalidade.
Os scripts que geram os números estão em `scripts/build_external.py` e
`scripts/analyze_external.py`; a origem das fontes está em
`docs/fontes_externas.md`.

## 1. Base final

A junção usa **temporada + mandante + visitante + placar**, não a data,
porque as fontes divergem em jogos remarcados. Nomes passam por um mapa de
aliases; Barueri/Grêmio Prudente (2010) é tratado como a mesma franquia.

| Item | Cobertura |
|---|---:|
| Partidas na base do TCC | 7.219 |
| Com público | 6.618 (91,7%) |
| Com público em 2007–2024 | 6.618 de 6.839 (96,8%) |
| Com árbitro | 6.821 (94,5%) |
| Com árbitro em 2007–2024 | 6.821 de 6.839 (99,7%) |
| Com faltas (2018+) | 2.090 |

Regras de limpeza:

- **2006:** sem público e sem árbitro na fonte; fica ausente, sem imputação.
- **2008:** os 217 `publico = 0` são tratados como **falha de registro**, não
  portão fechado. Os zeros estão espalhados por todos os clubes e por todos
  os meses (maio a dezembro); a média dos 163 jogos não-zero é 18.287,
  compatível com 2007 (17.659) e 2009 (17.712). Se os zeros fossem reais, a
  média de 2008 seria 7.844 e criaria uma queda artificial.
- **2020:** os 380 zeros são **reais** (portões fechados).
- **2021:** os 218 zeros são **reais** (retorno gradual; a frequência cai de
  63 jogos em junho para 2 em outubro).
- **2024:** a Base dos Dados tem 286 jogos; o FBref completa o público dos
  demais. Resultado: 376 de 380 jogos com público (99,0%).
- **`publico_max`** é capacidade, não público do jogo; não é usado.
- **2024, árbitro:** a Base dos Dados cobre 286 jogos e o FBref acrescenta
  76 jogos sem árbitro na BD; a união chega a 362 de 380 (95,3%).

## 2. Público por temporada

| Temporada | Jogos | Com público | Média | Mediana | Zeros reais |
|---|---:|---:|---:|---:|---:|
| 2006 | 380 | 0 | — | — | 0 |
| 2007 | 380 | 380 | 17.659 | 13.522 | 0 |
| 2008 | 380 | 163 | 18.287¹ | 14.741¹ | 0 |
| 2009 | 380 | 380 | 17.712 | 14.830 | 0 |
| 2010 | 380 | 380 | 14.826 | 12.339 | 0 |
| 2011 | 380 | 380 | 14.930 | 12.794 | 0 |
| 2012 | 380 | 380 | 13.733 | 11.614 | 0 |
| 2013 | 380 | 380 | 15.759 | 12.154 | 0 |
| 2014 | 380 | 380 | 16.725 | 14.044 | 0 |
| 2015 | 380 | 380 | 17.224 | 13.056 | 0 |
| 2016 | 379 | 379 | 15.725 | 12.087 | 0 |
| 2017 | 380 | 380 | 16.922 | 13.576 | 0 |
| 2018 | 380 | 380 | 20.358 | 16.280 | 0 |
| 2019 | 380 | 380 | 22.649 | 18.910 | 0 |
| 2020 | 380 | 380 | 0 | 0 | 380 |
| 2021 | 380 | 380 | 6.524 | 0 | 218 |
| 2022 | 380 | 380 | 21.482 | 18.288 | 0 |
| 2023 | 380 | 380 | 27.081 | 26.616 | 0 |
| 2024 | 380 | 376 | 26.930 | 25.747 | 0 |

¹ Apenas os 163 jogos com público; os 217 zeros de 2008 foram removidos.

Fonte: Base dos Dados/Transfermarkt, com complemento do FBref em 2024.
Elaboração própria.

A série mostra três patamares: público médio de 14–18 mil em 2010–2017,
salto para 20–23 mil em 2018–2019, colapso em 2020–2021 e retorno em
22–27 mil em 2022–2024. A tendência de alta pós-2022 é consistente com a
retomada de público, mas também com mudanças de capacidade e preço; não é
uma medida de demanda isolada.

## 3. Vantagem de casa por bloco

| Bloco | Jogos | Pollard | IC 95% | Saldo médio | Pontos casa | Vitória casa | Público médio |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2006 (sem público) | 380 | 64,2 | 59,8–68,6 | 0,468 | 1,763 | 50,3% | — |
| 2007–2018 | 4.559 | 64,9 | 63,7–66,2 | 0,542 | 1,775 | 50,3% | 16.574 |
| 2019 | 380 | 62,4 | 57,8–67,0 | 0,458 | 1,711 | 48,4% | 22.649 |
| 2020 (portões fechados) | 380 | 60,2 | 55,6–64,7 | 0,337 | 1,634 | 45,0% | 0 |
| 2021 (retorno parcial) | 380 | 61,8 | 57,5–66,3 | 0,326 | 1,671 | 45,8% | 6.524 |
| 2022–2024 | 1.140 | 60,6 | 57,9–63,3 | 0,384 | 1,654 | 46,1% | 25.291 |

Fonte: base do TCC + Base dos Dados/FBref. IC 95% por bootstrap de partidas
(3.000 reamostragens); não considera dependência dentro de temporada.

Leitura: o Pollard cai 4,7 p.p. de 2007–2018 para 2020, mas **não
desaparece** com os portões fechados. Em 2022–2024, com público de volta a
25 mil, o índice fica em 60,6% — praticamente o mesmo patamar de 2020–2021.
O retorno da torcida não trouxe a vantagem de volta ao patamar pré-2019.
Isso é compatível com a leitura do TCC de que a queda de nível coincide com
um conjunto de choques (VAR, pandemia, calendário), não com a torcida
isoladamente.

## 4. Público e vantagem de casa

### 4.1 Nível equipe-temporada

| Recorte | Equipe-temporadas | Spearman HA × público | Spearman pontos × público |
|---|---:|---:|---:|
| Todas | 360 | 0,068 | 0,461 |
| 2007–2019 | 260 | 0,033 | 0,545 |
| 2022–2024 | 60 | 0,085 | 0,589 |
| Sem 2020–2021 | 320 | −0,010 | 0,543 |

Fonte: `team_season_features` + público médio dos jogos em casa. HA = pontos
por jogo em casa − fora. Spearman com pares completos.

Leitura: o público médio é um **proxy forte de tamanho/força do clube**
(pontos, 0,46–0,59), mas não da vantagem casa−fora (0,03–0,09; −0,01 sem as
temporadas pandêmicas). Clubes com mais torcida não são os que mais
dependem do mando.

### 4.2 Nível partida

| Recorte | Partidas | Spearman bruto saldo × público | Spearman parcial¹ |
|---|---:|---:|---:|
| Todas | 6.618 | 0,079 | −0,042 |
| 2007–2019 | 4.722 | 0,063 | −0,052 |
| 2022–2024 | 1.136 | 0,133 | −0,063 |
| Sem 2020–2021 | 5.858 | 0,069 | −0,053 |

¹ Correlação de Spearman entre o desvio de público e o desvio de saldo de
gols, ambos dentro da equipe-temporada, controlando a diferença de posição
pré-jogo (`rank_diff`).

Leitura: a correlação bruta é positiva porque clubes grandes têm mais
público e melhores resultados. Ao comparar o mesmo clube na mesma temporada
e controlar a força pré-jogo do adversário, a associação fica **levemente
negativa**. Ou seja: dentro de uma equipe-temporada, os jogos de maior
público tendem a ser justamente os mais difíceis.

### 4.3 Acima e abaixo da mediana de público da equipe-temporada

| Grupo | Partidas | Público médio | Posição média do adversário¹ | Saldo médio | Pontos casa | Vitória casa | Rank diff² |
|---|---:|---:|---:|---:|---:|---:|---:|
| Abaixo da mediana | 2.792 | 12.286 | 11,53 | 0,591 | 1,822 | 52,2% | +0,094 |
| Acima da mediana | 2.933 | 24.596 | 9,82 | 0,429 | 1,678 | 46,7% | −0,756 |

¹ Posição na tabela antes da partida; menor = adversário mais forte.  
² `away_pos_before − home_pos_before`; positivo = mandante relativamente
mais forte.

Leitura: os jogos com público acima da mediana têm adversários mais fortes
(9,82 vs. 11,53) e mandante relativamente mais fraco (−0,76 vs. +0,09). A
diferença de desempenho entre os grupos é, em boa parte, **composição de
confrontos**, não efeito da torcida. Isso não refuta a hipótese da torcida;
mostra que a variação observada de público não é um experimento limpo. O
contraste de 2020 (portões fechados) é mais informativo, e nele a vantagem
cai, mas permanece.

### 4.4 Por quartil de público (equipe)

| Quartil | Times | Público médio | Pontos/temporada | HA | Casa pts/jogo | Fora pts/jogo |
|---|---:|---:|---:|---:|---:|---:|
| Q1 (menor) | 7 | 6.461 | 43,1 | 0,657 | 1,463 | 0,806 |
| Q2 | 7 | 12.960 | 46,5 | 0,815 | 1,632 | 0,817 |
| Q3 | 7 | 18.074 | 52,7 | 0,762 | 1,769 | 1,007 |
| Q4 (maior) | 7 | 24.939 | 59,4 | 0,731 | 1,930 | 1,199 |

Fonte: base validada + base externa; 28 equipes com pelo menos cinco temporadas.
HA = pontos/jogo em casa − fora. Spearman público × pontos = 0,786; público ×
HA = 0,043.

Os pontos sobem de 43,1 (Q1) para 59,4 (Q4), enquanto o HA fica entre 0,657
e 0,815, sem ordem monotônica — o Q4 tem 0,731, abaixo do Q2. O público
separa clubes grandes de pequenos, não clubes mais dependentes do mando.
Flamengo (Q4) tem HA 0,59; Santos (Q2), 0,86; Atlético-GO (Q1), 0,36. A
Figura 12 da monografia mostra o mesmo padrão em dispersão.

## 5. Arbitragem

| Item | Valor |
|---|---:|
| Jogos com árbitro | 6.821 |
| Árbitros distintos | 185 |
| Jogos por árbitro (mediana) | 13 |
| Jogos por árbitro (máximo) | 284 |
| Taxa de vitória do mandante | 48,9% |
| Árbitros com 40+ jogos | 48 |
| Faixa da taxa de vitória do mandante (40+ jogos) | 40,8%–67,4% |

A variação entre árbitros é grande, mas compatível com ruído: com
p = 48,9% e 40–284 jogos por árbitro, apenas **1 dos 48** árbitros com 40+
jogos fica fora de ±2 desvios-padrão (esperado sob a hipótese nula: 2,2).
Não há, portanto, evidência descritiva de heterogeneidade além do acaso na
taxa de vitória do mandante.

Mais importante: a base identifica **quem apitou**, não **o que decidiu**.
Sem cartões, pênaltis e faltas por árbitro, não é possível testar viés
arbitral. As faltas da Base dos Dados só existem a partir de 2018 e têm
lacunas; não cobrem a série. Por isso a arbitragem entra como **cobertura e
limitação**, não como variável da matriz de correlação.

## 6. O que isso acrescenta ao TCC

1. **Público não é um bom preditor da vantagem casa−fora** no nível
   equipe-temporada: a associação é quase nula, enquanto a associação com
   pontos é forte. O público mede tamanho de clube, não dependência do mando.
2. **No nível partida, a associação bruta é confundida** por composição de
   confrontos; controlando equipe-temporada e força pré-jogo, ela se inverte.
3. **O contraste de 2020 é o achado mais forte**: sem torcida, a vantagem
   cai, mas não desaparece; com torcida de volta em 2022–2024, ela não
   retorna ao patamar pré-2019. Isso reforça a leitura multifatorial e a
   cautela contra atribuir a queda à torcida.
4. **Arbitragem**: a identidade do árbitro não mede viés; a variação bruta
   é compatível com ruído. Para testar o canal arbitral seriam necessários
   cartões/pênaltis das súmulas da CBF, que ficam como trabalho futuro.

## 7. Limitações

- **Público é proxy**, não medida exata: a fonte pode misturar pagante e
  total. No overlap de 2024 com o FBref (286 jogos), 243 são idênticos
  (85,0%), 248 ficam a ≤100 (86,7%) e 271 a ≤1.000 (94,8%); a diferença
  média absoluta é 316 espectadores.
- **2008** tem 217 zeros tratados como ausentes; a decisão é documentada,
  mas não é observável na fonte.
- **2020–2021** são estruturais: o público é zero ou parcial por restrição
  sanitária, não por demanda.
- **Público é endógeno**: depende de adversário, fase, preço, clima e
  expectativa. O desenho observacional não isola a torcida.
- **Arbitragem**: identidade não é decisão; a base não tem cartões/pênaltis.
- **Não causalidade**: todas as leituras são descritivas.

## 8. Reprodução

```bash
# 1. Base dos Dados (requer gcloud ADC + projeto de billing)
python3 scripts/fetch_basedosdados.py --project SEU_PROJETO

# 2. FBref 2024: extrair o JSON no navegador (ver data/external/fbref/FONTE.md)
python3 scripts/parse_fbref.py --input .playwright-mcp/fbref_2024.json

# 3. Base limpa + relatório de qualidade
python3 scripts/build_external.py

# 4. Análise
python3 scripts/analyze_external.py
```

Os CSVs externos ficam em `data/external/` e não são versionados por
licença; scripts, metadados e este relatório são versionados.
