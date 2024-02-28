# userSchema.py
from ariadne import gql

user_type_defs = gql("""
    type User {
      id: ID!
      username: String!
      email: String!
      books: [Book!]!

    }

    type Query {
      getUser(userId: ID!): User
      getAllUsers: [User!]
    }

    type Mutation {
      createUser(username: String!, email: String!,password: String!): User
    }
""")
