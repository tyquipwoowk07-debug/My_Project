import os
import sqlite3
from database.database import create_tables,insert_sample_data
from resourses.Auth import Authorization
from resourses.User_Actions import LibrarianActions, UserActions
DB_FILE = "mainDataBase.db"
lib_act = LibrarianActions(DB_FILE)
user_act = UserActions(DB_FILE)

def main():
    # Если базы нет, создаем таблицы и вставляем тестовые данные
    if not os.path.exists(DB_FILE):
        create_tables(DB_FILE)
        insert_sample_data(DB_FILE)
    auth = Authorization(DB_FILE)

    # --- Основной цикл программы ---
    while True:
        user_role = ''
        print("**** Aвторизация ****")
        print("1 - Войти с ролью Библиотекарь")
        print("2 - Войти с ролью Читатель")
        print("3 - Регистрация ")
        print("0 - Выход (не в ту дверь вошел)")
        choice = input("Ваш выбор: ")
        if choice == "1":
            user_role = 'Libr'
            print("**** Aвторизация пользователя c ролью Библиотекарь ****")
            print("___ Логины и пароли ___")
            users = auth.get_all_users_Lib()
            for user in users:
                print(f"Логин: {user[0]} Пароль: {user[1]}")
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            Librarian_ID = auth.Librarian(Login = login,password = password)
            if Librarian_ID:
                print(f"Здравствуй, {login}!")
                break
            else:
                print('Указан некорректный логин или пароль.\n')
        elif choice == "2":
            user_role = 'User'
            print("\n**** Aвторизация пользователя c ролью Читатель ****")
            print("___ Логины и пароли ___")
            users = auth.get_all_users()
            for user in users:
                print(f"Логин: {user[0]} Пароль: {user[1]}")
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            user_id = auth.User(Login = login, password = password)
            if user_id:
                print(f"Здравствуй, {login}!")
                user_act.Looking_users_booking(user_id=user_id)
                break
            else:
                print('Указан некорректный логин или пароль.\n')
        elif choice == "3":
            user_role = 'User'
            print("**** Регистрация нового пользователя c ролью Читатель ****")
            login = input("Введите логин: ")
            password = input("Введите пароль (буквы\цифры\символы): ")
            user_id = auth.NewUser(Login = login, password = password)
            if user_id:
                print(f"Здравствуй, {login}!\n")
                break
            else:
                print('Указан некорректный логин или пароль.\n')
        elif choice == "0":
            print("Выход из программы...")
            break
        else:
           print('Некорректная команда, попробуйте снова\n')
    if choice != "0":
        while True:
            if user_role=='Libr':
                print("\n**** Выберите действие ****")
                print("1 - Выдать книгу Читателю")
                print("2 - Принять книгу у Читателя")
                print("3 - Добавить книгу")
                print("4 - Исправить данные книги (автор, название)")
                print("0 - Выход (я устал, я ухожу)")
                while True:
                    choice = input("Ваш выбор: ")
                    if choice.isdigit():
                        if 0 > int(choice) or int(choice) > 5:
                            print("Ошибка! Попробуйте ещё раз.")
                        else:
                            break
                    else:
                        print("Ошибка! Команда не найдена.")
                if choice == "1":
                    print("\n**** Выдача книги читателю ****")
                    try:
                        if lib_act.looking_booking():
                            print("")
                            BBID = int(input("Номер брони: "))
                            UID = int(input("ID забронировавшего Читателя: "))
                            if lib_act.Issuanse(Booking_Book_ID=BBID, User_ID=UID, Librarian_ID=Librarian_ID):
                                print("Книга успешно выдана")
                            else:
                                print('Ошибка при выдаче книги\n')
                    except ValueError:
                        print("Ошибка: номер брони и ID должны быть числами")
                    except Exception as e:
                        print(f"Произошла ошибка: {e}")
                    print("\n")
                elif choice == "2":
                    lib_act.looking_booking_up()
                    print("\n**** Принятие книги от Читателя ****")
                    try:
                        BI = int(input("\nВведите номер выдачи: "))
                    except ValueError:
                        print("Ошибка: введите число")
                        continue
                    if lib_act.Accept(Booking_ID=BI):
                        print("Книга успешно принята")
                    else:
                        print('Ошибка при принятии книги\n')
                elif choice == "3":
                    print("\n**** Добавление новой книги ****")
                    while True:
                        defect = input('Обнаружены дефекты? (да/нет)')
                        if defect.lower() in ['да', "нет"]:
                            break
                        else:
                            print("Введите корректную команду - да/нет")
                    if defect.lower()=="нет":
                        name_book = input("Ведите название книги: ")
                        author = input("Введите имя автора: ")
                        lib_act.AddBook(name_book = name_book,author = author)
                        print('\n')
                    else:
                        print('Возврат поставищку.')
                elif choice == "4":
                    print("**** Исправление опечаток ****")
                    while True:
                        try:
                            bookid =int(input("Введите id книги для исправления: "))
                            if lib_act.check_book_id(bookid=bookid):
                                break
                        except:
                            pass
                    while True:
                        print("1 - Исправить автора")
                        print("2 - Исправить название")
                        try:
                            choice1 = int(input())
                            if 1<=choice1<=2:
                                break
                            else:
                                print("Ошибка! Введите 1 или 2")
                        except:pass
                    if choice1 == 1:
                        val = input("Корректно введите имя автора: ")
                    elif choice1 == 2:
                        val = input("Корректно введите название книги: ")
                    else:
                        print("Определись,смертный,че тебе надо?")
                    lib_act.Correct(bookid = bookid, val = val, choice1 = choice1)
                    print('\n')
                elif choice == "0":
                    print("Выход из программы...")
                    lib_act.close()
                    break
            else:
                print("\n**** Выберите действие ****")
                print("1 - Взять книгу")
                print("2 - Поиск книг по автору \ названию \ ключевому слову")
                print("3 - Посмотреть каталог")
                print("4 - Просмотреть отзывы")
                print("5 - Оставить отзыв")
                print("0 - Выход (я устал, я ухожу)")
                while True:
                    choice = input("Ваш выбор: ")
                    if choice.isdigit():
                        if 0 > int(choice) or int(choice)>5:
                            print("Ошибка! Попробуйте ещё раз.")
                        else:
                            break
                    else:
                        print("Ошибка! Команда не найдена.")
                if choice == "1":
                    print("\n**** Взять книгу ****")
                    while True:
                        if user_act.take_book(user_id=user_id):
                            break
                if choice == "2":
                    user_act.SearchInformation(keyword = input("Введите слово для поиска: "))
                if choice == "3":
                    print("*** Посмотреть каталог***")
                    user_act.looking_catalog()
                if choice == "4":
                    print("*** Посмотреть отзывы***")
                    while True:
                        try:
                            id_book = int(input("Введите id книги: "))
                            if user_act.check_book_id(book_id=id_book):
                                break
                        except:
                            print('Некорректный ввод, попробуйте еще раз!')
                    user_act.looking_reviews(book_id = id_book)
                if choice == "5":
                    print("*** Оставить отзыв ***")
                    while True:
                        try:
                            id_book = int(input("Введите id книги: "))
                            if user_act.check_book_id(book_id=id_book):
                                break
                        except:
                            print('Некорректный ввод, попробуйте еще раз!')
                    text_for_review = str(input("Напишите отзыв: "))
                    while True:
                        score = int(input("Оцените книгу по 5-ти балльной шкале: "))
                        if 0<=score<=5:
                            break
                    user_act.Review(book_id = id_book, review_text = text_for_review, score=score)
                elif choice == "0":
                    print("Выход из программы...")
                    user_act.close()
                    break

if __name__ == "__main__":
    main()
