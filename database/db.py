import MySQLdb as mdb

def get_db_connection():
    """Создает соединение с базой данных."""
    try:
        conn = mdb.connect(
            host="localhost",
            user="root",
            password="root",
            database="tech_sub",
            autocommit = True
        )
        print('Connection ok')
        conn.close()

    except Exception as ex:
        print('Connection no')
        print(ex)


def test_fun():
    """ТЕСТОВАЯ ФУНКЦИЯ - ШАБЛОН"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(...)
    res = cursor.fetchall()
    return res


def select_tickets_user(id):
    """Ищет все заявки пользователя"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM tickets WHERE id_user = %s""", (id,))
    res = cursor.fetchall()
    return res