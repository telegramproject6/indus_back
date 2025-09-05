from sqlalchemy import select, update, func, insert
from fastapi import HTTPException
from typing import Optional

from database.create_db import new_session_mydatabase2, MyDB2, new_session_tasks, TasksDB2Taskdone
from schemas.schemas_in import (AadUserSchemaIn, UpdateUserSchemaIn, MarkTaskDoneIn, IncreaseTotalgotSchemaIn,
                                GamerSchemaIn, UpdateGamerSchemaIn)


class TaskMyDB2:
    @classmethod
    async def add_user(cls, data: AadUserSchemaIn):
        async with new_session_mydatabase2() as session:
            # Проверка наличия пользователя
            existing_user = await session.execute(
                select(MyDB2).where(MyDB2.UserId == str(data.UserId))
            )
            if existing_user.scalar_one_or_none():
                return {"message": "User already exists"}

            # Создание нового пользователя
            user = MyDB2(
                UserId=str(data.UserId),
                totalgot=0,
                invitedby=str(data.invitedby),
                miningstarttime='0',
                timeinminute='180',
                rate='0',
                youtube=None,
                instagram=None,
                discord=None,
                telegram=None,
                X=None,
                facebook=None,
                Username=str(data.Username),
                dailycombotime=0,
                dailyclaimedtime=0,
                alreadydailyclaimed=0,
                walletid=None
            )

            session.add(user)
            await session.commit()

            return {"message": "User added"}


    @classmethod
    async def get_user(cls, user_id: str):
        if not user_id:
            return HTTPException(status_code=400, detail={"error": "UserId is required"})

        async with new_session_mydatabase2() as session:
            result = await session.execute(
                select(MyDB2).where(MyDB2.UserId == str(user_id))
            )
            user = result.scalar_one_or_none()

            if not user:
                return HTTPException(status_code=404, detail={"error": "User not found"})

            # Преобразуем объект Users в словарь
            user_dict = {c.name: getattr(user, c.name) for c in user.__table__.columns}

            return {"data": user_dict}


    @classmethod
    async def update_user(cls, data: UpdateUserSchemaIn):
        data_dict = data.model_dump(exclude_unset=True)  # или .dict() в зависимости от версии Pydantic
        user_id = data_dict.pop("UserId", None)

        if not user_id or not data_dict:
            raise HTTPException(status_code=400, detail={"error": "UserId and at least one field are required"})

        async with new_session_mydatabase2() as session:
            stmt = (
                update(MyDB2)
                .where(MyDB2.UserId == str(user_id))
                .values(**data_dict)
            )
            result = await session.execute(stmt)
            await session.commit()

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail={"error": "User not found"})

            return {"message": "User updated"}


    @classmethod
    async def get_invitations_1(cls, user_id: str):
        if not user_id:
            raise HTTPException(status_code=400, detail={"error": "UserId is required"})

        async with new_session_mydatabase2() as session:
            # Получаем referrewarded
            reward_result = await session.execute(
                select(MyDB2.referrewarded).where(MyDB2.UserId == str(user_id))
            )
            reward_row = reward_result.scalar_one_or_none()
            reward_val = reward_row if reward_row is not None else None
            print(reward_val)

            # Получаем список приглашённых
            invited_result = await session.execute(
                select(MyDB2.Username, MyDB2.totalgot)
                .where(MyDB2.invitedby == str(user_id))
                .where(MyDB2.UserId != MyDB2.invitedby)
            )
            invited_rows = invited_result.all()

            invitations = [{"Username": row.Username, "totalgot": row.totalgot} for row in invited_rows]
            print(invitations)

            return {
                "invitations": invitations,
                "referrewarded": reward_val
            }

    @classmethod
    async def get_user_ranking(cls, user_id: str):
        if not user_id:
            raise HTTPException(status_code=400, detail={"error": "UserId is required"})

        async with new_session_mydatabase2() as session:
            # Топ 100 пользователей по totalgot
            top_result = await session.execute(
                select(MyDB2.UserId, MyDB2.Username, MyDB2.totalgot)
                .order_by(MyDB2.totalgot.desc())
                .limit(100)
            )
            top_rows = top_result.all()

            top_users = [
                {"rank": i + 1, "username": row.Username, "totalgot": row.totalgot}
                for i, row in enumerate(top_rows)
            ]

            # Информация о конкретном пользователе
            user_result = await session.execute(
                select(MyDB2.UserId, MyDB2.Username, MyDB2.totalgot)
                .where(MyDB2.UserId == str(user_id))
            )
            user_row = user_result.one_or_none()

            if user_row is not None:
                user_totalgot = user_row.totalgot

                # Подсчёт сколько пользователей с totalgot больше, чем у запрашиваемого
                count_result = await session.execute(
                    select(func.count()).select_from(MyDB2).where(MyDB2.totalgot > user_totalgot)
                )
                higher_count = count_result.scalar_one()

                requested_user = {
                    "position": higher_count + 1,
                    "username": user_row.Username,
                    "totalgot": user_row.totalgot,
                }
            else:
                requested_user = {"error": "User not found"}

            # Общее количество пользователей
            total_result = await session.execute(
                select(func.count()).select_from(MyDB2)
            )
            total_users = total_result.scalar_one()

            return {
                "requested_user": requested_user,
                "top_users": top_users,
                "total_users": f"{total_users / 1000:.3f}k"
            }

    @classmethod
    async def increase_totalgot(cls, data: IncreaseTotalgotSchemaIn):
        user_id = data.UserId
        amount = float(data.Amount)
        if not user_id or amount is None:
            raise HTTPException(
                status_code=400,
                detail={"error": "UserId and Amount are required"}
            )

        async with new_session_mydatabase2() as session:
            # Получаем текущее значение totalgot
            result = await session.execute(
                select(MyDB2.totalgot).where(MyDB2.UserId == str(user_id))
            )
            current_total: Optional[int] = result.scalar_one_or_none()

            if current_total is None:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "User not found"}
                )

            new_total = current_total + amount

            # Обновляем
            stmt = update(MyDB2).where(MyDB2.UserId == str(user_id)).values(totalgot=new_total)
            await session.execute(stmt)
            await session.commit()

            return {"totalgot": new_total}


