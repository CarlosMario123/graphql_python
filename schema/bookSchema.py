# book_schema.py
from ariadne import gql

book_type_defs = gql("""
    type Book {
      id: ID!
      title: String!
      author: String!
    }

    extend type Query {
      getBook(bookId: ID!): Book
      getAllBooks: [Book!]!
    }

    extend type Mutation {
      createBook(title: String!, author: String!): Book
    }
""")
