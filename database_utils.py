import mysql.connector
from mysql.connector import Error
from config import SAKILA_DB_CONFIG, LOG_DB_CONFIG

def connect_db(config):
    """Создаёт подключение к базе данных."""
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"❌ Ошибка подключения: {e}")
        return None
