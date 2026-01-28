from ninja.security import HttpBearer
import jwt
from django.conf import settings
from user.models import User

class UserAuth(HttpBearer):
    async def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(payload)
            user_id = payload.get('user_id')
            if user_id and await User.objects.filter(id=user_id).aexists():
                print('payload')
                user = await User.objects.aget(id=user_id)
                return user
            return None
        except Exception as e:
            return None