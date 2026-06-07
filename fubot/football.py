"""Cliente da API-Football (via RapidAPI) para dados e estatísticas de futebol.

Usa apenas a biblioteca padrão (``urllib``) — sem dependências externas.

A chave de acesso é lida da variável de ambiente ``APIFOOTBALL_KEY``.
Pegue uma chave grátis em https://rapidapi.com/api-sports/api/api-football
e configure-a assim (PowerShell, permanente):

    setx APIFOOTBALL_KEY "sua-chave-aqui"
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_HOST = "api-football-v1.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}/v3"


class FootballError(Exception):
    """Erro ao falar com a API-Football (chave ausente, rede, resposta inválida)."""


def _api_key():
    key = os.environ.get("APIFOOTBALL_KEY")
    if not key:
        raise FootballError(
            "A variável de ambiente APIFOOTBALL_KEY não está definida. "
            "Pegue uma chave grátis em "
            "https://rapidapi.com/api-sports/api/api-football e rode: "
            'setx APIFOOTBALL_KEY "sua-chave"'
        )
    return key


def _get(path, params=None):
    """Faz um GET na API-Football e devolve o campo ``response`` do JSON.

    Esta é a única função que toca a rede; nos testes ela é substituída
    por uma versão falsa, então o resto do módulo pode ser testado offline.
    """
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "x-rapidapi-key": _api_key(),
            "x-rapidapi-host": API_HOST,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise FootballError(
            f"A API respondeu com erro HTTP {exc.code}. "
            "Verifique sua chave e seu plano no RapidAPI."
        ) from exc
    except urllib.error.URLError as exc:
        raise FootballError(f"Falha de conexão com a API: {exc.reason}") from exc

    errors = payload.get("errors")
    if errors:
        raise FootballError(f"A API retornou erros: {errors}")
    return payload.get("response", [])


def search_team(name):
    """Procura times pelo nome.

    Devolve uma lista de dicionários ``{id, nome, pais}``.
    O ``id`` é usado nas outras funções.
    """
    response = _get("/teams", {"search": name})
    times = []
    for item in response:
        team = item.get("team", {})
        times.append(
            {
                "id": team.get("id"),
                "nome": team.get("name"),
                "pais": team.get("country"),
            }
        )
    return times


def team_statistics(team_id, league_id, season):
    """Estatísticas de um time em uma liga/temporada.

    ``team_id`` e ``league_id`` são números (use :func:`search_team` para
    descobrir o id do time). ``season`` é o ano, ex.: ``2023``.
    """
    response = _get(
        "/teams/statistics",
        {"team": team_id, "league": league_id, "season": season},
    )
    return _parse_team_statistics(response)


def _parse_team_statistics(response):
    if not response:
        return None
    fixtures = response.get("fixtures", {})
    goals = response.get("goals", {})
    league = response.get("league", {})
    return {
        "time": response.get("team", {}).get("name"),
        "liga": league.get("name"),
        "temporada": league.get("season"),
        "forma": response.get("form"),
        "jogos": fixtures.get("played", {}).get("total"),
        "vitorias": fixtures.get("wins", {}).get("total"),
        "empates": fixtures.get("draws", {}).get("total"),
        "derrotas": fixtures.get("loses", {}).get("total"),
        "gols_pro": goals.get("for", {}).get("total", {}).get("total"),
        "gols_contra": goals.get("against", {}).get("total", {}).get("total"),
    }


def fixture_statistics(fixture_id):
    """Estatísticas de uma partida (chutes, posse de bola, etc.).

    ``fixture_id`` é o número da partida na API. Devolve uma lista com um
    bloco por time: ``{time, estatisticas}``.
    """
    response = _get("/fixtures/statistics", {"fixture": fixture_id})
    return _parse_fixture_statistics(response)


def _parse_fixture_statistics(response):
    blocos = []
    for bloco in response:
        estatisticas = {
            item.get("type"): item.get("value")
            for item in bloco.get("statistics", [])
        }
        blocos.append(
            {
                "time": bloco.get("team", {}).get("name"),
                "estatisticas": estatisticas,
            }
        )
    return blocos
