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
try:   # При отмене действия будет выводиться соответствующее сообщение

    """"Выбор действия"""

    create_user = '1'  # Создать новый аккаунт
    enter = '2'  # Авторизоваться
    recover_password = '3'  # Восстановить пароль
    action = input('Выберите цифру какую операцию выполнить?\n1 - Создать новый аккаунт\n2 - Авторизоваться\n3 - '
                   'Восстановить пароль\n')

    if len(action) == 0 or action >= str(4) or action == str(0):
        print('Неизвестная команда')

    """Создаём нового пользователя"""

    while True:                                                     # Цикл, который помогает нам сделать так, что бы не было пустых строк.
        if action == create_user:

            login = input('Введите свой логин: ')
            if len(login) == 0:                                     # Конструкция, которая прекращает действие, если пользователь оставил пустую строку.
                print('Ошибка! Повторите попытку.')
                break
            else:
                cur.execute(f"""SELECT Login FROM users_data WHERE Login = '{login}';""")
                date_login = cur.fetchone()

                if date_login is None:

                    password = input('Введите пароль от аккаунта: ')
                    if len(password) == 0:
                        print('Ошибка! Повторите попытку.')
                        break
                    else:
                        code = input('Введите восстанавливающий код: ')
                        if len(code) == 0:
                            print('Ошибка! Повторите попытку.')
                            break
                        else:
                            cur.execute(f"""INSERT INTO users_data(Login, Password, Code)
                                        VALUES ('{login}', '{password}', {code});
                                        """)
                            db.commit()
                            print('\nНовый пользователь создан!')
                else:
                    print('\nТакой пользователь существует')
        break

    """Авторизация существующего пользователя"""

    while True:
        if action == enter:
            login = input('Введите свой логин: ')
            if len(login) == 0:
                print('Ошибка! Cтрочка не должна быть пустой.')
                break
            else:

                cur.execute(f"""SELECT Login FROM users_data WHERE Login = '{login}';""")
                users_login = cur.fetchone()

                if users_login is None:
                    print('\nТакого пользователя не существует!')
                    break
                else:

                    password = input('Введите пароль от аккаунта: ')
                    if len(password) == 0:
                        print('Ошибка! Cтрочка не должна быть пустой.')
                        break
                    else:
                        cur.execute(f"""SELECT Password FROM users_data WHERE Password = '{password}';""")
                        users_password = cur.fetchone()
                        attempt = 3

                    if users_password is None:
                        attempt -= 1  # Cлужит для отсчёта попыток
                        print(f'Пароль не подходит. Осталось попыток: {attempt}')

                        password = input('Введите пароль от аккаунта: ')
                        if len(password) == 0:
                            print('Ошибка! Cтрочка не должна быть пустой.')
                            break
                        else:
                            cur.execute(f"""SELECT Password FROM users_data WHERE Password = '{password}';""")
                            users_password = cur.fetchone()

                            if users_password is None:
                                attempt -= 1
                                print(f'Пароль не подходит. Осталось попыток: {attempt}')

                                password = input('Введите пароль от аккаунта: ')
                                if len(password) == 0:
                                    print('Ошибка! Cтрочка не должна быть пустой.')
                                    break
                                else:
                                    cur.execute(f"""SELECT Password FROM users_data WHERE Password = '{password}';""")
                                    users_password = cur.fetchone()

                                    if users_password is None:
                                        attempt -= 1
                                        print(f'Осталось попыток: {attempt}. Восстановите пароль, используя код!')
                                        break
                                    else:
                                        print('\nАвторизацуия прошла успешно!')
                            else:
                                print('\nАвторизацуия прошла успешно!')

                    else:
                        print('\nАвторизацуия прошла успешно!')

        break

    """Восстановление аккаунта"""
    while True:
        if action == recover_password:

            login = input('Введите cвой логин: ')
            if len(login) == 0:
                print('Ошибка! Cтрочка не должна быть пустой.')
                break
            else:
                cur.execute(f"""SELECT Login FROM users_data WHERE Login = '{login}';""")
                users_login = cur.fetchone()

                if users_login is None:
                    print('\nТакого пользователя не существует!')
                    break
                else:

                    recover_code = input('Введите восстанавливающий код: ')
                    if len(recover_code) == 0:
                        print('Ошибка! Cтрочка не должна быть пустой.')
                        break
                    else:
                        cur.execute(f"""SELECT Code FROM users_data WHERE Login = '{login}';""")
                        users_code = cur.fetchone()
                        date_code = users_code[0]

                        if str(date_code) != str(recover_code):
                            print('Вы ввели неверный код! Повторите попытку')
                            break
                        else:

                            new_password = input('Введите новый пароль, состоящий более чем из 3 символов: ')

                            if len(new_password) == 0:
                                print('Ошибка! Cтрочка не должна быть пустой.')
                                break
                            elif len(new_password) <= 3:
                                print('Пароль должен состоять минимум из 4 символов')
                                break
                            else:
                                cur.execute(f"""UPDATE users_data SET Password = '{new_password}' WHERE Login = '{login}'
                                AND Code = '{recover_code}';""")
                                db.commit()
                                print('\nНовый пароль установлен!')
        break
except KeyboardInterrupt:
    print('\nОперация отменена!')