import psycopg2

conn = psycopg2.connect(database="customerDB", user="postgres", password="postgres")
# with conn.cursor() as cur:
cur = conn.cursor()


def del_table():

    cur.execute("""
        DROP TABLE phones;
        DROP TABLE emails;
        DROP TABLE clients;
    """)


def create_db():

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            first_name varchar(50) NOT NULL,
            last_name varchar(50) NOT NULL
          );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id),
            phone_number VARCHAR(15) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS emails(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id),
            email VARCHAR(60) NOT NULL
        );
    """)

    conn.commit()


def add_client(first_name, last_name):
    cur.execute('''
        INSERT INTO clients (first_name, last_name) 
        VALUES (%s, %s)
    ''', (first_name, last_name))

    conn.commit()


def add_phone(client_id, phone_number):
    cur.execute('''
        INSERT INTO phones (client_id, phone_number) 
        VALUES (%s, %s)
    ''', (client_id, phone_number))

    conn.commit()


def add_email(client_id, email):
    cur.execute('''
        INSERT INTO emails (client_id, email) 
        VALUES (%s, %s)
    ''', (client_id, email))

    conn.commit()


def change_client(id, first_name=None, last_name=None, email=None, phone_number=None):
    if first_name:
        cur.execute('''UPDATE clients SET first_name=%s WHERE id=%s;''', (first_name, id))
    elif last_name:
        cur.execute('''UPDATE clients SET last_name=%s WHERE id=%s;''', (last_name, id))
    elif email:
        cur.execute('''UPDATE emails SET email=%s WHERE id=%s;''', (email, id))
    elif phone_number:
        cur.execute('''UPDATE phones SET phone_number=%s WHERE id=%s;''', (phone_number, id))
    conn.commit()


def delete_phones(phones_id):
    cur.execute('''
        DELETE FROM phones
        WHERE id IN %s
    ''', (phones_id,))

    conn.commit()


def delete_emails(emails_id):
    cur.execute('''
        DELETE FROM emails
        WHERE id IN %s
    ''', (emails_id,))

    conn.commit()


def delete_client(client_id):
    cur.execute('''
        DELETE FROM phones
        WHERE client_id = %s
    ''', (client_id,))
    cur.execute('''
        DELETE FROM emails
        WHERE client_id = %s
    ''', (client_id,))
    cur.execute('''
        DELETE FROM clients
        WHERE id = %s
    ''', (client_id,))

    conn.commit()


def find_client(search):
    cur.execute('''
        SELECT * FROM clients
        WHERE first_name = %s OR last_name = %s OR id IN (
        SELECT client_id
        FROM phones WHERE phone_number = %s
        )
    ''', (search, search, search))
    result = cur.fetchall()
    print(result)


if __name__ == '__main__':
    del_table()
    print('Летопись удалена')
    create_db()
    print('Летопись создана')
    add_client('Alyosha', 'Popovich')
    add_client('Dobrynya', 'Nikitich')
    add_client('Ilya', 'Muromets')
    print('Богатырь добавлен')
    add_phone(1, '+79190000000')
    add_phone(1, '+79220000000')
    add_phone(1, '+79090000000')
    add_phone(2, '+73420000000')
    print('Номер телефона добавлен')
    add_email(2, 'Nikitich@ya.ru')
    add_email(3, 'Muromets@bk.ru')
    print('E-mail добавлен')
    change_client(1, first_name='Aleksey')
    print('Запись в летописе обновлена')
    delete_client(2, )
    print('Богатырь удален')
    delete_phones((4,))
    print('Номер телефона удален')
    delete_emails((2, ))
    print('E-mail удален')
    find_client(search='Muromets')

    conn.close()
