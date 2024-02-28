from ariadne import QueryType, MutationType
from uuid import uuid4
from db.db import Database

book_query = QueryType()
book_mutation = MutationType()
db = Database() 

@book_query.field("getBook")
def resolve_get_book(*_, bookId):
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books WHERE id = %s", (bookId,))
        result = cursor.fetchone()
        return {"id": result[0], "title": result[1], "author": result[2]} if result else None
    except Exception as e:
        print(f"Error al obtener libro: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
            connection.close()

@book_query.field("getAllBooks")
def resolve_get_all_books(*_):
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()
        return [{"id": row[0], "title": row[1], "author": row[2]} for row in results]
    except Exception as e:
        print(f"Error al obtener todos los libros: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
            connection.close()

@book_mutation.field("createBook")
def resolve_create_book(*_, title, author):
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        new_book_id = str(uuid4())
        cursor.execute("INSERT INTO books (id, title, author) VALUES (%s, %s, %s)", (new_book_id, title, author))
        connection.commit()
        return {"id": new_book_id, "title": title, "author": author}
    except Exception as e:
        print(f"Error al crear un libro: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
            connection.close()

# Crear un objeto de resolvers para los libros
book_resolvers = [book_query, book_mutation]
