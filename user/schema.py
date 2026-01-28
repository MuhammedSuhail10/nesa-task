from ninja import Schema
from typing import *

class LoginSchema(Schema):
    username: str
    password: str

class TokenOut(Schema):
    access: str
    refresh: str

class Message(Schema):
    message: str