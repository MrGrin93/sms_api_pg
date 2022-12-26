from fastapi import Depends, APIRouter, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_login import LoginManager #Loginmanager Class
from fastapi_login.exceptions import InvalidCredentialsException
from app.db.db import *
from .config import SECRET
# security = HTTPBasic()

# async def get_current_username(session: AsyncSession = Depends(get_session), credentials: HTTPBasicCredentials = Depends(security)):
#     result_user = await session.execute(select(Users).filter(Users.username == credentials.username, Users.password == credentials.password))
#     user = result_user.scalars().all()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username

class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(SECRET,"/auth/login",use_cookie=True, custom_exception=NotAuthenticatedException)
# manager.cookie_name = "some-name"

router = APIRouter()

@manager.user_loader()
async def load_user(username:str):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as one_session:
        try:
            result_user = await one_session.execute(select(Users).where(Users.username == username))
            user = result_user.scalars().one()
        except:
            raise NotAuthenticatedException
    return user

@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = await load_user(username)
    print(user)
    if not user:
        print("User not found")
        raise InvalidCredentialsException
    elif password != user.password:
        print("Password not correct")
        raise NotAuthenticatedException
    print("User correct")
    access_token = manager.create_access_token(
        data=dict(sub=user.username)
    )

    #print(access_token.decode("utf-8"))
    resp = RedirectResponse(url="/index",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    return resp