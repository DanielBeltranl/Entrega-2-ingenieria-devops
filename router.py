from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import RankingEntry, PlayerResult
from service import get_top_players, find_players

router = APIRouter(prefix="/api")


@router.get("/rankings/top", response_model=list[RankingEntry])
def top_rankings(db: Session = Depends(get_db)):
    return get_top_players(db)


@router.get("/players/search", response_model=list[PlayerResult])
def search(q: str = Query(min_length=2), db: Session = Depends(get_db)):
    return find_players(db, q)
