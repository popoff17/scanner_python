from db.db import DatabaseManager
from user import User
from menu import Menu, MenuItem
from helpers import Helper  # Импортируем класс Helper для очистки экрана


class Application:
    def __init__(self):
        self.db_manager = DatabaseManager()  # Создаем объект для управления базой данных
        self.session = None
        self.user = User()
        self.menu = None
        self.helper = Helper()  # Создаем объект Helper для очистки экрана

    def initialize(self):
        """Инициализация базы данных и всех компонентов."""
        self.session = self.db_manager.initialize_db()  # Инициализируем базу данных

    def authorize_user(self):
        """Авторизация пользователя."""
        while not self.user.username:
            if self.user.authorize():
                break

    def setup_menu(self):
        """Настраиваем меню для приложения."""
        # Создаем главное меню
        main_menu = MenuItem("Главное меню", sub_menu=[
            MenuItem("Анализ сайта", sub_menu=[
                MenuItem("Установить страницу", self.show_message),
                MenuItem("Анализ CSS", self.show_message),
                MenuItem("Анализ JS", self.show_message)
            ]),
            MenuItem("Обработать сайт полностью", self.show_message)
        ])

        # Инициализируем объект Menu с главным меню
        self.menu = Menu(root_menu=main_menu)

    def show_message(self):
        """Пример действия для меню."""
        print("Этот метод был вызван!")
        input("Нажмите Enter для продолжения...")

    def run(self):
        """Запуск приложения."""
        try:
            # Инициализация
            self.initialize()
            # Авторизация
            self.authorize_user()
            # Настройка меню
            self.setup_menu()

            current_menu = self.menu.root_menu  # Начинаем с главного меню
            previous_menus = []  # Стек для хранения предыдущих уровней меню
            breadcrumb = [current_menu]  # Хлебные крошки для навигации

            # Основной цикл приложения
            while True:
                try:
                    result = self.menu.navigate(current_menu, breadcrumb)
                except KeyboardInterrupt:
                    # Вывести сообщение и предложить пользователю завершить работу
                    print("\nЗавершить программу? (y/n): ", end="")
                    choice = input().strip().lower()
                    if choice == 'y':
                        break
                    else:
                        continue

                # Очистка экрана
                Helper.clear_screen()

                if result == 'exit':
                    # Если 0 было выбрано в главном меню — выход из программы
                    if not previous_menus:
                        break
                    else:
                        # Если в подменю выбрали 0, возвращаемся на предыдущий уровень
                        current_menu = previous_menus.pop()
                        breadcrumb.pop()
                        continue
                elif isinstance(result, MenuItem):
                    if result.is_leaf():
                        # Если выбранный элемент — лист (нет подменю), то выполняем действие
                        result.run()
                    else:
                        # Сохраняем текущее меню в стек и переходим в подменю
                        previous_menus.append(current_menu)
                        breadcrumb.append(result)
                        current_menu = result
                else:
                    print("Неверный выбор, попробуйте снова.")

        finally:
            # Закрытие сессии после завершения
            self.db_manager.close_session(self.session)



if __name__ == "__main__":
    app = Application()
    app.run()
