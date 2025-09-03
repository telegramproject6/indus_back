from pydantic import BaseModel


# ─────────────────────── User endpoints ──────────────────────────
class AadUserSchemaOut(BaseModel):
    message: str

class GetUserSchemaOut(BaseModel):
    data: dict

class UpdateUserSchemaOut(BaseModel):
    message: str


# ───────────────────── Invitation / referral ─────────────────────
class GetInvitationsSchemaOut(BaseModel):
    invitations: list
    referrewarded: str

class GetCreationMonthCountSchemaOut(BaseModel):
    user_id: int
    years: int
    months: int
    reward: int


# ─────────────────────── Leaderboard ─────────────────────────────
class GetUserRankingSchemaOut(BaseModel):
    requested_user: dict
    top_users: list
    total_users: str


# ─────────────────────── Task endpoints ─────────────────────────
class GetUserTasksSchemaOut(BaseModel):
    task_details: list
    completed_tasks: str

class MarkTaskDoneSchemaOut(BaseModel):
    message: str

class IncreaseTotalgotSchemaOut(BaseModel):
    totalgot: str

class CheckTelegramStatusSchemaOut(BaseModel):
    status: str


# ─────────────────────── Game endpoints ─────────────────────────
class GamerSchemaOut(BaseModel):
    data: dict

class UpdateGamerSchemaOut(BaseModel):
    message: str


class ErrorResponseSchemaOut(BaseModel):
    error: str
