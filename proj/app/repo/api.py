from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import datetime
from app.db.db import *
from app.models.models import *

router = APIRouter()

@router.get('/api/sms/', response_model=List[SmsBase])
async def get_sms(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Sms))
    smss = result.scalars().all()
    return [Sms(number=sms.number, text=sms.text, id=sms.id, ul=sms.ul, date=sms.date) for sms in smss]

@router.get('/api/ul/', response_model=List[Ur_l])
async def get_ul(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Ur_l))
    ur_ls = result.scalars().all()
    return [Ur_l(ul=ur_l.ul, number=ur_l.number) for ur_l in ur_ls]


@router.post("/api/sms/", response_model=SmsBase)
async def create_post(sms: SmsCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Ur_l))
    ur_ls = result.scalars().all()
    ul_list = [
        {
            "number": u.number,
            "ul": u.ul
        }
        for u in ur_ls
    ]
    if {"ul":sms.ul, "number":sms.ul_number} not in ul_list:
        ur_l_new = Ur_l(ul=sms.ul, number=sms.ul_number)
        session.add(ur_l_new)
        await session.commit()
        await session.refresh(ur_l_new)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    sms_new = Sms(number=sms.number, text=sms.text, ul=sms.ul, date=date)
    session.add(sms_new)
    await session.commit()
    await session.refresh(sms_new)
    
    # return {**sms_new, "date": date}

@router.get('/api/get-users/')
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Users))
    users = result.scalars().all()
    return users

@router.post('/api/signup/', response_model=Users)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Users).filter(Users.username == user.username))
    user_exist = result.scalars().all()
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exists")
    user_new = Users(username=user.username, password=user.password)
    session.add(user_new)
    await session.commit()
    await session.refresh(user_new)
    return user_new