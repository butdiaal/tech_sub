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
        print(res)
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


def get_user_role(user_id):
    """Получает роль пользователя"""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    res = cursor.fetchone()
    connection.close()
    return res[0] if res else None

def get_employee_id_by_user_id(user_id):
    """Получает id сотрудника по id пользователя"""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM employees WHERE id_user = %s", (user_id,))
    res = cursor.fetchone()
    connection.close()
    return res[0] if res else None

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


def create_user(login, password, ph_num):
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


def update_user(user_id, new_login, new_password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Проверяем существует ли пользователь
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return False

        # Обновляем данные
        cursor.execute(
            "UPDATE users SET login = %s, password = %s WHERE id = %s",
            (new_login, new_password, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating user: {e}")
        return False
    finally:
        if conn:
            conn.close()


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


def show_ticket_description__for_answer(id_ticket):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        f'''select t.id, c.name, t.description, t.status, t.creation_dt from tickets t join categories c on t.id_category = c.id;''')
    data = cur.fetchall()
    cur.close()
    return data


def get_types():
    db = get_db_connection()
    cur = db.cursor()
    cur.execute('SELECT name FROM categories ORDER BY name;')
    data = [item[0] for item in cur.fetchall()]
    cur.close()
    return data


def get_statuses():  # вывод списка статусов в скроллэриа гроупбокс
    db = get_db_connection()
    cur = db.cursor()
    cur.execute('select distinct(status) from tickets;')
    data = cur.fetchall()
    cur.close()
    return data


def get_active_tickets_except_done():
    db = get_db_connection()
    cur = db.cursor()
    cur.execute('''SELECT t.id, t.id_user, c.name, t.description, 
                  t.status, t.creation_dt, t.id_employee
                  FROM tickets t 
                  JOIN categories c ON t.id_category = c.id
                  WHERE t.status IN ('в ожидании', 'в работе')''')
    data = cur.fetchall()
    cur.close()
    return data

def get_active_tickets_except_done():
    """Возвращает все активные заявки кроме завершённых"""
    db = get_db_connection()
    cur = db.cursor()
    cur.execute('''SELECT 
                    t.id, t.id_user, c.name, t.description, 
                    t.status, t.creation_dt, t.id_employee
                   FROM tickets t 
                   JOIN categories c ON t.id_category = c.id 
                   WHERE t.status IN ('в ожидании', 'в работе')''')
    data = cur.fetchall()
    cur.close()
    return data


def show_ticket_description_for_answer(id_ticket): #описание тикета в окне ответа
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        f'''select t.id, c.name, t.description, t.status, t.creation_dt from tickets t join categories c on t.id_category = c.id where t.id = id_ticket;''')
    data = cur.fetchone()
    cur.close()
    return data


def take_ticket(ticket_id, employee_id):
    db = get_db_connection()
    cur = db.cursor()
    try:
        # Проверяем, что заявка существует и имеет статус 'в ожидании'
        cur.execute("SELECT id FROM tickets WHERE id = %s AND status = 'в ожидании'", (ticket_id,))
        if not cur.fetchone():
            return False

        # Обновляем заявку
        cur.execute("""
            UPDATE tickets 
            SET status = 'в работе', 
                id_employee = %s 
            WHERE id = %s
        """, (employee_id, ticket_id))

        db.commit()
        return cur.rowcount > 0  # Возвращает True если была обновлена хотя бы одна строка

    except Exception as e:
        print(f"Ошибка при взятии заявки: {e}")
        db.rollback()
        return False
    finally:
        cur.close()

def selected_status(status_name): #выбор по статусу (радиоботтон)
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        f''' SELECT t.id, t.id_user, c.name, t.description, 
                  t.status, t.creation_dt, t.id_employee
                  FROM tickets t 
                  JOIN categories c ON t.id_category = c.id
                  WHERE t.status = '{status_name}'
        ''')
    data = cur.fetchall()
    cur.close()
    return data

def selected_category(category_name): #выбор по категории (радиоботтон)# не используется
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        f''' SELECT t.id, t.id_user, c.name, t.description, 
                  t.status, t.creation_dt, t.id_employee
                  FROM tickets t 
                  JOIN categories c ON t.id_category = c.id
                  WHERE c.name = '{category_name}'
        ''')
    data = cur.fetchall()
    cur.close()
    return data

def get_answer(id_ticket, answer): #получает ответ и айди заявки и запускает процедуру (окно ответа - коннект рна кнопку)
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        f'''call get_answer_upd_status_ins_reports({id_ticket}, '{answer}');
''')
    cur.close()
    return


def get_tickets_by_status(status):
    """Получение заявок по указанному статусу"""
    db = get_db_connection()
    cur = db.cursor()
    try:
        cur.execute('''SELECT t.id, t.id_user, c.name, t.description, 
                      t.status, t.creation_dt, t.id_employee
                      FROM tickets t 
                      JOIN categories c ON t.id_category = c.id
                      WHERE t.status = %s''', (status,))
        return cur.fetchall()
    except Exception as e:
        print(f"Ошибка при получении заявок по статусу: {e}")
        return []
    finally:
        cur.close()

def show_ticket_description(ticket_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT description FROM tickets WHERE id = %s",
            (ticket_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else "Описание не найдено"
    except Exception as e:
        print(f"Ошибка при получении описания: {e}")
        return "Ошибка загрузки описания"
    finally:
        if connection:
            connection.close()

def get_all_from_reports():
    try:
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute(
            f"select * from reports;"
        )
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Ошибка при получении решенных заявок: {e}")
        return "Ошибка загрузки решенных заявок"
    finally:
        if con:
            con.close()