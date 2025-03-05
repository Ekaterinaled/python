from database_utils import connect_db, LOG_DB_CONFIG

def create_table_search_log_EF():
    """Создаёт таблицу search_logs_EF, если её нет."""
    connection = connect_db(LOG_DB_CONFIG)
    if connection is None:
        return

    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS search_logs_EF (
        id INT AUTO_INCREMENT PRIMARY KEY,
        genre VARCHAR(255),
        year INT,
        keyword VARCHAR(255),
        search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ Таблица search_logs_EF успешно создана (если её не было).")
    except Exception as e:
        print(f"❌ Ошибка при создании таблицы: {e}")
    finally:
        cursor.close()
        connection.close()

def log_search_query(genre, year, keyword):
    """Сохраняет параметры поиска в таблицу search_logs_EF."""
    connection = connect_db(LOG_DB_CONFIG)
    if connection is None:
        return

    cursor = connection.cursor()
    insert_query = """
    INSERT INTO search_logs_EF (genre, year, keyword, search_time)
    VALUES (%s, %s, %s, NOW());
    """

    try:
        cursor.execute(insert_query, (genre or None, year or None, keyword or None))
        connection.commit()
    except Exception as e:
        print(f"❌ Ошибка при сохранении запроса: {e}")
    finally:
        cursor.close()
        connection.close()

def get_popular_queries():
    """Выводит 10 самых популярных поисковых запросов."""
    print("🔍 Проверка: выполняется get_popular_queries()")  

    connection = connect_db(LOG_DB_CONFIG)
    if connection is None:
        return []

    cursor = connection.cursor()

    query = """
    SELECT 
        COALESCE(genre, 'Любой') AS genre,
        COALESCE(year, 'Любой') AS year,
        COALESCE(keyword, 'Любое') AS keyword,
        COUNT(*) AS count 
    FROM search_logs_EF 
    GROUP BY genre, year, keyword 
    ORDER BY count DESC 
    LIMIT 10;
    """

    print("📌 SQL-запрос для популярных запросов:")
    print(query)  

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        print("📊 Результаты запроса:")  
        for row in results:
            print(row)  # Вывод данных в терминал

        if not results:
            print("⚠️ Популярные запросы отсутствуют в базе.")  

        return results

    except Exception as e:
        print(f"❌ Ошибка при выполнении SQL-запроса: {e}")
        return []
    
    finally:
        cursor.close()
        connection.close()
