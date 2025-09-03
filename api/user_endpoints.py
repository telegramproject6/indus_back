from fastapi import APIRouter, Query

from schemas.schemas_in import AadUserSchemaIn, UpdateUserSchemaIn

from database.database_queries import TaskMyDB2


router = APIRouter(
    tags=['User endpoints']
)


# ─────────────────────── User endpoints ──────────────────────────
@router.post('/add_user')
async def add_user(user_data: AadUserSchemaIn):

    print("Добавляем пользователя:")
    print("User ID:", user_data.UserId)
    print("Username:", user_data.Username)
    print("Invited by:", user_data.invitedby)

    result = await TaskMyDB2.add_user(user_data)

    return result

# ----------------------------------------------------------------------------------------------------------------------

@router.get('/get_user')
async def get_user(UserId: str = Query(...)):


    print("Добавляем пользователя:")
    print("User ID:", UserId)

    print(UserId)

    data_user = await TaskMyDB2.get_user(UserId)

    return data_user

# ----------------------------------------------------------------------------------------------------------------------

@router.post('/update_user')
async def update_user(user_data: UpdateUserSchemaIn):

    print(user_data)

    result = await TaskMyDB2.update_user(user_data)

    return result