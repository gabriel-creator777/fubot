"""Interface de linha de comando do fubot.

Exemplos:

    python -m fubot time "Flamengo"
    python -m fubot estatisticas 127 71 2023
    python -m fubot jogo 215662
"""

import sys

from . import football

AJUDA = """fubot — informações de futebol

Uso:
  python -m fubot time <nome>                  Procura um time e mostra o id
  python -m fubot estatisticas <time> <liga> <temporada>
                                               Estatísticas do time na temporada
  python -m fubot jogo <id_da_partida>         Estatísticas de uma partida

Antes de usar, configure sua chave do RapidAPI:
  setx APIFOOTBALL_KEY "sua-chave"
(e abra um novo terminal)
"""


def _cmd_time(args):
    if len(args) != 1:
        print('Uso: python -m fubot time "<nome>"', file=sys.stderr)
        return 2
    times = football.search_team(args[0])
    if not times:
        print("Nenhum time encontrado.")
        return 0
    print(f"{'id':>7}  {'time':<28} país")
    print("-" * 50)
    for t in times:
        print(f"{t['id']!s:>7}  {t['nome'] or '?':<28} {t['pais'] or ''}")
    return 0


def _cmd_estatisticas(args):
    if len(args) != 3:
        print(
            "Uso: python -m fubot estatisticas <time> <liga> <temporada>",
            file=sys.stderr,
        )
        return 2
    time_id, liga_id, temporada = args
    stats = football.team_statistics(time_id, liga_id, temporada)
    if not stats:
        print("Sem estatísticas para esses parâmetros.")
        return 0
    print(f"{stats['time']} — {stats['liga']} ({stats['temporada']})")
    print(f"  Forma recente : {stats['forma']}")
    print(f"  Jogos         : {stats['jogos']}")
    print(
        f"  V/E/D         : {stats['vitorias']}/"
        f"{stats['empates']}/{stats['derrotas']}"
    )
    print(f"  Gols pró      : {stats['gols_pro']}")
    print(f"  Gols contra   : {stats['gols_contra']}")
    return 0


def _cmd_jogo(args):
    if len(args) != 1:
        print("Uso: python -m fubot jogo <id_da_partida>", file=sys.stderr)
        return 2
    blocos = football.fixture_statistics(args[0])
    if not blocos:
        print("Sem estatísticas para essa partida.")
        return 0
    for bloco in blocos:
        print(f"\n{bloco['time']}")
        for tipo, valor in bloco["estatisticas"].items():
            print(f"  {tipo:<22} {valor}")
    return 0


COMANDOS = {
    "time": _cmd_time,
    "estatisticas": _cmd_estatisticas,
    "jogo": _cmd_jogo,
}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "ajuda"):
        print(AJUDA)
        return 0
    comando = COMANDOS.get(argv[0])
    if comando is None:
        print(f"Comando desconhecido: {argv[0]}\n", file=sys.stderr)
        print(AJUDA)
        return 2
    try:
        return comando(argv[1:])
    except football.FootballError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
