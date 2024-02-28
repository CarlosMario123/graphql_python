from ariadne import QueryType, MutationType
from uuid import uuid4
from db.db import Database
import bcrypt

user_query = QueryType()
user_mutation = MutationType()

db = Database()  # Creamos una instancia de la clase Database

@user_query.field("getUser")
def resolve_get_user(*_, userId):
    try:
        with db.get_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (userId,))
            result = cursor.fetchone()
            return {"id": result[0], "username": result[1], "email": result[2], "books": []} if result else None
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return None

@user_query.field("getAllUsers")
def resolve_get_all_users(*_):
    try:
        with db.get_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            return [{"id": row[0], "username": row[1], "email": row[2], "books": []} for row in results]
    except Exception as e:
        print(f"Error al obtener todos los usuarios: {e}")
        return None

@user_mutation.field("createUser")
def resolve_create_user(*_, username, email, password):
    try:
        with db.get_connection() as connection, connection.cursor() as cursor:
            new_user_id = str(uuid4())
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO users (id, username, email, password) VALUES (%s, %s, %s, %s)",
                           (new_user_id, username, email, hashed_password))
            connection.commit()
            return {"id": new_user_id, "username": username, "email": email, "books": []}
    except Exception as e:
        print(f"Error al crear un usuario: {e}")
        return None

# Crear un objeto de resolvers para los usuarios
user_resolvers = [user_query, user_mutation]
