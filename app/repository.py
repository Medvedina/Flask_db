from app.service.service import check_password
import os
import psycopg2
import sys
from werkzeug.security import generate_password_hash
from psycopg2 import Error, pool

class Repository:
    def __init__(self):
        db_config = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }

        try:
            connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20, **db_config)
        except Exception as error:
            raise error
        
        try:
            self.connection = connection_pool.getconn()
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
            raise error

    def get_user(self, login, password):
        if not self.connection or not self.cursor:
            print("Соединение с базой данных не установлено.")
            sys.exit(Error)  
        
        try:
            self.cursor.execute('SELECT id, login, password FROM accounts WHERE login = %s;', (login, ))
            account = self.cursor.fetchone()
            return check_password(account, password)
        except Exception as error:
            raise error
        

    def register_user(self, account):
        if not self.connection or not self.cursor:
            print("Соединение с базой данных не установлено.")
            sys.exit(Error)

        try:
            self.cursor.execute('''INSERT INTO accounts (login, password, full_name, birth_date, role)
                                   VALUES (%s, %s, %s, %s, %s)''', 
                                   (account.login, generate_password_hash(account.password), 
                                    account.full_name, account.birth_date, account.role))
            self.connection.commit()
            return True
        except Exception as error:
            print(f'Произошла ошибка: {error}')
            self.connection.rollback()
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

def get_repository():
    return Repository()