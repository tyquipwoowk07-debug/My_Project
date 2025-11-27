import sqlite3
from models.models import Librarian, User

class Authorization:
    '''
    Авторизация существующего пользователя с ролью Библиотекарь или Читатель
    "Регистарция нового пользователя с ролью Чиnатель
    '''

    def __init__(self, db_file: str = "mainDataBase.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_all_users(self):
        """Получить всех пользователей из базы данных"""
        self.cursor.execute("SELECT Login, Password FROM User")
        return self.cursor.fetchall()
    def get_all_users_Lib(self):
        """Получить всех пользователей из базы данных"""
        self.cursor.execute("SELECT Login, Password FROM Librarian")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    ''' Аворизация пользователя с ролью Библиотекарь'''
    def Librarian(self, Login: str, password: str):
        self.cursor.execute("SELECT LIBRARIAN_ID FROM Librarian WHERE Login = ? AND Password = ?", (Login,password))
        row = self.cursor.fetchone()
        if row:
            return row['Librarian_ID']
        return None

    ''' Авторизация пользователя с ролью Читатель'''
    def User(self, Login: str, password: str):
        self.cursor.execute("SELECT USER_ID FROM User WHERE Login = ? AND Password = ?", (Login,password))
        row = self.cursor.fetchone()
        if row:
            return row['User_ID']
        else:
            return False

    ''' Добавление нового пользователя'''

    def NewUser(self, Login: str, password: str):
        self.cursor.execute("SELECT COUNT(*) FROM User")
        USER_ID = self.cursor.fetchone()[0] + 1
        users = [(USER_ID, Login, password)]
        self.cursor.executemany("INSERT INTO User (USER_ID, Login, Password) VALUES (?,?,?)", users)
        print(f"Пользователь с логином {Login} успешно добавлен! Ваш ID {USER_ID}.")
        self.conn.commit()
        return True

def close(self):
    self.conn.close()

