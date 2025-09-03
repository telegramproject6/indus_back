from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ModelMydb2(DeclarativeBase):
    pass

mydatabase2_engine = create_async_engine(
    "sqlite+aiosqlite:///database/file_db/mydatabase2.db"
)
new_session_mydatabase2 = async_sessionmaker(mydatabase2_engine, expire_on_commit=False)

class MyDB2(ModelMydb2):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    UserId: Mapped[str]
    Username: Mapped[str] = mapped_column(nullable=True)
    Refertotal: Mapped[str] = mapped_column(nullable=True)
    X: Mapped[str] = mapped_column(nullable=True)
    alreadydailyclaimed: Mapped[int] = mapped_column(nullable=True)
    claimedtotal: Mapped[int] = mapped_column(nullable=True)
    dailyclaimedtime: Mapped[int] = mapped_column(nullable=True)
    dailycombotime: Mapped[int] = mapped_column(nullable=True)
    discord: Mapped[str] = mapped_column(nullable=True)
    facebook: Mapped[str] = mapped_column(nullable=True)
    instagram: Mapped[str] = mapped_column(nullable=True)
    invitedby: Mapped[str] = mapped_column(nullable=True)
    miningstarttime: Mapped[str] = mapped_column(nullable=True)
    rate: Mapped[str] = mapped_column(nullable=True)
    telegram: Mapped[str] = mapped_column(nullable=True)
    timeinminute: Mapped[str] = mapped_column(nullable=True)
    totalcollectabledaily: Mapped[str] = mapped_column(nullable=True)
    totalgot: Mapped[float] = mapped_column(nullable=True)
    youtube: Mapped[str] = mapped_column(nullable=True)
    walletid: Mapped[str] = mapped_column(nullable=True)
    referrewarded: Mapped[int] = mapped_column(nullable=True)
    task1: Mapped[str] = mapped_column(nullable=True)
    task2: Mapped[str] = mapped_column(nullable=True)
    task3: Mapped[str] = mapped_column(nullable=True)
    task4: Mapped[str] = mapped_column(nullable=True)
    task5: Mapped[str] = mapped_column(nullable=True)
    task6: Mapped[str] = mapped_column(nullable=True)
    task7: Mapped[str] = mapped_column(nullable=True)
    task8: Mapped[str] = mapped_column(nullable=True)
    task9: Mapped[str] = mapped_column(nullable=True)
    task10: Mapped[str] = mapped_column(nullable=True)
    task11: Mapped[str] = mapped_column(nullable=True)
    task12: Mapped[str] = mapped_column(nullable=True)
    task13: Mapped[str] = mapped_column(nullable=True)
    task14: Mapped[str] = mapped_column(nullable=True)
    task15: Mapped[str] = mapped_column(nullable=True)
    task16: Mapped[str] = mapped_column(nullable=True)
    task17: Mapped[str] = mapped_column(nullable=True)
    task18: Mapped[str] = mapped_column(nullable=True)
    task19: Mapped[str] = mapped_column(nullable=True)
    task20: Mapped[str] = mapped_column(nullable=True)
    tonwallet: Mapped[str] = mapped_column(nullable=True)
    tgid: Mapped[str] = mapped_column(nullable=True)
    number: Mapped[str] = mapped_column(nullable=True)
    cmcid: Mapped[str] = mapped_column(nullable=True)
    xid: Mapped[str] = mapped_column(nullable=True)
    ytid: Mapped[str] = mapped_column(nullable=True)
    igid: Mapped[str] = mapped_column(nullable=True)
    fbid: Mapped[str] = mapped_column(nullable=True)
    prelink: Mapped[str] = mapped_column(nullable=True)
    task21: Mapped[str] = mapped_column(nullable=True)
    task22: Mapped[str] = mapped_column(nullable=True)
    task23: Mapped[str] = mapped_column(nullable=True)
    task24: Mapped[str] = mapped_column(nullable=True)
    task25: Mapped[str] = mapped_column(nullable=True)
    task26: Mapped[str] = mapped_column(nullable=True)
    task27: Mapped[str] = mapped_column(nullable=True)
    task28: Mapped[str] = mapped_column(nullable=True)
    task29: Mapped[str] = mapped_column(nullable=True)
    task30: Mapped[str] = mapped_column(nullable=True)
    task31: Mapped[str] = mapped_column(nullable=True)
    task32: Mapped[str] = mapped_column(nullable=True)
    task33: Mapped[str] = mapped_column(nullable=True)
    task34: Mapped[str] = mapped_column(nullable=True)
    task35: Mapped[str] = mapped_column(nullable=True)
    Invite5Friends: Mapped[str] = mapped_column(nullable=True)

async def create_tables_mydb():
    async with mydatabase2_engine.begin() as conn_mydb:
        await conn_mydb.run_sync(MyDB2.metadata.create_all)

# ----------------------------------------------------------------------------------------------------------------------

class ModelGame(DeclarativeBase):
    pass

game_engine = create_async_engine(
    "sqlite+aiosqlite:///database/file_db/game.db"
)
new_session_game = async_sessionmaker(game_engine, expire_on_commit=False)

class GameDB2(ModelGame):
    __tablename__ = 'gamers'

    id: Mapped[int] = mapped_column(primary_key=True)
    userid: Mapped[str]
    hookspeed: Mapped[str] = mapped_column(nullable=True)
    multiplier: Mapped[str] = mapped_column(nullable=True)
    hookspeedtime: Mapped[str] = mapped_column(nullable=True)
    multipliertime: Mapped[str] = mapped_column(nullable=True)
    startime: Mapped[str] = mapped_column(nullable=True)
    starmultiplier: Mapped[str] = mapped_column(nullable=True)

async def create_tables_game():
    async with game_engine.begin() as conn_game:
        await conn_game.run_sync(ModelGame.metadata.create_all)

# ----------------------------------------------------------------------------------------------------------------------

class ModelTasks(DeclarativeBase):
    pass

tasks_engine = create_async_engine(
    "sqlite+aiosqlite:///database/file_db/Tasks.db"
)
new_session_tasks = async_sessionmaker(tasks_engine, expire_on_commit=False)

class TasksDB2Taskdone(ModelTasks):
    __tablename__ = 'Taskdone'

    id: Mapped[int] = mapped_column(primary_key=True)
    userid: Mapped[int]
    tasks: Mapped[str] = mapped_column(nullable=True)

async def create_tables_tasks():
    async with tasks_engine.begin() as conn_tasks:
        await conn_tasks.run_sync(ModelTasks.metadata.create_all)
