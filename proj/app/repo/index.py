from fastapi import APIRouter, Depends, Request

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import os

from app.db.db import *
from app.models.models import *
from app.core.security import manager

current_path = os.path.dirname(os.path.abspath(__file__))

router = APIRouter()
templates = Jinja2Templates(directory=f"{current_path}/templates")



@router.get('/index', response_class=HTMLResponse)
async def get_webpage(request: Request,  session: AsyncSession = Depends(get_session), _=Depends(manager)):  
    result_ul = await session.execute(select(Ur_l))
    ur_ls = result_ul.scalars().all()
    ul_list = [
        {
            "number": u.number,
            "ul": u.ul
        }
        for u in ur_ls
    ]
    # sorted by date
    result_sms = await session.execute(select(Sms))
    smss = result_sms.scalars().all()
    # postss to dict
    smss_list = [
        {
            "id": sms.id,
            "number": sms.number,
            "text": sms.text,
            "ul": sms.ul,
            "date": sms.date,
        }
        for sms in smss
    ]
    newlist = sorted(smss_list,reverse=True, key=lambda d: d['id'] )
    return templates.TemplateResponse("index.html", {"request": request,"smsss": newlist, "title": "All", "ul_set": ul_list})

@router.get('/index/{ul}', response_class=HTMLResponse)
async def get_webpage(request: Request, ul: str, session: AsyncSession = Depends(get_session),_=Depends(manager)):  
    result_ul = await session.execute(select(Ur_l))
    ur_ls = result_ul.scalars().all()
    ul_list = [
        {
            "number": u.number,
            "ul": u.ul
        }
        for u in ur_ls
    ]
    # sorted by date
    result_sms = await session.execute(select(Sms).filter(Sms.ul == ul))
    smss = result_sms.scalars().all()
    # postss to dict
    smss_list = [
        {
            "id": sms.id,
            "number": sms.number,
            "text": sms.text,
            "ul": sms.ul,
            "date": sms.date,
        }
        for sms in smss
    ]
    newlist = sorted(smss_list,reverse=True, key=lambda d: d['id'] )
    return templates.TemplateResponse("index.html", {"request": request,"smsss": newlist, "title": ul, "ul_set": ul_list})

@router.get("/",response_class=HTMLResponse)
def loginwithCreds(request:Request):
    return templates.TemplateResponse("auth.html", {"request": request})