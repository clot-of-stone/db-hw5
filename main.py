import psycopg2

# Открываем соединение
conn = psycopg2.connect(database="homework5", user="postgres", password="")


def create_table():
    with conn.cursor() as cur:
        cur.execute(""" 
                create table if not exists client_info(
                    id_client serial primary key,
                    client_name VARCHAR(60) not null,
                    client_last_name VARCHAR(60) not null,
                    client_email VARCHAR(40) UNIQUE
                );
                create table if not exists phone_number(
                    id_phone_number serial primary key ,
                    id_client INTEGER NOT NULL REFERENCES client_info(id_client),
                    client_number_phone VARCHAR(20) UNIQUE
                );
            """)

        conn.commit()

    conn.close()


def add_client(client_name, client_last_name, email, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
            insert into client_info(client_name, client_last_name, client_email) values(%s, %s, %s) RETURNING id_client;
        """, (client_name, client_last_name, email))

        conn.commit()

        cur.execute("""
            insert into phone_number(client_number_phone, id_client) values(%s, %s)
        """, (phone_number, cur.fetchone()))

        conn.commit()


def add_phone_number(phone_number, id_client):
    with conn.cursor() as cur:
        cur.execute("""
                    insert into phone_number(client_number_phone, id_client) values(%s, %s)
                """, (phone_number, id_client))

        conn.commit()


def change_data_client(id_client, client_name="", lastname="", email=""):
    with conn.cursor() as cur:
        if client_name:
            cur.execute("""
                            UPDATE client_info SET client_name=%s WHERE id_client=%s;
                        """, (client_name, id_client))
        if lastname:
            cur.execute("""
                            UPDATE client_info SET client_last_name=%s WHERE id_client=%s;
                        """, (lastname, id_client))
        if email:
            cur.execute("""
                            UPDATE client_info SET client_email=%s WHERE id_client=%s;
                        """, (email, id_client))

        is_change_number = input("Если хотите изменить номер пишите - y, если нет - q: ")

        if is_change_number == "y":
            change_phone_number(id_client)

        conn.commit()


def change_phone_number(id_client):
    with conn.cursor() as cur:
        cur.execute("""
                        select client_number_phone, id_phone_number from phone_number
                        where id_client = %s
                    """, id_client)
        print("Список номеров для изменения, выберите какой хотите изменить:")

        list_number = cur.fetchall()

        [print(f'{i + 1}.{el[0]}') for i, el in enumerate(list_number)]
        chenge_number = input("Введите цифру номера который хотите изменить: ")
        id_phone_number = list_number[int(chenge_number)][1]
        new_number = input("Введите новый номер: ")

        cur.execute("""
                        UPDATE phone_number SET client_number_phone=%s WHERE id_phone_number=%s;
                    """, (new_number, id_phone_number))


def delete_client_phone_numper(id_client):
    with conn.cursor() as cur:
        cur.execute("""
                        select client_number_phone, id_phone_number from phone_number
                        where id_client = %s
                    """, (id_client))
        print("Список номеров для удаления:")
        list_number = cur.fetchall()
        [print(f'{i + 1}.{el[0]}') for i, el in enumerate(list_number)]
        delete_number = input("Введите цифру номера который хотите удалить: ")
        id_phone_number = list_number[int(delete_number) - 1][1]
        cur.execute("""
                        DELETE FROM phone_number WHERE id_client=%s and id_phone_number=%s
                    """, (id_client, id_phone_number))
        conn.commit()


def delete_client(id_client):
    with conn.cursor() as cur:
        cur.execute("""
                        DELETE FROM phone_number WHERE id_client=%s
                    """, id_client)
        cur.execute("""
                        DELETE FROM client_info WHERE id_client=%s
                    """, id_client)
        conn.commit()


def find_client():
    print("Искать по: \n"
          "Имени - введите 1 \n"
          "Фамилии - введите 2 \n"
          "По почте - введите 3 \n"
          "Номеру телефона- введите 4 \n"

          )
    search_params = input("Введите номер поиска по параметру: ")
    if search_params == '1':
        search_info = input("Введите имя: ")
        with conn.cursor() as cur:
            cur.execute("""
                            select client_name, client_last_name, client_email, client_number_phone from client_info ci
                            left join phone_number pn on pn.id_client = ci.id_client
                            where client_name = %s
                        """, (search_info,))
            print(cur.fetchall())
    if search_params == '2':
        search_info = input("Введите фамилию: ")
        with conn.cursor() as cur:
            cur.execute("""
                            select client_name, client_last_name, client_email, client_number_phone from client_info ci
                            left join phone_number pn on pn.id_client = ci.id_client
                            where client_last_name = %s
                        """, (search_info,))
            print(cur.fetchall())
    if search_params == '3':
        search_info = input("Введите почту: ")
        with conn.cursor() as cur:
            cur.execute("""
                            select client_name, client_last_name, client_email, client_number_phone from client_info ci
                            left join phone_number pn on pn.id_client = ci.id_client
                            where client_email = %s
                        """, (search_info,))
            print(cur.fetchall())
    if search_params == '4':
        search_info = input("Введите номер телефона: ")
        with conn.cursor() as cur:
            cur.execute("""
                            select client_name, client_last_name, client_email, client_number_phone from client_info ci
                            left join phone_number pn on pn.id_client = ci.id_client
                            where client_number_phone=%s
                        """, (search_info,))
            print(cur.fetchall())


# создаем таблицы
# create_table()
# создаем клиента 1
# add_client("Clent_1", "Last_name_clent_1", "clent_1@gmail", "1-111-111-11-11")
# создаем клиента 2
# add_client("Clent_1", "Last_name_clent_2", "clent_2@gmail", "2-222-222-22-22")

# Изменяем клиента
# change_data_client("1", "Vasiliy", "Andronov")

# Добавить номер телефона клиента
# add_phone_number("1", "8-800-200-600")

# Удалить номер телефона
# delete_client_phone_numper("1")

# удаление клиента
# delete_client("1")

# поиск клиента
# find_client()

# Закрываем соединение
conn.close()