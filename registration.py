import sqlite3

db = sqlite3.connect('registration.db')
cur = db.cursor()

"""Создание таблицы"""

cur.execute("""CREATE TABLE IF NOT EXISTS users_data(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    Code INTEGER NOT NULL);
""")
db.commit()

# """Заполнение таблицы"""
#
# user_1 = ('Ivan', 'qwer1234', '1234')
# cur.execute("""INSERT INTO users_data(Login, Password, Code)
#     VALUES(?, ?, ?);
# """, user_1)
# db.commit()

"""Выбор действия"""

create_user = '1'  # Создать новый аккаунт
enter = '2'  # Авторизоваться
recover_password = '3'  # Восстановить пароль
action = input('Что нужно выполнить?\n1 - Создать новый аккаунт\n2 - Авторизоваться\n3 - Восстановить пароль\n')

"""Создаём нового пользователя"""
if action == create_user:

    login = input('Введите свой логин: ')

    cur.execute(f"""SELECT Login FROM users_data WHERE Login = '{login}';""")
    date_login = cur.fetchone()

    if date_login == None:
        password = input('Введите пароль от аккаунта: ')
        code = input('Введите восстанавливающий код: ')
        cur.execute(f"""INSERT INTO users_data(Login, Password, Code)
                    VALUES ('{login}', '{password}', {code});
                    """)
        db.commit()
        print('Новый пользователь создан!')
    else:
        print('Такой пользователь существует')

    """Авторизация существующего пользователя"""
elif action == enter:
    login = input('Введите свой логин: ')
    password = input('Введите пароль от аккаунта: ')
    user = login + ", " + password

    cur.execute("""SELECT * FROM users_data;""")
    users_data = cur.fetchone()
    data_login = users_data[1]
    data_password = users_data[2]
    authorization = data_login + ', ' + data_password

    if user == authorization:
        print('Авторизация прошла успешно!')
    else:
        print('Неверный логин или пароль. Осталось попыток: 3')
        login = input('Введите свой логин: ')
        password = input('Введите пароль от аккаунта: ')
        user = login + ", " + password

        cur.execute("""SELECT * FROM users_data;""")
        users_data = cur.fetchone()
        data_login = users_data[1]
        data_password = users_data[2]
        authorization = data_login + ', ' + data_password

        if user == authorization:
            print('Авторизация прошла успешно!')

        else:
            print('Неверный логин или пароль. Осталось попыток: 2')
            login = input('Введите свой логин: ')
            password = input('Введите пароль от аккаунта: ')
            user = login + ", " + password

            cur.execute("""SELECT * FROM users_data;""")
            users_data = cur.fetchone()
            data_login = users_data[1]
            data_password = users_data[2]
            authorization = data_login + ', ' + data_password

            if user == authorization:
                print('Авторизация прошла успешно!')

            else:
                print('Неверный логин или пароль. Осталось попыток: 1')
                login = input('Введите свой логин: ')
                password = input('Введите пароль от аккаунта: ')
                user = login + ", " + password

                cur.execute("""SELECT * FROM users_data;""")
                users_data = cur.fetchone()
                data_login = users_data[1]
                data_password = users_data[2]
                authorization = data_login + ', ' + data_password

                if user == authorization:
                    print('Авторизация прошла успешно!')

                else:
                    print('Восстановите пароль от аккаунта, используя код!')

    """Изменяем пароль через кодовое слово"""

elif action == recover_password:
    login = input('Введите свой логин: ')
    recover_code = input('Введите кодовое слово: ')
    log_user = login + ", " + recover_code

    cur.execute(f"""SELECT Login, Code FROM users_data WHERE Login = '{login}' AND Code = '{recover_code}';""")
    user_data = cur.fetchone()

    if user_data == None:
        print('Вы вели неверные данные! Повторите попытку')
    else:

        new_password = input('Введите новый пароль: ')

        cur.execute(f"""UPDATE users_data SET Password = '{new_password}' WHERE Code = '{recover_code}' ;""")
        db.commit()
        print('Новый пароль установлен!')

else:
    print('Неизвестная команда! Повторите попытку.')
