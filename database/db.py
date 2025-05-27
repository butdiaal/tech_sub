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
    try:
        cursor.execute("""DELETE FROM tickets WHERE id = %s AND id_user = %s 
            AND status = 'в ожидании'""", (id_ticket, id_user))
        rows_deleted = cursor.rowcount
        conn.commit()
        return rows_deleted > 0
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при удалении заявки: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def select_categories():
    """Ищет все категории"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM categories """, ())
    res = cursor.fetchall()
    return res


def add_new_ticket(id_user, id_categ, desc):
    """Добавляет новую заявку"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO tickets (id_user, id_category, description, status, creation_dt) 
            VALUES (%s, %s, %s, 'в ожидании', now())""", (id_user, id_categ, desc, ))
        rows_add = cursor.rowcount
        conn.commit()
        return rows_add > 0
    except Exception as e:
        print(f"Ошибка при добавлении заявки: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
