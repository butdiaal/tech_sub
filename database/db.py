import MySQLdb as mdb


def get_db_connection():
    """Создает соединение с базой данных."""
    try:
        conn = mdb.connect(
            host="localhost",
            user="root",
            password="root",
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
            VALUES (%s, %s, %s, 'в ожидании', now())""", (id_user, id_categ, desc,))
        rows_add = cursor.rowcount
        conn.commit()
        return rows_add > 0
    except Exception as e:
        print(f"Ошибка при добавлении заявки: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def select_for_watch(id_ticket):
    """Ищет все про заявку"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM tickets WHERE id = %s", (id_ticket,))
    status_result = cursor.fetchone()
    if not status_result:
        return None
    status = status_result[0]

    if status == "в ожидании" or "в работе":
        cursor.execute("""SELECT cat.name, tks.description, tks.status, tks.creation_dt, 
            CONCAT('отсуствует') as finish_dt, CONCAT('отсуствует') as answer
            FROM tickets AS tks 
            JOIN categories AS cat ON cat.id = tks.id_category
            WHERE tks.id = %s""", (id_ticket,))
        res = cursor.fetchall()
        return res
    elif status == "решена":
        cursor.execute("""SELECT reports.category, reports.description, tickets.status, 
            reports.start_dt, reports.finish_dt, reports.answer
            FROM reports
            JOIN tickets ON tickets.id = reports.id_ticket
            WHERE id_ticket = %s""", (id_ticket,))
        res = cursor.fetchall()
        return res


def select_ticket(id_ticket):
    """Ищет заявку по id"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Проверяем статус заявки
        cursor.execute("SELECT status FROM tickets WHERE id = %s", (id_ticket,))
        status_result = cursor.fetchone()
        if not status_result:
            return None
        status = status_result[0]

        if status == "в ожидании":
            cursor.execute("""
                SELECT categories.name, tickets.description 
                FROM tickets
                JOIN categories ON categories.id = tickets.id_category
                WHERE tickets.id = %s
            """, (id_ticket,))
            return cursor.fetchone()
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении заявки: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def update_ticket(id_ticket, id_categ, desc):
    """Изменяет заявку"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE tickets SET id_category = %s, description = %s 
                WHERE id = %s""", (id_categ, desc, id_ticket,))
        rows_add = cursor.rowcount
        conn.commit()
        return rows_add > 0
    except Exception as e:
        print(f"Ошибка при изменении заявки: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def select_status(id_ticket):
    """Ищет статус заявки"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT status FROM tickets WHERE id = %s""", (id_ticket,))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else None


def get_user_id(login):
    """Получает id пользователя"""
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_get_user_id = f"SELECT id FROM users WHERE login='{login}'"
    cursor.execute(sql_statement_get_user_id)
    res = cursor.fetchone()
    connection.close()
    if res is not None:
        return res[0]
    else:
        return None


def get_employees_id(login):
    """Получает id пользователя"""
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_get_user_id = f"SELECT id FROM employees WHERE login='{login}'"
    cursor.execute(sql_statement_get_user_id)
    res = cursor.fetchone()
    connection.close()
    if res is not None:
        return res[0]
    else:
        return None


def get_user(login, password):
    """Получаем логин и пароль"""
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_get_user_id = f"SELECT * FROM users WHERE login='{login}' AND password=MD5('{password}')"
    cursor.execute(sql_statement_get_user_id)
    user = cursor.fetchone()
    connection.close()
    return user


def get_employee(login, password):
    """Получаем логин и пароль"""
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_get_user_id = f"SELECT * FROM employees WHERE login='{login}' AND password=MD5('{password}')"
    cursor.execute(sql_statement_get_user_id)
    user = cursor.fetchone()
    connection.close()
    return user


def create_user(login, password, ph_num) :

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE login = %s", (login,))
        if cursor.fetchone():
            print("Ошибка: пользователь уже существует")
            return False

        cursor.execute(
            f"INSERT INTO users (login, password, ph_num) VALUES ('{login}', md5('{password}'), '{ph_num}')",

        )

        connection.commit()
        return True


def create_user_admin(login, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM users WHERE login = '{login}'")
    if cursor.fetchone():
        print("Ошибка: пользователь уже существует")
        return False

    cursor.execute(
        f"INSERT INTO users (login, password) VALUES ('{login}', md5('{password}'));"
    )

    connection.commit()
    return True


def get_all_users():
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_get_all_users = "SELECT id,login, password FROM users"
    cursor.execute(sql_statement_get_all_users)
    users = cursor.fetchall()
    connection.close()
    return users


def get_all_employees():
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_get_all_users = "SELECT id,login, password, is_admin FROM employees"
    cursor.execute(sql_statement_get_all_users)
    users = cursor.fetchall()
    connection.close()
    return users


def delete_user(login):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_delete_user = f"DELETE FROM users WHERE login = '{login}'"
    cursor.execute(sql_statement_delete_user)
    connection.commit()
    connection.close()


def reset_password(login, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql_statement_reset_password = f"UPDATE users SET password='{password}' WHERE login='{login}'"
    cursor.execute(sql_statement_reset_password)
    connection.commit()
    connection.close()


def update_user(user_id, login, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        sql = "UPDATE users SET login = %s, password = %s WHERE user_id = %s"
        cursor.execute(sql, (login, password,  user_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error updating user: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()


def update_employee(emp_id, login, password, is_admin):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        sql = "UPDATE employees SET login = %s, password = %s, is_admin = %s WHERE id = %s"
        cursor.execute(sql, (login, password, is_admin, emp_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error updating employee: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()


def get_types(): #вывод списка категорий (типов) в скроллэриа гроупбокс
    db = get_db_connection()
    cur = db.cursor()
    cur.execute('select concat(name,", приоритет - ", level) from categories;')
    data = cur.fetchall()
    cur.close()
    return data

def get_statuses(): #вывод списка статусов в скроллэриа гроупбокс
    db = get_db_connection()
    cur = db.cursor()
    cur.execute('select distinct(status) from tickets;')
    data = cur.fetchall()
    cur.close()
    return data

#commitnula