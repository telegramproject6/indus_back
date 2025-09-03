from fastapi import APIRouter, Query

from database.database_queries import TaskMyDB2


router = APIRouter(
    tags=['Leaderboard']
)


# ─────────────────────── Leaderboard ─────────────────────────────
@router.get('/get_user_ranking')
async def get_user_ranking(UserId: str = Query(...)):

    print(UserId)

    result = await TaskMyDB2.get_user_ranking(UserId)

    return result
