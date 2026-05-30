from sqlalchemy import Column, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Player(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True)
    name_first = Column(Text)
    name_last = Column(Text)
    hand = Column(Text)
    dob = Column(Float)
    ioc = Column(Text)
    height = Column(Float)
    wikidata_id = Column(Text)

    rankings = relationship("Ranking", back_populates="player_ref")


class Ranking(Base):
    __tablename__ = "rankings"

    ranking_date = Column(Integer, primary_key=True)
    rank = Column(Integer, primary_key=True)
    player = Column(Integer, ForeignKey("players.player_id"), primary_key=True)
    points = Column(Float)

    player_ref = relationship("Player", back_populates="rankings")
