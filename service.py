from sqlalchemy.orm import Session
from repository import get_top_rankings, search_players
from schemas import RankingEntry, PlayerResult


def get_top_players(db: Session, limit: int = 5) -> list[RankingEntry]:
    rows = get_top_rankings(db, limit)
    return [RankingEntry(**row) for row in rows]


def find_players(db: Session, q: str) -> list[PlayerResult]:
    rows = search_players(db, q)
    return [PlayerResult(**row) for row in rows]
