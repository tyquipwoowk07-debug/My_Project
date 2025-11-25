import sqlite3, datetime
from models.models import Librarian, User, Book,Booking,Booking_Book,Status
class LibrarianActions:
    def __init__(self, db_file: str = "mainDataBase.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    def Issuanse(self,Booking_Book_ID: int, User_ID: int,Librarian_ID: int):
        '''
        После выдачи книги на руки установка статуса "Выдана" для книги по номеру брони и id пользователя, забронировавшего книгу
        '''
        book_ids = self.cursor.fetchall()
        if book_ids:
            print("У Пользователя имеется задолженность:")
            id_list = [book[0] for book in book_ids]
            books_on_user_hands = ','.join('?' * len(id_list))
            query = f"SELECT Name, Author FROM Book WHERE BOOK_ID IN ({books_on_user_hands})"
            self.cursor.execute(query, id_list)
            books = self.cursor.fetchall()
            for book in books:
                name, author = book
                print(f"- {name} (автор: {author})")
                return None
        self.cursor.execute("SELECT Book_ID FROM Booking_Book WHERE BOOKING_BOOK_ID = ? AND User_ID = ?", (Booking_Book_ID, User_ID))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute("SELECT COUNT(*) FROM Booking")
            Booking_ID = self.cursor.fetchone()[0] + 1
            booking = (Booking_ID, datetime.datetime.now().strftime('%d.%m.%Y'), "-", Librarian_ID, User_ID, 4)
            self.cursor.execute("INSERT INTO Booking (BOOKING_ID,ISSUE,RETURN,Librarian_ID,User_ID,Status_ID) VALUES (?,?,?,?,?,?)",booking)
            self.cursor.execute("SELECT Book_ID FROM Booking_Book WHERE BOOKING_BOOK_ID = ? AND User_ID = ?",(Booking_Book_ID, User_ID))
            self.cursor.execute("UPDATE Book SET Current_Status = 4 WHERE BOOK_ID = ?",(row['Book_ID'],))
            self.cursor.execute("UPDATE Booking_Book SET Booking_ID = ? WHERE BOOKING_BOOK_ID = ?", (Booking_ID, Booking_Book_ID))
            print(f'Книга выдана на руки Читателю, данные внесены в БД под ID {Booking_ID}')
            row = self.cursor.fetchone()
            self.conn.commit()
            return True
        else:
            print('Бронь не найдена или забронирована другим Читателем')
            return False
    def Accept(self, Booking_ID: int):
        '''
        После принятия книги у Читателя установить статус "Доступна" для книги по номеру брони и id пользователя,забронировавшего книгу
        '''
        self.cursor.execute("SELECT Book_ID FROM Booking_Book WHERE Booking_ID = ?",(Booking_ID,))
        row = self.cursor.fetchone()
        if row:
            Book_ID = row['Book_ID']
            self.cursor.execute("UPDATE Book SET Current_Status = 1 WHERE BOOK_ID = ?",(Book_ID,))
            self.cursor.execute("UPDATE Booking SET Status_ID = 1, RETURN = ? WHERE BOOKING_ID = ?",(datetime.datetime.now().strftime('%d.%m.%Y'),Booking_ID,))
            self.conn.commit()
            return True
        else:
            print("Не нашли id книги")
            return False
    def AddBook(self,name_book: str, author: str):
        '''
        Добавить новую книгу и его автора в базу данных
        '''
        self.cursor.execute("SELECT COUNT(*) FROM Book")
        Book_ID = self.cursor.fetchone()[0] + 1
        self.cursor.execute("INSERT INTO Book (BOOK_ID,Name,Author,Current_Status) VALUES (?,?,?,?)",(Book_ID,name_book,author,1))
        self.conn.commit()
        print("Книга и его автор добавлены в базу данных")
        return None
    def check_book_id(self, bookid: int):
        self.cursor.execute(f"SELECT * FROM Book WHERE BOOK_ID = {bookid}")
        if not self.cursor.fetchall():
            print('Книга с указанным ID отсутствует в базе данных')
            return False
        else:
            return True
    def looking_booking(self):
        self.cursor.execute('''
            SELECT 
                b.BOOK_ID,
                b.Name,
                b.Author,
                b.Current_Status,
                bb.BOOKING_BOOK_ID,
                bb.User_ID
            FROM 
                Book b
            LEFT JOIN 
                Booking_Book bb ON b.BOOK_ID = bb.Book_ID AND bb.Booking_ID IS NULL
            WHERE 
                b.Current_Status = ?
        ''', (3,))
        books = self.cursor.fetchall()
        if not books:
            print('Актуальныx броней нет')
            return False
        for book in books:
            print(f"ID: {book[0]} | '{book[1]}' | Автор: {book[2]} | Статус: {book[3]} | Id читательской брони: {book[4]} | ID читателя: {book[5]}")
        return  True
    def looking_booking_up(self):
        self.cursor.execute('''
                            SELECT 
                                b.BOOK_ID,
                                b.Name,
                                b.Author,
                                b.Current_Status,
                                bb.BOOKING_BOOK_ID,
                                bb.User_ID AS Booking_User_ID,
                                bb.Booking_ID
                            FROM 
                                Book b
                            LEFT JOIN 
                                Booking_Book bb ON b.BOOK_ID = bb.Book_ID
                            LEFT JOIN 
                                Booking bk ON bb.Booking_ID = bk.BOOKING_ID
                            WHERE 
                                b.Current_Status = ?
                        ''', (4,))
        books = self.cursor.fetchall()
        if not books:
            print('Нет книг, выданных на руки')
            return False
        for book in books:
            print(f"ID: {book[0]} | '{book[1]}' | Автор: {book[2]} | Статус: {book[3]} | Id читательской брони: {book[4]} | ID читателя: {book[5]} | ID выдачи: {book[6]}")
        return True
    def Correct(self,bookid: int, choice1: int, val: str):
        '''
        Исправить опечатки и некорректные данные
        '''
        if choice1 == 1:
            self.cursor.execute("UPDATE Book SET Author = ? WHERE BOOK_ID = ?",(val,bookid))
        if choice1 == 2:
            self.cursor.execute("UPDATE Book SET Name = ? WHERE BOOK_ID = ?",(val,bookid))
            self.conn.commit()
        print("Данные обновлены!")
        return None
    def close(self):
        self.conn.close()
class UserActions:
    def __init__(self, db_file: str = "mainDataBase.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    def looking_catalog(self):
        """Показать все книги со статусами"""
        self.cursor.execute('''
            SELECT 
                b.BOOK_ID,
                b.Name AS Book_Name, 
                b.Author, 
                s.Name AS Status 
            FROM Book b 
            JOIN Status s ON b.Current_Status = s.STATUS_ID
            ORDER BY b.BOOK_ID
        ''')
        all_books = self.cursor.fetchall()

        print(f"Всего книг в каталоге: {len(all_books)}")
        if not all_books:
            print("В каталоге нет книг")
        else:
            print("\n" + "=" * 50)
            print("КАТАЛОГ ВСЕХ КНИГ")
            print("=" * 50)
            for book in all_books:
                print(f"ID: {book[0]:<3} | '{book[1]:<20}' | Автор: {book[2]:<15} | Статус: {book[3]}")
            print("=" * 50)
    def check_book_id(self,book_id: int):
        self.cursor.execute("SELECT BOOK_ID, Name, Author, Current_Status FROM Book WHERE BOOK_ID = ?", (book_id,))
        book = self.cursor.fetchone()
        if not book:
            print("Книга не найдена в БД")
            return False
        else:
            return True
    def take_book(self, user_id: int):
        """Взять книгу"""
        self.cursor.execute("SELECT BOOK_ID, Name, Author FROM Book WHERE Current_Status = '1'")
        available_books = self.cursor.fetchall()
        print(f"Найдено книг: {len(available_books)}")
        if not available_books:
            print("Нет доступных книг")
        else:
            print("\n___ Доступные книги ___")
            for book in available_books:
                print(f"ID: {book[0]} - '{book[1]}' (автор: {book[2]})")
        book_id = int(input("\nВведите ID книги: "))
        self.cursor.execute("SELECT BOOK_ID, Name, Author, Current_Status FROM Book WHERE BOOK_ID = ?", (book_id,))
        book = self.cursor.fetchone()
        if not book:
            print("Книга не найдена в БД")
            return False
        else:
            book_id, book_name, author, status = book
            print(f"Найдена: ID={book_id}, '{book_name}', автор={author}, статус='Забронированно'")
            if str(status) != "1":
                print(f"Книга недоступна")
                return False
            else:
                self.cursor.execute("SELECT COUNT(*) FROM Booking_Book")
                booking_book_id = self.cursor.fetchone()[0] + 1
                print(f"ID вашей брони: {booking_book_id}.Для получения книги на руки назовите его библиотекарю")
                booking_book = [(booking_book_id,book_id,None,user_id),]
                self.cursor.executemany("INSERT INTO Booking_Book (BOOKING_BOOK_ID, Book_ID, Booking_ID, User_ID ) VALUES (?,?,?,?)",booking_book)
                self.cursor.execute("UPDATE Book SET Current_Status = ? WHERE BOOK_ID = ?", (3,book_id))
                self.conn.commit()
                return True
    def Review(self, book_id: int, review_text: str, score: int):
        '''
        Оставить отзыв о прочитанной книге
        '''
        self.cursor.execute('''INSERT INTO Reviews (BOOK_ID, Review, Score) VALUES (?, ?, ?)''', (book_id, review_text, score))
        self.conn.commit()
    def Looking_users_booking(self,user_id: int):
        self.cursor.execute('''
            SELECT 
                b.BOOK_ID,
                b.Name,
                b.Author,
                b.Current_Status,
                bb.BOOKING_BOOK_ID,
                bb.User_ID
            FROM 
                Book b
            LEFT JOIN 
                Booking_Book bb ON b.BOOK_ID = bb.BOOK_ID
            WHERE 
                b.Current_Status = ? and bb.User_ID=?                
        ''', (3,user_id))
        books = self.cursor.fetchall()
        if not books:
            print('Актуальныx броней нет')
            return False
        for book in books:
            print("\n___ Ваши бронирования ___")
            print(f"ID: {book[0]} | '{book[1]}' | Автор: {book[2]} | Статус: {book[3]} | Id читательской брони: {book[4]}")
        return True
    def looking_reviews(self, book_id: int):
        """Показать все отзывы для конкретной книги"""
        try:
            self.cursor.execute('''
                SELECT Name, Author FROM Book WHERE BOOK_ID = ?
            ''', (book_id,))
            book_info = self.cursor.fetchone()
            if not book_info:
                print(f"Книга с ID {book_id} не найдена")
                return
            book_name, book_author = book_info
            self.cursor.execute('''
                SELECT REVIEWS_ID, Review, Score 
                FROM Reviews 
                WHERE BOOK_ID = ?
                ORDER BY REVIEWS_ID
            ''', (book_id,))
            reviews = self.cursor.fetchall()
            print("\n" + "="*60)
            print(f"ОТЗЫВЫ НА КНИГУ:")
            print(f"ID: {book_id} | '{book_name}' | Автор: {book_author}")
            print("="*60)
            if not reviews:
                print("Пока нет отзывов на эту книгу")
            else:
                print(f"Всего отзывов: {len(reviews)}")
                print("-" * 60)
                for review in reviews:
                    review_id, review_text, score = review
                    print(f"Отзыв ID: {review_id}")
                    print(f"Оценка: {score}/10")
                    print(f"Текст: {review_text}")
                    print("-" * 40)
        except Exception as e:
            print(f"Ошибка при получении отзывов: {e}")
    def SearchInformation(self, keyword: str):
        '''
        Просматривать информаицю об авторах
        '''
        self.cursor.execute("SELECT Name, Author FROM Book")
        all_books = self.cursor.fetchall()
        print("Все книги в базе:")
        for book in all_books:
            print(f"  - '{book[0]}' автор: '{book[1]}'")
        self.cursor.execute('''
            SELECT 
                b.BOOK_ID,
                b.Name,
                b.Author,
                b.Current_Status,
                AVG(CAST(r.Score AS REAL)) as Average_Score,
                COUNT(r.REVIEWS_ID) as Review_Count
            FROM 
                Book b
            LEFT JOIN 
                Reviews r ON b.BOOK_ID = r.BOOK_ID
            WHERE 
                b.Name LIKE '%' || ? || '%' 
                OR b.Author LIKE '%' || ? || '%'
                OR b.Current_Status LIKE '%' || ? || '%'
                OR b.Name LIKE '%' || ? || '%' 
                OR b.Author LIKE '%' || ? || '%'
                OR b.Current_Status LIKE '%' || ? || '%'
            GROUP BY 
                b.BOOK_ID, b.Name, b.Author, b.Current_Status
            ORDER BY 
                Average_Score DESC NULLS LAST
        ''', (keyword, keyword, keyword, keyword.lower(), keyword.lower(), keyword.lower()))

        results = self.cursor.fetchall()

        # Дополнительная отладка
        print(f"\nПоиск по ключу: '{keyword}'")
        print(f"Найдено записей: {len(results)}")

        if not results:
            print(f"\Результаты поиска по запросу: '{keyword}'")
            print("┌" + "─" * 50 + "┐")
            print("│" + " " * 50 + "│")
            print("│" + "Книги не найдены".center(50) + "│")
            print("│" + " " * 50 + "│")
            print("└" + "─" * 50 + "┘")
            return
        else:
            print(f"\nРезультаты поиска: '{keyword}'")
            print(f"Найдено книг: {len(results)}")
            print("ID    Название книги                     Автор              Статус     Оценка    Отзывов")
            print("----  ----------------------------------  ------------------  ---------  --------  --------")

            for row in results:
                book_id, name, author, status, avg_score, review_count = row
                avg_score_display = f"{avg_score:.2f} ⭐" if avg_score is not None else "   ─   "
                name_display = name if len(name) <= 30 else name[:27] + "..."
                author_display = author if len(author) <= 18 else author[:15] + "..."
                status_display = status if len(status) <= 10 else status[:7] + "..."
                print(f"{book_id:<4}  {name_display:<32}  {author_display:<18}  {status_display:<9}  {avg_score_display:<8}  {review_count:<8}")
            print(f"\n")
    def close(self):
        self.conn.close()
