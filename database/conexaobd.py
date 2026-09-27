import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def iniciar_banco():
    """Cria e retorna uma conexão com o banco de dados."""

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )