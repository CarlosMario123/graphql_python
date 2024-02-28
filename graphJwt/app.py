from ariadne import QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
import jwt
from datetime import datetime, timedelta

USERS = []

type_defs = """
    type User {
        id: Int!
        username: String!
        password: String!
    }

    type Mutation {
        registerUser(username: String!, password: String!): User
        login(username: String!, password: String!): TokenResponse
    }

    type Query {
        users: [User]
    }

    type TokenResponse {
        token: String
        error: String
    }
"""

query = QueryType()
mutation = MutationType()

@query.field("users")
def resolve_users(_, info):
    # Verifica la autenticación utilizando el token en el contexto
    user = authenticate_user(info)
    if user:
        return USERS
    else:
        raise PermissionError("No autenticado")

@mutation.field("registerUser")
def resolve_register_user(_, info, username, password):
    user_id = len(USERS) + 1
    new_user = {"id": user_id, "username": username, "password": password}
    USERS.append(new_user)
    return new_user

@mutation.field("login")
def resolve_login(_, info, username, password):
    user = next((user for user in USERS if user["username"] == username and user["password"] == password), None)
    if user:
        # Genera un token JWT al hacer login
        token = create_jwt_token(user["id"])
        return {'token': token}
    else:
        return {'error': 'Credenciales incorrectas'}

def create_jwt_token(user_id: int) -> str:
    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    token = jwt.encode(payload, '1234', algorithm='HS256')
    return token

def authenticate_user(info):
    auth_header = info.context['request'].headers.get('Authorization', '').split(' ')[1]
    
    print("valor")
    print(auth_header)
  
    try:
        payload = jwt.decode(auth_header, '1234', algorithms=['HS256'])
        user_id = payload.get('user_id')
        return next((user for user in USERS if user["id"] == user_id), None)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    return None

schema = make_executable_schema(type_defs, query, mutation)

app = GraphQL(schema)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