class TaskTasksDB2:
    @classmethod
    async def get_user_tasks(cls, user_id: str):
        if not user_id:
            raise HTTPException(status_code=400, detail={"error": "userid is required"})

        async with new_session_tasks() as session:
            # Получаем все задачи
            tasks_result = await session.execute(
                select(TasksDB2Taskdone)
            )
            tasks = tasks_result.scalars().all()

            # Получаем список выполненных задач
            done_result = await session.execute(
                select(TasksDB2Taskdone.tasks).where(TasksDB2Taskdone.userid == str(user_id))
            )
            done: Optional[str] = done_result.scalar_one_or_none()

            return {
                "task_details": [
                    {c.name: getattr(task, c.name) for c in task.__table__.columns}
                    for task in tasks
                ],
                "completed_tasks": done
            }

    @classmethod
    async def mark_task_done(cls, data: MarkTaskDoneIn):
        user_id = data.userid
        task_id = data.taskid

        if not user_id or not task_id:
            raise HTTPException(
                status_code=400,
                detail={"error": "userid and taskid are required"}
            )

        async with new_session_tasks() as session:
            # Проверяем, есть ли уже запись для пользователя
            result = await session.execute(
                select(TasksDB2Taskdone.tasks).where(TasksDB2Taskdone.userid == str(user_id))
            )
            existing_tasks: Optional[str] = result.scalar_one_or_none()

            if existing_tasks is None:
                # Создаем новую запись
                stmt = insert(TasksDB2Taskdone).values(userid=str(user_id), tasks=str(task_id))
                await session.execute(stmt)
                await session.commit()
                return {"message": "Task marked done"}

            # Преобразуем задачи в множество
            tasks_set = set(filter(None, existing_tasks.split(",")))
            if str(task_id) in tasks_set:
                return {"message": "Task already done"}

            tasks_set.add(str(task_id))
            updated_tasks = ",".join(sorted(tasks_set))

            # Обновляем запись
            stmt = update(TasksDB2Taskdone).where(TasksDB2Taskdone.userid == str(user_id)).values(tasks=updated_tasks)
            await session.execute(stmt)
            await session.commit()

            return {"message": "Task marked done"}


