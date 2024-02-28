
from uuid import uuid4#permite la generacion de id para graphql

# Lista global simulada de libros
global_books = [
    {"id": str(uuid4()), "title": "Libro 1", "author": "Autor 1"},
    {"id": str(uuid4()), "title": "Libro 2", "author": "Autor 2"},
]
