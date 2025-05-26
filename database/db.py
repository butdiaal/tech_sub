import MySQLdb as mdb

def get_db_connection():
    """Создает соединение с базой данных."""
    try:
        conn = mdb.connect(
            host="localhost",
            user="root",
            password="",
            database="tech_sub",
            autocommit=True
        )
        print('Connection ok')
        return conn

    except Exception as ex:
        print('Connection failed')
        print(ex)
        return None


def test_fun():
    """ТЕСТОВАЯ ФУНКЦИЯ - ШАБЛОН"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(...)
    res = cursor.fetchall()
    return res


def select_tickets_user(id_user):
    """Ищет все заявки пользователя"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM tickets WHERE id_user = %s""", (id_user,))
    res = cursor.fetchall()
    return res

def delete_ticket(id_ticket, id_user):
    """Удаляет выбранную заявку, где статус = в ожидании"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM tickets WHERE id = %s 
        AND id_user = %s AND status = 'в ожидании'""", (id_ticket, id_user))
    res = cursor.fetchone()
    return res