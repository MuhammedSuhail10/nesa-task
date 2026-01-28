import random
from ninja import Router, PatchDict
from django.contrib.auth import authenticate
from .schema import *
from django.contrib.auth.models import User
from ninja_jwt.tokens import RefreshToken, AccessToken

user_api = Router(tags=["User"])

@user_api.post('login', auth=None, response={200: TokenOut, 404: Message})
def login(request, data: LoginSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is None:
        return 404, {"message": "User doesnot exist"}
    refresh = str(RefreshToken.for_user(user))
    access = str(AccessToken.for_user(user))
    return 200, {"access": access, "refresh": refresh}