from pydantic import BaseModel, computed_field


class RankingEntry(BaseModel):
    rank: int
    points: float
    name_first: str
    name_last: str
    country: str
    height: float | None

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.name_first} {self.name_last}"

    model_config = {"from_attributes": True}


class PlayerResult(BaseModel):
    player_id: int
    name_first: str
    name_last: str
    country: str
    height: float | None

    @computed_field
    @property
    def name(self) -> str:
        return f"{self.name_first} {self.name_last}"

    model_config = {"from_attributes": True}
