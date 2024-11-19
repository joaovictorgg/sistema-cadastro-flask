import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host = '127.0.0.1',
            database= 'db_py',
            user='root',
            password=''
        )
        if connection.is_connected():
            print("Conexão bem sucedida ")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e} ")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Conexão finalizada com o banco de dados")