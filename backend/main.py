from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Stickman Dojo API")
router = APIRouter()

class PlayerMatchData(BaseModel):
    name: str
    color: str
    damageDealt: int
    hitsLanded: int
    blocksExecuted: int
    remainingHp: float

class MatchPayload(BaseModel):
    matchId: str
    timestamp: datetime
    durationSeconds: float
    winner: str
    players: dict[str, PlayerMatchData]
    currentSeriesScore: dict[str, int]

class MatchRecord(BaseModel):
    id: int
    matchId: str
    timestamp: datetime
    winner: str
    durationSeconds: float

fake_db = []

# routes
@router.post("/api/v1/matches", status_code=201, response_model=MatchRecord)
async def create_match(payload: MatchPayload):
    # Itt történne az adatbázisba mentés (MatchRepository használatával)
    record = MatchRecord(
        id=len(fake_db) + 1,
        matchId=payload.matchId,
        timestamp=payload.timestamp,
        winner=payload.winner,
        durationSeconds=payload.durationSeconds
    )
    fake_db.append(record)
    return record

@router.get("/api/v1/matches", response_model=list[MatchRecord])
async def list_matches():
    return fake_db

@router.get("/api/v1/leaderboard")
async def get_leaderboard():
    return [{"player": "Levi", "wins": 5}, {"player": "Lóránt", "wins": 3}]

@router.get("/api/v1/statistics")
async def get_statistics():
    return {"total_matches": len(fake_db)}

app.include_router(router)