import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from database.create_db import create_tables_mydb, create_tables_game, create_tables_tasks
from api.task_endpoints import router as task_endpoints_router
from api.leaderboard import router as leaderboard_router
from api.invitation_or_referral import router as invitation_or_referral_router
from api.user_endpoints import router as user_endpoints_router
from api.game_endpoints import router as game_endpoints_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables_mydb()
    await create_tables_game()
    await create_tables_tasks()
    print('Start_db')

    yield
    print('Exit')


app = FastAPI(lifespan=lifespan)
app.include_router(user_endpoints_router)
app.include_router(invitation_or_referral_router)
app.include_router(leaderboard_router)
app.include_router(task_endpoints_router)
app.include_router(game_endpoints_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить ["http://localhost:5000"]
    allow_credentials=True,
    allow_methods=["*"],   # разрешаем все методы
    allow_headers=["*"],   # разрешаем все заголовки
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload= True, host='localhost', port=5000)
