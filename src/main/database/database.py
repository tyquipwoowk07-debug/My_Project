import sqlite3
from sqlite3 import Connection

def get_connection(db_name: str = "mainDataBase.db") -> Connection:
    """
    Создает соединение с базой данных SQLite.
    Если файл базы данных не существует, он будет создан.
    """
    return sqlite3.connect(db_name)


def create_tables(db_name: str = "mainDataBase.db"):
    """
    Создает таблицы Librarian,User,Book,Booking,Booking_Book,Status,Reviews если их еще нет.
    """
    conn = get_connection(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Librarian (
            LIBRARIAN_ID INTEGER PRIMARY KEY,
            Login TEXT NOT NULL,
            Password TEXT NOT NULL            
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User(
            USER_ID INTEGER PRIMARY KEY,
            Login TEXT NOT NULL,
            Password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Book(
            BOOK_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Author TEXT NOT NULL,
            Current_Status TEXT NOT NULL,
            FOREIGN KEY (Current_Status) REFERENCES Status(STATUS_ID)
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Status(
                STATUS_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL
            )
        ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Reviews(
                    REVIEWS_ID INTEGER PRIMARY KEY,
                    BOOK_ID INTEGER,
                    Review NEXT NOT NULL,
                    Score TEXT NOT NULL,
                    FOREIGN KEY (BOOK_ID) REFERENCES Book(Book_ID)
                )
            ''')

    cursor.execute('''
         CREATE TABLE IF NOT EXISTS Booking(
            BOOKING_ID INTEGER PRIMARY KEY,
            ISSUE TEXT NOT NULL,
            RETURN TEXT NOT NULL,
            Librarian_ID INTEGER,
            User_ID INTEGER,
            Status_ID INTEGER,
            FOREIGN KEY (Librarian_ID) REFERENCES Librarian(LIBRARIAN_ID),
            FOREIGN KEY (User_ID) REFERENCES User(USER_ID),
            FOREIGN KEY (Status_ID) REFERENCES Status(STATUS_ID)  
        )
    ''')

    cursor.execute('''
             CREATE TABLE IF NOT EXISTS Booking_Book(
                BOOKING_BOOK_ID INTEGER PRIMARY KEY,
                Book_ID INTEGER,
                Booking_ID INTEGER,
                User_ID INTEGER,
                FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID),
                FOREIGN KEY (Booking_ID) REFERENCES Booking(Booking_ID),
                FOREIGN KEY (User_ID) REFERENCES User(USER_ID)       
            )
        ''')

    conn.commit()
    conn.close()

def insert_sample_data(db_name: str = "mainDataBase.db"):
    """
    Вставляет тестовые записи в таблицы Book,Booking,Booking_Book,Status,
    если они еще не добавлены
    """
    conn = get_connection(db_name)
    cursor = conn.cursor()

    # Проверка, есть ли пользователи
    cursor.execute("SELECT COUNT(*) FROM User")
    if cursor.fetchone()[0] == 0:
        users = [
            (1, "Юзер-лузер", "abc"),
            (2, "Юзер-абьюзер", "def"),
            (3, "Биба", "ghi"),
            (4, "Боба", "jkl")
        ]
        cursor.executemany("INSERT INTO User (USER_ID, Login, Password) VALUES (?,?,?)", users)
        print("Добавлены пользователи.")

    # Проверка, есть ли книги
    cursor.execute("SELECT COUNT(*) FROM Book")
    if cursor.fetchone()[0] == 0:
        books = [
            (1,"Джек Лондон", "Морской волк",1),
            (2,"Агата Кристи", "Убийства по алфавиту",1),
            (3,"Дэн Браун", "Код да Винчи",1),
            (4,"Уильям Голдинг", "Повелитель мух",1)
        ]
        cursor.executemany("INSERT INTO Book (BOOK_ID, Author, Name,Current_Status) VALUES (?,?,?,?)", books)
        print("Добавлены книги.")

    # Проверка, есть ли статус
    cursor.execute("SELECT COUNT(*) FROM Status")
    if cursor.fetchone()[0] == 0:
        status = [
            (1, "Доступно"),
            (2, "Нет в наличии"),
            (3, "Забронировано"),
            (4, "Выдана"),
        ]
        cursor.executemany("INSERT INTO Status (STATUS_ID, Name) VALUES (?,?)", status)
        print("Добавлены статусы.")

    # Проверка, есть ли бронь
    cursor.execute("SELECT COUNT(*) FROM Booking")
    if cursor.fetchone()[0] == 0:
        booking = [
            (1,'01.05.2025',"",1,2,3),
            (2,'05.05.2025','15.05.2025',1,1,1),
            (3,'10.05.2025','25.05.2025',2,3,2),
        ]
        cursor.executemany("INSERT INTO Booking (BOOKING_ID,ISSUE,RETURN,Librarian_ID,User_ID,Status_ID) VALUES (?,?,?,?,?,?)", booking)
        print("Добавлены статусы.")

    # Проверка, есть ли библиотекарей
    cursor.execute("SELECT COUNT(*) FROM Librarian")
    if cursor.fetchone()[0] == 0:
        librarian = [
            (1, "Люциус", "12345"),
            (2, "Жорик", "54321"),
        ]
        cursor.executemany("INSERT INTO Librarian (LIBRARIAN_ID, Login, Password) VALUES (?,?,?)", librarian)
        print("Добавлены библиотекари.")

    # Проверка, есть ли бронь книги
    cursor.execute("SELECT COUNT(*) FROM Booking_Book")
    if cursor.fetchone()[0] == 0:
        booking_book = [
            (1,3,2),
            (2,1,2),
        ]
        cursor.executemany("INSERT INTO Booking_Book (BOOKING_BOOK_ID, Book_ID, Booking_ID ) VALUES (?,?,?)", booking_book)
        print("Добавлены брони книг.")
    cursor.execute("SELECT COUNT(*) FROM Reviews")
    if cursor.fetchone()[0] == 0:
        Reviews = [
            (1, 1, "Отличная книга!", 5),
            (2,2, "Такое себе", 4),
            (3, 1, "Затянуто", 4),
        ]
        cursor.executemany("INSERT INTO Reviews (REVIEWS_ID,BOOK_ID,Review,Score) VALUES (?,?,?,?)", Reviews)
        print("Добавлены библиотекари.")

    conn.commit()
    conn.close()
create_tables()
insert_sample_data()
