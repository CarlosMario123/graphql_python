# main.py
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from schema import user_type_defs , book_type_defs
import uvicorn
from resolvers import allResolver


type_defs = user_type_defs + book_type_defs


schema = make_executable_schema(type_defs,allResolver)
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
