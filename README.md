# fubot

[![Tests](https://github.com/gabriel-creator777/fubot/actions/workflows/tests.yml/badge.svg)](https://github.com/gabriel-creator777/fubot/actions/workflows/tests.yml)

Um pequeno conjunto de utilitários em Python para mensagens de um bot simples.

## Funcionalidades

- `greet(name)` — monta uma saudação.
- `add(a, b)` — soma dois números.
- `shout(text)` — devolve o texto em maiúsculas com `!` no final.
- **Futebol** — busca de times e estatísticas de time/partida via API-Football.

## Uso (utilitários)

```python
from fubot.bot import greet, add, shout

print(greet("Mundo"))   # Olá, Mundo!
print(add(2, 3))        # 5
print(shout("oi"))      # OI!
```

## Futebol ⚽

Os dados vêm da [API-Football](https://rapidapi.com/api-sports/api/api-football)
(via RapidAPI). Você precisa de uma chave grátis.

### 1. Pegue uma chave

1. Crie uma conta em [rapidapi.com](https://rapidapi.com).
2. Acesse a [página da API-Football](https://rapidapi.com/api-sports/api/api-football)
   e clique em **Subscribe to Test** → plano **Basic (Free)**.
3. Copie sua chave (campo `X-RapidAPI-Key`).

### 2. Configure a chave (PowerShell, permanente)

```powershell
setx APIFOOTBALL_KEY "sua-chave-aqui"
```

Depois **abra um novo terminal** para a variável valer.

### 3. Use pela linha de comando

```bash
python -m fubot time "Flamengo"               # descobre o id do time
python -m fubot estatisticas 127 71 2023      # <time> <liga> <temporada>
python -m fubot jogo 215662                    # estatísticas de uma partida
```

### 4. Ou use as funções em Python

```python
from fubot import search_team, team_statistics, fixture_statistics

times = search_team("Flamengo")
stats = team_statistics(team_id=127, league_id=71, season=2023)
jogo = fixture_statistics(fixture_id=215662)
```

> Observação: no plano grátis da API-Football algumas temporadas/ligas
> têm acesso limitado e há um limite diário de requisições.

## Rodando os testes

```bash
python -m unittest discover -s tests
```

## Licença

MIT
