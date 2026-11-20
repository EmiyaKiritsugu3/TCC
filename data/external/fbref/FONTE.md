# Fonte — FBref 2024

- **Página:** https://fbref.com/en/comps/24/2024/schedule/2024-Serie-A-Scores-and-Fixtures
- **Fonte:** FBref / Sports Reference
- **Cobertura:** 380 partidas da Série A 2024
- **Público:** 376 partidas (99,0%)
- **Árbitro:** 253 partidas (66,6%)
- **Estádio:** 380 partidas
- **SHA-256 do CSV:** `e2c14fbd5f7bbe4ac4423761574f280d470918edacbcd2e3af87308fa18808d7`
- **Arquivo local:** `2024_serie_a.csv` (não versionado)

## Como foi extraído

O FBref bloqueia requisições automatizadas com Cloudflare. A extração foi
feita em um navegador real, com a tabela `#sched_2024_24_1` carregada.
No console do navegador:

```js
const t = document.getElementById('sched_2024_24_1');
const rows = Array.from(t.rows).map(r => Array.from(r.cells).map(c => c.innerText.trim()));
const jogos = rows
  .filter(c => c.length === 12 && /^\d{4}-\d{2}-\d{2}$/.test(c[2]))
  .map(c => ({round: c[0], day: c[1], date: c[2], time: c[3], home: c[4],
              score: c[5], away: c[6], attendance: c[7], venue: c[8], referee: c[9]}));
console.log(JSON.stringify(jogos));
```

Salvar o JSON e rodar:

```bash
python3 scripts/parse_fbref.py --input caminho/para/fbref_2024.json
```

## Licença e uso

Sports Reference permite uso com restrições; não criar base concorrente,
não redistribuir o bruto e respeitar rate limit. Usar para validação
acadêmica e citar a fonte.
