"""fubot — utilitários simples e informações de futebol."""

from .bot import greet, add, shout
from .football import (
    FootballError,
    search_team,
    team_statistics,
    fixture_statistics,
)

__all__ = [
    "greet",
    "add",
    "shout",
    "FootballError",
    "search_team",
    "team_statistics",
    "fixture_statistics",
]
__version__ = "0.2.0"
