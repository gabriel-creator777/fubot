import unittest
from unittest import mock

from fubot import football
from fubot.__main__ import main


# --- Amostras de resposta da API (formato real, reduzido) ---

TEAMS_SAMPLE = [
    {"team": {"id": 127, "name": "Flamengo", "country": "Brazil"}},
    {"team": {"id": 124, "name": "Fluminense", "country": "Brazil"}},
]

TEAM_STATS_SAMPLE = {
    "team": {"name": "Flamengo"},
    "league": {"name": "Serie A", "season": 2023},
    "form": "WWDLW",
    "fixtures": {
        "played": {"total": 38},
        "wins": {"total": 21},
        "draws": {"total": 8},
        "loses": {"total": 9},
    },
    "goals": {
        "for": {"total": {"total": 60}},
        "against": {"total": {"total": 40}},
    },
}

FIXTURE_STATS_SAMPLE = [
    {
        "team": {"name": "Flamengo"},
        "statistics": [
            {"type": "Shots on Goal", "value": 7},
            {"type": "Ball Possession", "value": "58%"},
        ],
    },
    {
        "team": {"name": "Fluminense"},
        "statistics": [
            {"type": "Shots on Goal", "value": 3},
            {"type": "Ball Possession", "value": "42%"},
        ],
    },
]


class TestApiKey(unittest.TestCase):
    def test_api_key_ausente_gera_erro(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(football.FootballError):
                football._api_key()

    def test_api_key_presente(self):
        with mock.patch.dict("os.environ", {"APIFOOTBALL_KEY": "abc"}):
            self.assertEqual(football._api_key(), "abc")


class TestParsers(unittest.TestCase):
    def test_search_team(self):
        with mock.patch.object(football, "_get", return_value=TEAMS_SAMPLE):
            times = football.search_team("Fla")
        self.assertEqual(times[0], {"id": 127, "nome": "Flamengo", "pais": "Brazil"})
        self.assertEqual(len(times), 2)

    def test_team_statistics(self):
        with mock.patch.object(football, "_get", return_value=TEAM_STATS_SAMPLE):
            stats = football.team_statistics(127, 71, 2023)
        self.assertEqual(stats["time"], "Flamengo")
        self.assertEqual(stats["jogos"], 38)
        self.assertEqual(stats["vitorias"], 21)
        self.assertEqual(stats["gols_pro"], 60)
        self.assertEqual(stats["gols_contra"], 40)

    def test_team_statistics_vazio(self):
        with mock.patch.object(football, "_get", return_value=[]):
            self.assertIsNone(football.team_statistics(1, 1, 2023))

    def test_fixture_statistics(self):
        with mock.patch.object(football, "_get", return_value=FIXTURE_STATS_SAMPLE):
            blocos = football.fixture_statistics(215662)
        self.assertEqual(len(blocos), 2)
        self.assertEqual(blocos[0]["time"], "Flamengo")
        self.assertEqual(blocos[0]["estatisticas"]["Shots on Goal"], 7)
        self.assertEqual(blocos[1]["estatisticas"]["Ball Possession"], "42%")

    def test_get_propaga_erros_da_api(self):
        payload = {"errors": {"token": "inválido"}, "response": []}
        with mock.patch.dict("os.environ", {"APIFOOTBALL_KEY": "x"}):
            with mock.patch("fubot.football.urllib.request.urlopen") as urlopen:
                ctx = urlopen.return_value.__enter__.return_value
                ctx.read.return_value = __import__("json").dumps(payload).encode()
                with self.assertRaises(football.FootballError):
                    football._get("/teams", {"search": "x"})


class TestCli(unittest.TestCase):
    def test_ajuda_sem_argumentos(self):
        self.assertEqual(main([]), 0)

    def test_comando_desconhecido(self):
        self.assertEqual(main(["xpto"]), 2)

    def test_cli_time(self):
        with mock.patch.object(football, "search_team", return_value=[
            {"id": 127, "nome": "Flamengo", "pais": "Brazil"}
        ]):
            self.assertEqual(main(["time", "Flamengo"]), 0)

    def test_cli_erro_de_football_vira_codigo_1(self):
        with mock.patch.object(
            football, "search_team", side_effect=football.FootballError("x")
        ):
            self.assertEqual(main(["time", "Flamengo"]), 1)


if __name__ == "__main__":
    unittest.main()
