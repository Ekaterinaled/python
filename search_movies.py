from log_queries import log_search_query
from mysql.connector import Error
from database_utils import connect_db, SAKILA_DB_CONFIG
from prettytable import PrettyTable

def search_movies(genre=None, year=None, keyword=None):
    """Ищет фильмы в базе данных по жанру, году и ключевому слову и логирует запрос в SQL.""" 
    conditions = []
    params = []

    if genre:
        conditions.append("c.name = %s")
        params.append(genre)
    if year:
        conditions.append("f.release_year = %s")
        params.append(year)
    if keyword:
        conditions.append("LOWER(f.title) LIKE LOWER(%s)")
        params.append(f"%{keyword}%")

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT f.title, f.release_year, c.name AS category, f.rating, f.length, f.description
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE {where_clause}
        ORDER BY f.title
        LIMIT 5;
    """

    connection = connect_db(SAKILA_DB_CONFIG)
    if connection is None:
        return []

    cursor = connection.cursor()

    try:
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        print("🔎 Результаты поиска:", results)

        if not results:
            print("⚠️ Фильмы не найдены.")
            return []

       
        log_search_query(genre, year, keyword)  

    
        table = PrettyTable(["Название", "Год", "Категория", "Рейтинг", "Длительность", "Описание"])
        for row in results:
            table.add_row(row)

        print(table)

        return results
    except Error as e:
        print(f"❌ Ошибка выполнения запроса: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