class GamerService:

    @classmethod
    async def get_or_add_gamer(cls, data: GamerSchemaIn):
        gamer_id = data.GamerId

        if not gamer_id:
            raise HTTPException(
                status_code=400,
                detail={"error": "GamerId is required"}
            )

        async with new_session_tasks() as session:
            # Проверяем, существует ли игрок
            result = await session.execute(
                select(TasksDB2Taskdone).where(TasksDB2Taskdone.userid == str(gamer_id))
            )
            row: Optional[TasksDB2Taskdone] = result.scalar_one_or_none()

            if row:
                return {"data": {c.name: getattr(row, c.name) for c in row.__table__.columns}}

            # Если не существует — создаем
            stmt = insert(TasksDB2Taskdone).values(
                userid=str(gamer_id),
                hookspeed=1,
                multiplier=1,
                hookspeedtime=0,
                multipliertime=0,
                startime=0,
                starmultiplier=1
            )
            await session.execute(stmt)
            await session.commit()

            # Получаем созданную запись
            result = await session.execute(
                select(TasksDB2Taskdone).where(TasksDB2Taskdone.userid == str(gamer_id))
            )
            new_row: TasksDB2Taskdone = result.scalar_one_or_none()

            if not new_row:
                raise HTTPException(
                    status_code=500,
                    detail={"error": "Failed to create gamer"}
                )

            return {"data": {c.name: getattr(new_row, c.name) for c in new_row.__table__.columns}}

    @classmethod
    async def update_gamer(cls, data_schema: UpdateGamerSchemaIn):
        data = data_schema.model_dump(exclude_unset=True)  # или .dict() в зависимости от версии Pydantic
        gamer_id = data.pop("GamerId", None)

        if not gamer_id or not data:
            raise HTTPException(
                status_code=400,
                detail={"error": "GamerId and at least one field are required"}
            )

        async with new_session_tasks() as session:
            # Проверяем, существует ли такой игрок
            result = await session.execute(
                select(TasksDB2Taskdone).where(TasksDB2Taskdone.userid == str(gamer_id))
            )
            row: Optional[TasksDB2Taskdone] = result.scalar_one_or_none()

            if not row:
                raise HTTPException(
                    status_code=404,
                    detail={"error": "Gamer not found"}
                )

            # Обновляем только переданные поля
            stmt = (
                update(TasksDB2Taskdone)
                .where(TasksDB2Taskdone.userid == str(gamer_id))
                .values(**data)
            )
            await session.execute(stmt)
            await session.commit()

            return {"message": "Gamer updated"}


"""
class TaskMyDB2:
    @classmethod
    async def add_one(cls, data: AadUserSchemaIn):
        async with new_session_mydatabase2() as session:
            task_dict = data.model_dump()

            task = MyDB2(**task_dict)
            session.add(task)
            await session.commit()

    @classmethod
    async def get_user(cls, user_id: str):
        async with new_session_mydatabase2() as session:
            stmt = select(MyDB2).where(MyDB2.UserId == user_id)
            result = await session.execute(stmt)
            row = result.scalar_one_or_none()  # Возвращает ORM-объект или None
            return {k: v for k, v in row.__dict__.items() if k != "_sa_instance_state"} if row else None

    @classmethod
    async def update_user(cls, data: UpdateUserSchemaIn, name_column: str):
        async with new_session_mydatabase2() as session:
            # Преобразуем Pydantic-схему в словарь
            user_dict = data.model_dump(exclude_unset=True)

            # Достаём UserId
            user_id = user_dict.pop(name_column, None)
            if user_id is None:
                raise ValueError("В данных отсутствует 'UserId'")

            # Формируем UPDATE-запрос
            stmt = (
                update(MyDB2)
                .where(MyDB2.UserId == user_id)
                .values(**user_dict)
            )
            await session.execute(stmt)
            await session.commit()
"""
