# Fonte — cartões por partida (BrazilianFootball/Data)

- **Repositório:** https://github.com/BrazilianFootball/Data
- **Commit fixado:** `0dd1bc5f7da20130df460b9876e0bbbfebcbfa03`
- **DOI:** `10.5281/zenodo.15207727`
- **Licença:** MIT
- **Cobertura usada:** Série A 2013–2024 (380 jogos por temporada; 2016 com 379)
- **Arquivos locais:** `data/external/cards/Serie_A_<ano>_games.json` (não versionados)
- **Metadados:** `FETCH_METADATA.json` (URL, commit, SHA-256 por arquivo)

## O que o arquivo contém

Cada JSON é um dicionário de partidas. Por jogo, há:

- `Date`, `Time`, `Stadium`, `Home`, `Away`, `Result`;
- `Players`, `Goals`, `Changes`;
- **`Yellow cards`** e **`Red cards`**: listas com minuto, jogador e equipe
  (ex.: `"12:00 1T6Jean Lucas de Souza Oliveira Bahia/BA"`).

Os dados são extraídos dos **borderôs/súmulas oficiais da CBF** pelos
mantenedores do repositório.

## Limitações

- Cobre 2013–2024; **2006–2012 não tem cartões** nessa fonte.
- O nome da equipe no cartão pode vir abreviado e com sufixo empresarial
  (`Saf`, `S.a.f.`); o parser normaliza e registra não atribuídos.
- O arquivo não traz o árbitro; a arbitragem vem da Base dos Dados/Transfermarkt.
- Cartão é decisão do árbitro, mas também reflete comportamento do jogador;
  não é medida direta de viés.
- Licença MIT do repositório; os dados subjacentes são dos borderôs da CBF.
  Para o TCC, usar dados derivados com atribuição e não redistribuir o bruto
  sem verificar os termos da CBF.

## Reprodução

```bash
PYTHONPATH=src python3 scripts/fetch_cards.py
PYTHONPATH=src python3 scripts/fetch_cards.py --check
PYTHONPATH=src python3 scripts/build_cards.py
PYTHONPATH=src python3 scripts/analyze_cards.py
```
