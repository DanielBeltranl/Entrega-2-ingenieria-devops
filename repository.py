from sqlalchemy.orm import Session
from sqlalchemy import func, select
from models import Player, Ranking


def get_top_rankings(db: Session, limit: int = 5) -> list:
    latest_date = db.scalar(select(func.max(Ranking.ranking_date)))
    stmt = (
        select(
            Ranking.rank,
            Ranking.points,
            Player.name_first,
            Player.name_last,
            Player.ioc.label("country"),
            Player.height,
        )
        .join(Player, Ranking.player == Player.player_id)
        .where(Ranking.ranking_date == latest_date)
        .order_by(Ranking.rank)
        .limit(limit)
    )
    return db.execute(stmt).mappings().all()


def search_players(db: Session, q: str, limit: int = 20) -> list:
    subquery = select(Ranking.player).distinct()
    stmt = (
        select(
            Player.player_id,
            Player.name_first,
            Player.name_last,
            Player.ioc.label("country"),
            Player.height,
        )
        .where(Player.player_id.in_(subquery))
        .where(
            func.lower(Player.name_first + " " + Player.name_last).contains(
                q.lower()
            )
        )
        .limit(limit)
    )
    return db.execute(stmt).mappings().all()
