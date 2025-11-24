# models/models.py
class Librarian:
    """
    Модель для таблицы Librarian
    Поля:
    - Librarian_ID: уникальный идентификатор пользователя с ролью "Библиотекарь"
    - Login: логин пользователя с ролью "Библиотекарь"
    - Password: пароль пользователя с ролью "Библиотекарь"
    """
    def __init__(self, Librarian_ID, Login, Password):
        self.Librarian_ID = Librarian_ID
        self.Login = Login
        self.Password = Password

class User:
    """
    Модель для таблицы User
    Поля:
    - User_ID: уникальный идентификатор пользователя с ролью "Участник"
    - Login: логин пользователя с ролью "Участник"
    - Password: пароль пользователя с ролью "Участник"
    """
    def __init__(self, User_ID, Login, Password):
        self.User_ID = User_ID
        self.Login = Login
        self.Password = Password

class Book:
    """
    Модель для таблицы Book
    Поля:
    - Book_ID: уникальный идентификатор каждой книги
    - Name: название книги
    - Author: автор произведения
    - Current_Status: текущий статус книги
    """
    def __init__(self, Book_ID, Name, Author,Current_Status):
        self.Book_ID = Book_ID
        self.Name = Name
        self.Author = Author
        self.Current_Status = Current_Status

class Status:
    """
    Модель для таблицы Status
    Поля:
    - Status_ID: идентификатор
    - Name: статус
    """
    def __init__(self, Status_ID, Name):
        self.Status_ID = Status_ID
        self.Name = Name

class Booking:
    """
    Модель для таблицы Booking
    Поля:
    - Booking_ID: идентификатор
    - Issue: дата выдачи книги
    - Return: дата возврата книги
    - Librarian_ID: идентификатор библиотекаря
    - User_ID: идентификатор участника
    - Status_ID: идентификатор статуса книги
    """
    def __init__(self, Booking_ID, Issue, Return, Librarian_ID, User_ID, Status_ID):
        self.Booking_ID = Booking_ID
        self.Issue = Issue
        self.Return = Return
        self.Librarian_ID = Librarian_ID
        self.User_ID = User_ID
        self.Status_ID = Status_ID

class Booking_Book:
    """
    Модель для таблицы Booking_Book
    Поля:
    - Booking_Book_ID: идентификатор брони книги
    - Book_ID: идентификатор книги
    - Booking_Id: идентификатор брони
    """
    def __init__(self, Booking_Book_ID, Book_ID, Booking_ID, User_ID):
        self.Booking_Book_ID = Booking_Book_ID
        self.Book_ID = Book_ID
        self.Booking_ID = Booking_ID
        self.User_ID = User_ID

class Reviews:
    """
    Модель для таблицы Reviews
    Поля:

    """