from typing import List, Tuple
from mysql.connector import connect, Error
from os import environ


def update_user(id: int, username: str) -> bool:
    """
    Создает пользователя с id и никнеймом

    Args:
        id: int - id пользователя
        username: str - никнейм пользователя
    Returns:
        bool: True, если пользователь успешно создан, False - в противном случае
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            with connection.cursor() as cursor:
                # Проверяем, если пользователь уже зарегистрирован
                check_query = "SELECT username FROM users WHERE id = %s"
                cursor.execute(check_query, (id,))
                result = cursor.fetchone()

                if result:
                    # Пользователь уже зарегистрирован, проверяем никнейм
                    current_username = result[0]
                    if current_username != username:
                        # Обновляем никнейм если он изменился
                        update_query = "UPDATE users SET username = %s WHERE id = %s"
                        cursor.execute(update_query, (username, id))
                        connection.commit()
                    return True
                else:
                    # Пользователь не зарегистрирован, регистрируем
                    insert_query = "INSERT INTO users (id, username) VALUES (%s, %s)"
                    cursor.execute(insert_query, (id, username))
                    connection.commit()
                    return True
    except Error as e:
        print(e)
        print(
            "Не получилось создать пользователя с id =", id, "и никнеймом =", username
        )
        return False


def get_all_ids() -> List[int]:
    """
    Возвращает список id всех пользователей
    или пустый список в случае ошибки

    Returns:
        List[int]: - список id всех пользователей
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                SELECT id FROM users;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Error as e:
        print(e)
        print("Не получилось получить список пользователей")
        return []


def is_user_registered(id: int) -> bool:
    """
    Проверяет, зарегистрирован ли пользователь

    Args:
        id: int - id пользователя
    Returns:
        bool: True, если пользователь зарегистрирован, False - в противном случае
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                SELECT id FROM users WHERE id = %s;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                return cursor.fetchone() is not None
    except Error as e:
        print(e)
        print("Не получилось проверить наличие пользователя с id =", id)
        return False


def add_confirm(text: str) -> int:
    """
    Добавляет рассылку с подтверждением

    Args:
        text: str - текст рассылки

    Returns:
        int: id добавленной рассылки или 0 в случае ошибки
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                INSERT INTO confirms (text) VALUES (%s);
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (text[:125] + "...",))
                connection.commit()
                return cursor.lastrowid
    except Error as e:
        print(e)
        print("Не получилось добавить рассылку с подтверждением")
        return 0


def get_all_confirms() -> List[int]:
    """
    Возвращает все рассылки

    Returns:
        List[str]: все рассылки
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                SELECT id, text FROM confirms;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Error as e:
        print(e)
        print("Не получилось получить рассылки с подтверждением")
        return []


def add_confirm_user_mailing(user_id, mailing_id):
    """
    Добавляет подтверждение рассылки пользователю

    Args:
        user_id: int - id пользователя
        mailing_id: int - id рассылки
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                INSERT INTO users_confirms (user_id, confirm_id) VALUES (%s, %s);
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (user_id, mailing_id))
                connection.commit()
    except Error as e:
        print(e)
        print("Не получилось добавить подтверждение рассылки пользователю")


def end_confirm(id: int) -> bool:
    """
    Завершает рассылку с подтверждением

    Args:
        id: int - id рассылки
    Returns:
        bool: True, если рассылка завершена, False - в противном случае
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            query: str = (
                """
                DELETE FROM confirms WHERE id = %s;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                connection.commit()
                return True
    except Error as e:
        print(e)
        print("Не получилось завершить рассылку с подтверждением")
        return False


def get_confirm(id: int) -> Tuple[str, List[Tuple[int, str]]]:
    """
    Возвращает информацию о подтвержденных пользователях и текст рассылки

    Args:
        id: int - id рассылки
    Returns:
        Tuple[str,List[Tuple[int,str]]]: текст + тг id и username каждого пользователя, подтвердившего id конкурса
    """
    try:
        with connect(
            host=environ["DB_HOST"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
        ) as connection:
            text_query: str = (
                """
                SELECT text FROM confirms WHERE id = %s;
                """
            )
            users_query: str = (
                """
                SELECT 
                 user.id,
                 user.username
                FROM 
                 users_confirms AS confirmation 
                JOIN 
                 users AS user ON user.id = confirmation.user_id
                WHERE 
                 confirmation.confirm_id = %s;
                """
            )
            with connection.cursor() as cursor:
                cursor.execute(text_query, (id,))
                text = cursor.fetchone()[0]
                cursor.execute(users_query, (id,))
                users = cursor.fetchall()
                return text, [(user[0], user[1]) for user in users]
    except Error as e:
        print(e)
        print("Не получилось получить подтвержденных пользователей")
        return []
