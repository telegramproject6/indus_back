from pydantic import BaseModel
from typing import Optional


# ─────────────────────── User endpoints ──────────────────────────
class AadUserSchemaIn(BaseModel):
    UserId: str
    Username: str
    invitedby: str | None

class UpdateUserSchemaIn(BaseModel):     #TODO ??????
    UserId: str
    Username: Optional[str] = None
    Refertotal: Optional[str] = None
    X: Optional[str] = None
    alreadydailyclaimed: Optional[int] = 0
    claimedtotal: Optional[int] = 0
    dailyclaimedtime: Optional[int] = 0
    dailycombotime: Optional[int] = 0
    discord: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    invitedby: Optional[str] = None
    miningstarttime: Optional[str] = None
    rate: Optional[str] = None
    telegram: Optional[str] = None
    timeinminute: Optional[str] = None
    totalcollectabledaily: Optional[str] = None
    totalgot: Optional[float] = None
    youtube: Optional[str] = None
    walletid: Optional[str] = None
    referrewarded: Optional[int] = 0
    task1: Optional[str] = None
    task2: Optional[str] = None
    task3: Optional[str] = None
    task4: Optional[str] = None
    task5: Optional[str] = None
    task6: Optional[str] = None
    task7: Optional[str] = None
    task8: Optional[str] = None
    task9: Optional[str] = None
    task10: Optional[str] = None
    task11: Optional[str] = None
    task12: Optional[str] = None
    task13: Optional[str] = None
    task14: Optional[str] = None
    task15: Optional[str] = None
    task16: Optional[str] = None
    task17: Optional[str] = None
    task18: Optional[str] = None
    task19: Optional[str] = None
    task20: Optional[str] = None
    tonwallet: Optional[str] = None
    tgid: Optional[str] = None
    number: Optional[str] = None
    cmcid: Optional[str] = None
    xid: Optional[str] = None
    ytid: Optional[str] = None
    igid: Optional[str] = None
    fbid: Optional[str] = None
    prelink: Optional[str] = None
    task21: Optional[str] = None
    task22: Optional[str] = None
    task23: Optional[str] = None
    task24: Optional[str] = None
    task25: Optional[str] = None
    task26: Optional[str] = None
    task27: Optional[str] = None
    task28: Optional[str] = None
    task29: Optional[str] = None
    task30: Optional[str] = None
    task31: Optional[str] = None
    task32: Optional[str] = None
    task33: Optional[str] = None
    task34: Optional[str] = None
    task35: Optional[str] = None
    Invite5Friends: Optional[str] = None


# ───────────────────── Invitation / referral ─────────────────────

# ─────────────────────── Leaderboard ─────────────────────────────

# ─────────────────────── Task endpoints ─────────────────────────
class MarkTaskDoneIn(BaseModel):
    userid: str
    taskid: str

class IncreaseTotalgotSchemaIn(BaseModel):
    UserId: str
    Amount: str

# ─────────────────────── Game endpoints ─────────────────────────
class GamerSchemaIn(BaseModel):
    GamerId: str

class UpdateGamerSchemaIn(BaseModel):     # TODO ?????
    GamerId: str