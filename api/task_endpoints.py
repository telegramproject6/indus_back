from fastapi import APIRouter, Query, HTTPException

from schemas.schemas_in import MarkTaskDoneIn, IncreaseTotalgotSchemaIn

from database.database_queries import TaskTasksDB2, TaskMyDB2


router = APIRouter(
    tags=['Task endpoints']
)


# ─────────────────────── Task endpoints ─────────────────────────
@router.get('/get_user_tasks')
async def get_user_tasks(userid: str = Query(...)):
    print(userid)

    result = await TaskTasksDB2.get_user_tasks(userid)

    return result

# ----------------------------------------------------------------------------------------------------------------------

@router.post('/mark_task_done')
async def mark_task_done(user: MarkTaskDoneIn):
    print(user)

    result = await TaskTasksDB2.mark_task_done(user)

    return result

# ----------------------------------------------------------------------------------------------------------------------

@router.post('/increase_totalgot')
async def increase_totalgot(user_data: IncreaseTotalgotSchemaIn):
    print(user_data)

    result = await TaskMyDB2.increase_totalgot(user_data)

    return result

# ----------------------------------------------------------------------------------------------------------------------
# ────────────────── Telegram status helper ───────────────────────
BOT_TOKEN = "7846799651:AAGOt2D3udtnh9Aos0haWQUfiRIUVTbefwg"
TG_API    = f"https://api.telegram.org/bot{BOT_TOKEN}"


import requests
@router.get('/check_telegram_status')
async def check_telegram_status(user_id: str = Query(...), chat_id: str = Query(...)):
    print(user_id)
    print(chat_id)

    if not user_id or not chat_id:
        return HTTPException(status_code=400, detail={"error": "user_id and chat_id are required"})


    resp = requests.get(f"{TG_API}/getChatMember",
                        params={"chat_id": chat_id, "user_id": user_id},
                        timeout=10).json()
    if resp.get("ok") and resp["result"].get("status") in {"member", "administrator", "creator"}:
        return {"status": "1"}
    return {"status": "0"}
