import mysql.connector
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv()
        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")

        self.db_config = {
            "host": self.db_host,
            "user": self.db_user,
            "password": self.db_password,
            "database": self.db_name,
        }

        self.create_tables()

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def create_tables(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        user_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255)
        )
        """

        book_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            id VARCHAR(36) PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255)
        )
        """

        cursor.execute(user_table_query)
        cursor.execute(book_table_query)

        connection.commit()
        cursor.close()
        connection.close()
