import os
import getpass
from sqlalchemy.orm import sessionmaker
from db.db import DatabaseManager
from db.tables import UserTable

class User:
    def __init__(self):
        self.username = None
        self.session = DatabaseManager.initialize_db()  # Создаем сессию для работы с БД

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def authorize(self):
        self.clear_screen()
        print("=== Авторизация ===")
        username = input("Введите логин: ")
        password = getpass.getpass("Введите пароль: ")

        # Проверка пользователя в базе данных
        user = self.session.query(UserTable).filter_by(username=username, password=password).first()

        if user:
            self.clear_screen()
            print(f"\nДобро пожаловать, {user.name}!\n")
            self.username = username
            return True
        else:
            self.clear_screen()
            print("\nНеверный логин или пароль.\n")
            return False

    def get_user_info(self):
        if self.username:
            user = self.session.query(UserTable).filter_by(username=self.username).first()
            if user:
                return {'name': user.name, 'age': user.age}
        return {}

    def close(self):
        DatabaseManager.close_session(self.session)  # Закрываем сессию после завершения работы
