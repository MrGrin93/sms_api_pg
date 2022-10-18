from typing import List
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn, os

from app.db.db import *
from app.models.models import *
from app.repo import index, api
from app.core import security


current_path = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory=f"{current_path}/static/css"), name="static")
app.include_router(security.router, prefix="/auth", tags=["auth"])
app.include_router(index.router, prefix="", tags=["index"])
app.include_router(api.router, prefix="/api", tags=["api"])

@app.on_event("startup")
async def create_admin_user():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as one_session:
        result_user = await one_session.execute(select(Users).filter(Users.username == "admin"))
        user = result_user.scalars().all()
        if not user:
            admin_usr = Users(username="admin", password="admin")
            one_session.add(admin_usr)
            await one_session.commit()


# if __name__ == "__main__":
#     uvicorn.run(app, port=8000)