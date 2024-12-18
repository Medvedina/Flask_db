from typing import List
import psycopg2
import os
from abc import ABCMeta, abstractmethod
from psycopg2 import Error
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from .models.account import Account

class Repository:
    @abstractmethod
    def get_user(self, login, password) -> Account:
        pass

load_dotenv()

class PostgresQLRepository(Repository):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                    id SERIAL PRIMARY KEY,
                                    login VARCHAR(255) NOT NULL UNIQUE,
                                    password VARCHAR(255) NOT NULL,
                                    firstname VARCHAR(100) NOT NULL,
                                    lastname VARCHAR(100) NOT NULL,
                                    birth_date DATE,
                                    role VARCHAR(100) NOT NULL
                                    );''')
            self.connection.commit()
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            


    def get_user(self, login, password):
        try:
            self.cursor.execute('SELECT id, login, password FROM accounts WHERE login = %s;', (login,))
            account = self.cursor.fetchone()
            
            if account:
                if check_password_hash(account[2], password):
                    return account
                else:
                    print('Неверный пароль')
            else:
                print('Пользователь не найден')
        except Exception as e:
            print(f'Произошла ошибка: {e}')
        finally:
            return account 

        
    def register_user(self, login, password, first_name, last_name, birth_date = None, role = 'User'):
        try:
            self.cursor.execute('''INSERT INTO accounts (login, password, firstname, lastname, birth_date, role)
                                VALUES (%s, %s, %s, %s, %s, %s)''', (login, generate_password_hash(password), first_name, last_name, birth_date, role))
            self.connection.commit()
            return True
        except Exception as e:
            print(f'Произошла ошибка: {e}')
            self.connection.rollback()


def get_repository():
    return PostgresQLRepository()