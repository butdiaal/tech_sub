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


def get_user_id(username):
    """Получает id пользователя"""
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_get_user_id = f"SELECT user_id FROM users WHERE username='{username}'"
    cursor.execute(sql_statement_get_user_id)
    res = cursor.fetchone()
    connection.close()
    if res is not None:
        return res[0]
    else:
        return None


def get_user(username, password):
    """Получаем логин и пароль"""
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_get_user_id = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(sql_statement_get_user_id)
    user = cursor.fetchone()
    connection.close()
    return user


def create_user(username, password, role):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_test_user = (
        "INSERT OR IGNORE INTO users "
        "(username, password, role) "
        f"VALUES ('{username}', '{password}', '{role}')"
    )
    cursor.execute(sql_statement_test_user)
    connection.commit()
    connection.close()