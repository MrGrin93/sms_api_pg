from sqlmodel import SQLModel, Field


"""Таблица для хранения смс"""
class SmsBase(SQLModel):
    number: str = Field()
    text: str
    ul: str = Field(foreign_key='ur_l.ul')
    date: str


class Sms(SmsBase, tablename="smss", table=True):
    id: int = Field(primary_key=True)

class SmsCreate(SQLModel):
    number: str
    text: str
    ul: str
    ul_number: str

"""Таблица соответствия номера телефона и юр. лица """

class Ur_l(SQLModel, tablename="ur_l", table=True):
    number: str
    ul: str = Field(primary_key=True)

"""Таблица пользователей"""

class Users(SQLModel,  tablename="users", table=True):
    id: int = Field(primary_key=True)
    username: str
    password: str
    disabled: bool = Field(default=False)

class UserCreate(SQLModel):
    username: str
    password: str

"""таблица токенов"""
class Token(SQLModel, tablename="tokens", table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key='users.id')
    token: str

class TokenCreate(SQLModel):
    token: str
    user_id: int
