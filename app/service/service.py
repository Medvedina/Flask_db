from werkzeug.security import check_password_hash
from psycopg2 import Error

def check_password(account, password):
    if account and check_password_hash(account[2], password): 
        return account