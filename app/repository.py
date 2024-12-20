import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import Error

class Repository:
    def __init__(self):
        self.connection = None
        self.cursor = None
        try:
            self.connection = psycopg2.connect(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                    id SERIAL PRIMARY KEY,
                                    login VARCHAR(255) NOT NULL UNIQUE,
                                    password VARCHAR(255) NOT NULL,
                                    full_name VARCHAR(100) NOT NULL,
                                    birth_date DATE,
                                    role VARCHAR(100) NOT NULL
                                    );''')
            self.connection.commit()
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def get_user(self, login, password):
        if not self.connection or not self.cursor:
            print("Соединение с базой данных не установлено.")
            return None
        
        try:
            self.cursor.execute('SELECT id, login, password FROM accounts WHERE login = %s;', (login, ))
            account = self.cursor.fetchone()

            if account and check_password_hash(account[2], password): 
                return account  
            else:
                print("Неверный логин или пароль.")
                return None

        except Exception as e:
            print(f'Произошла ошибка: {e}')
            return None

    def register_user(self, account):
        if not self.connection or not self.cursor:
            print("Соединение с базой данных не установлено.")
            return False

        try:
            self.cursor.execute('''INSERT INTO accounts (login, password, full_name, birth_date, role)
                                   VALUES (%s, %s, %s, %s, %s)''', 
                                   (account.login, generate_password_hash(account.password), 
                                    account.full_name, account.birth_date, account.role))
            self.connection.commit()
            return True
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            self.connection.rollback()
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

def get_repository():
    return Repository()