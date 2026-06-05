# fubot

Um pequeno conjunto de utilitários em Python para mensagens de um bot simples.

## Funcionalidades

- `greet(name)` — monta uma saudação.
- `add(a, b)` — soma dois números.
- `shout(text)` — devolve o texto em maiúsculas com `!` no final.

## Uso

```python
from fubot.bot import greet, add, shout

print(greet("Mundo"))   # Olá, Mundo!
print(add(2, 3))        # 5
print(shout("oi"))      # OI!
```

## Rodando os testes

```bash
python -m unittest discover -s tests
```

## Licença

MIT
