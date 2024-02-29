import jwt
from functools import wraps
from datetime import datetime, timedelta
from data import USERS
def authenticate_user(func):
    @wraps(func)
    def wrapper(_, info, *args, **kwargs):
        auth_header = info.context['request'].headers.get('Authorization', '').split(' ')[1]
        try:
            payload = jwt.decode(auth_header, '1234', algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = next((u for u in USERS if u["id"] == user_id), None)
            if user:
                return func(_, info, *args, **kwargs)
            else:
                raise PermissionError("No autenticado")
        except jwt.ExpiredSignatureError:
            raise PermissionError("Token expirado")
        except jwt.InvalidTokenError:
            raise PermissionError("Token inválido")

    return wrapper
