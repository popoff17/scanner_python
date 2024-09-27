from db.db import DatabaseManager
from user import User
from menu import Menu, MenuItem
#from parser import Parser
import pdb # отладка


class Application:
    def __init__(self):
        self.db_manager = DatabaseManager()  # Создаем объект для управления базой данных
        self.session = None
        self.user = User()
        self.parser = None
        self.menu = None

    def initialize(self):
        """Инициализация базы данных и всех компонентов."""
        self.session = self.db_manager.initialize_db()  # Инициализируем базу данных
        #self.parser = Parser(self.session)  # Передаем сессию в парсер

    def authorize_user(self):
        """Авторизация пользователя."""
        while not self.user.username:
            if self.user.authorize():
                break

    def setup_menu(self):
        """Настраиваем меню для приложения."""
        # Создаем экземпляр класса Menu без меню
        self.menu = Menu(root_menu=None)

        # Теперь создаем main_menu с передачей метода show_message из объекта self.menu
        main_menu = MenuItem("Главное меню", sub_menu=[
            MenuItem("Анализ сайта", sub_menu=[
                MenuItem("Установить страницу", self.menu.show_message),
                MenuItem("Анализ CSS", self.menu.show_message),
                MenuItem("Анализ JS", self.menu.show_message)
            ]),
            MenuItem("Обработать сайт полностью", self.menu.show_message)
        ])

        # Теперь присваиваем созданное меню как root_menu в объекте self.menu
        self.menu.root_menu = main_menu



    def run(self):


        """Запуск приложения."""
        # Инициализация
        self.initialize()
        # Авторизация
        self.authorize_user()
        # Настройка меню
        self.setup_menu()
        # Запуск меню
        self.menu.navigate(self.session)
        # Закрытие сессии после завершения
        self.db_manager.close_session(self.session)

if __name__ == "__main__":
    app = Application()
    app.run()
