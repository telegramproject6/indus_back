from fastapi import APIRouter, HTTPException, Query

from database.database_queries import TaskMyDB2


router = APIRouter(
    tags=['Invitation / referral']
)


# ───────────────────── Invitation / referral ─────────────────────
@router.get('/get_invitations')
async def get_invitations(UserId: str = Query(...)):

    print(UserId)

    result = await TaskMyDB2.get_invitations_1(UserId)

    return result

# ----------------------------------------------------------------------------------------------------------------------

from datetime import datetime
from dateutil.relativedelta import relativedelta
# ──────────────── ID → creation-date predictor ───────────────────
entries = [  # (id, unix_time)
    [1000000, 1380326400], [2768409, 1383264000], [7679610, 1388448000],
    # … (list truncated – keep full list from original code)
    [6925870357, 1701192327]
]
entries.sort(key=lambda x: x[0])

def predict_creation_date(user_id: int) -> datetime:
    print(user_id)
    if user_id <= entries[0][0]:
        return datetime.fromtimestamp(entries[0][1])
    for i in range(1, len(entries)):
        lo_id, lo_ts = entries[i - 1]
        hi_id, hi_ts = entries[i]
        if lo_id <= user_id <= hi_id:
            t = (user_id - lo_id) / (hi_id - lo_id)
            return datetime.fromtimestamp(int(lo_ts + t * (hi_ts - lo_ts)))
    return datetime.fromtimestamp(entries[-1][1])


@router.get('/get_creation_month_count')
async def get_creation_month_count(userid: str = Query(...)):
    try:
        userid = int(userid)
        print(userid)
    except (TypeError, ValueError):
        return HTTPException(status_code=400, detail={"error": "Invalid or missing userid"})

    creation = predict_creation_date(userid)
    delta    = relativedelta(datetime.now(), creation)
    months   = delta.years * 12 + delta.months

    if months < 12:
        reward = 30000
    elif months < 24:
        reward = 50000
    elif months < 36:
        reward = 60000
    elif months < 48:
        reward = 70000
    elif months < 60:
        reward = 80000
    else:
        reward = 100000

    return {
        "user_id": userid,
        "years": round(months / 12.0, 1),
        "months": months,
        "reward": reward
    }
