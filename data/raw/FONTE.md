# Proveniência dos dados brutos — `data/raw/`

## Arquivo auditado

- **Arquivo:** `campeonato-brasileiro-full.csv`
- **Repositório:** https://github.com/adaoduque/Brasileirao_Dataset (branch `master`)
- **Commit:** `15f027c3be337bb130d6ae94436b5cdca737377c`
- **Data do commit:** 2026-02-05 (mensagem: "Brasileirão 2025")
- **Data de acesso/download:** 2026-10-28
- **Tamanho:** 1.187.343 bytes
- **SHA-256:** `c09d03d36debfd7d7aee71da9a9f0909b5e420fc80a1705f215efc93c76e83fc`
- **Encoding:** UTF-8
- **URL direta:** https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/15f027c3be337bb130d6ae94436b5cdca737377c/campeonato-brasileiro-full.csv

## Arquivo complementar

- **Arquivo:** `Legenda.txt`
- **Tamanho:** 2.113 bytes
- **SHA-256:** `dfedf5fb55d9d7b178bce0e0e0b639c380d42d27af76a7d3ef1f1d6db6d1de1f`
- **URL direta:** https://raw.githubusercontent.com/adaoduque/Brasileirao_Dataset/15f027c3be337bb130d6ae94436b5cdca737377c/Legenda.txt

Os dois hashes são conferidos por `scripts/fetch_raw.py` após o download;
`python3 scripts/fetch_raw.py --check` valida as cópias locais sem baixar.

## Licença

- **Nenhum arquivo LICENSE no repositório** (API GitHub: `license: None`; `LICENSE` retorna 404 — verificado em 2026-10-28).
- O README do repositório apenas indica contato do autor: adaoduquesn@gmail.com / Telegram @adaoDuque.
- **Plano adotado (plano B): o CSV bruto NÃO é versionado.** O `.gitignore` exclui
- `data/raw/*.csv` (e `*.txt`). Para reproduzir: `python3 scripts/fetch_raw.py`
- (baixa do commit pinado acima e confere o SHA-256) e depois `python3 scripts/build_processed.py`.
- Para conferir cópias já baixadas sem acessar a rede: `python3 scripts/fetch_raw.py --check`.
- A base processada/derivada (`data/processed/`) contém apenas resultados factuais
- (placares) com coluna `source` de atribuição — prática padrão de citação acadêmica.

## Observações sobre a fonte

- A cobertura declarada vai de 2003 até 2025; o recorte do TCC (2006–2024) exige filtro explícito.
- O cabeçalho real do CSV difere da legenda oficial (`Legenda.txt`): a coluna de rodada chama-se `rodata` (typo) e não `Rodada`; a coluna `Dia` citada na legenda não existe no arquivo.
- Colunas `formacao_mandante`, `formacao_visitante`, `tecnico_mandante`, `tecnico_visitante` aparentam estar vazias nas temporadas antigas (fora do escopo do TCC; serão descartadas no pipeline).
- `vencedor` usa `-` para empate.

## Cópia imutável

Esta pasta é a cópia bruta de referência. O pipeline de limpeza (Fase 2) deve ler exclusivamente daqui e gravar em `data/processed/`, sem alterar este arquivo.
