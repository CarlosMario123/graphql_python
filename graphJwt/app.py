from functools import wraps
from ariadne import QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
import jwt
from datetime import datetime, timedelta
from authJwt import authenticate_user
from data import USERS,PRODUCTS

type_defs = """
    type User {
        id: Int!
        username: String!
        password: String!
    }

    type Product {
        id: Int!
        name: String!
        price: Float!
    }

    type Mutation {
        registerUser(username: String!, password: String!): User
        login(username: String!, password: String!): TokenResponse
        addProduct(name: String!, price: Float!): Product
    }

    type Query {
        users: [User]
        products: [Product]
    }

    type TokenResponse {
        token: String
        error: String
    }
"""

query = QueryType()
mutation = MutationType()


@query.field("users")
@authenticate_user
def resolve_users(_, info):
    return USERS

@query.field("products")
@authenticate_user
def resolve_products(_, info):
    return PRODUCTS

@mutation.field("registerUser")
def resolve_register_user(_, info, username, password):
    user_id = len(USERS) + 1
    new_user = {"id": user_id, "username": username, "password": password}
    USERS.append(new_user)
    return new_user

@mutation.field("login")
def resolve_login(_, info, username, password):
    user = next((u for u in USERS if u["username"] == username and u["password"] == password), None)
    if user:
        token = create_jwt_token(user["id"])
        return {'token': token}
    else:
        return {'error': 'Credenciales incorrectas'}

@mutation.field("addProduct")
@authenticate_user
def resolve_add_product(_, info, name, price):
    product_id = len(PRODUCTS) + 1
    new_product = {"id": product_id, "name": name, "price": price}
    PRODUCTS.append(new_product)
    return new_product

def create_jwt_token(user_id: int) -> str:
    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    token = jwt.encode(payload, '1234', algorithm='HS256')
    return token

schema = make_executable_schema(type_defs, query, mutation)

app = GraphQL(schema)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
