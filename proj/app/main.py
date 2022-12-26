from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import os

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
            admin_usr = Users(username="admin", password="password")
            one_session.add(admin_usr)
            await one_session.commit()


@app.exception_handler(security.NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: security.NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url='/')