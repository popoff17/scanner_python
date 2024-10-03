import sys
import pprint
from db.db import DatabaseManager
from user import User
#from menu import Menu, MenuItem
from menu import MainMenu
from parser import Parser
from helpers import Helper  # Импортируем класс Helper для очистки экрана


class Application:
    def __init__(self):
        self.db_manager = DatabaseManager()  # Создаем объект для управления базой данных
        self.session = None
        self.user = User()
        self.menu = MainMenu(self)
        self.currentMenuTitle = "Главное меню"
        self.prevMenuTitle = ""
        self.action = ""
        self.helper = Helper()  # Создаем объект Helper для очистки экрана
        self.parser = None
        self.project_domain = ""  # тут хранится домен сайта для парсинга, наш проект


    def initialize(self):
        """Инициализация базы данных и всех компонентов."""
        self.session = self.db_manager.initialize_db()  # Инициализируем базу данных
        self.parser = Parser(self.session)

    def authorize_user(self):
        """Авторизация пользователя."""
        while not self.user.username:
            if self.user.authorize():
                break

    def show_message(self):
        """Пример действия для меню."""
        print("Этот метод был вызван!")



    #запуск динамических методов из меню
    def call_dynamic_method(self, class_name_or_obj, method_name, *args):
        #примеры вызова метода:
        #print("1")
        #app.helper.test_text()
        #print("2")
        #app.call_dynamic_method("app.helper","test_text")
        #print("3")
        #app.call_dynamic_method("Helper","test_text")

       # Если передана строка
        if isinstance(class_name_or_obj, str):
            # Попробуем получить класс из глобального пространства имен
            obj_class = globals().get(class_name_or_obj)
            if obj_class is not None:
                obj = obj_class()  # Создаем экземпляр класса
            else:
                # Если не удалось найти класс, проверяем, является ли это полным именем объекта
                try:
                    obj = eval(class_name_or_obj)
                except NameError:
                    print(f"Класс или объект '{class_name_or_obj}' не найден.")
                    return
        elif isinstance(class_name_or_obj, object):
            obj = class_name_or_obj
        else:
            print(f"Некорректный аргумент: {class_name_or_obj}")
            return
        # Проверяем, есть ли метод в объекте
        if hasattr(obj, method_name):
            method = getattr(obj, method_name)
            if callable(method):
                method(*args)  # Вызываем метод с аргументами
            else:
                print(f"'{method_name}' не является вызываемым методом.")
        else:
            print(f"Метод '{method_name}' не найден в классе '{obj.__class__.__name__}'")


    def run(self):
        """Запуск приложения."""
        try:
            # Инициализация
            self.initialize()
            # Авторизация
            self.authorize_user()
            # Настройка меню

            # Инициализируем стек для истории меню
            self.menuHistory = []
            while True:
                Helper.clear_screen()
                try:
                    # Выводим пункты меню
                    activeMenu = self.menu.showMenu(self.currentMenuTitle)
                    #проверка что вернула функция - действие или меню
                    if isinstance(activeMenu, str):
                        #app.call_dynamic_method("app.helper","test_text")
                        callFunc = Helper.getClassAndMethod(activeMenu)
                        if callFunc[0] != "" and callFunc[1] != "" :
                            app.call_dynamic_method(callFunc[0],callFunc[1])
                        #возвращаем указатель меню на предыдущий уровень
                        self.currentMenuTitle = self.menuHistory.pop()

                    elif isinstance(activeMenu, list):
                        # Выводим пункты с нумерацией
                        counter = 1
                        for menu_item in activeMenu:
                            print(str(counter) + " - " + menu_item)
                            counter += 1
                        # Добавляем пункт "Назад" или "Выход"
                        if len(self.menuHistory) > 0:  # Если есть история, показываем "Назад"
                            print("0 - Назад")
                        else:  # Если мы в корневом меню, показываем "Выход"
                            print("0 - Выход")
                        # Ждем ввода цифры от пользователя
                        action = input("Выберите действие: ")

                        # Проверяем, является ли введенное значение числом и корректным индексом
                        if action.isdigit():
                            action = int(action)
                            # Обрабатываем пункт "Назад" или "Выход"
                            if action == 0:
                                if len(self.menuHistory) > 0:
                                    # Возвращаемся на предыдущий уровень
                                    self.currentMenuTitle = self.menuHistory.pop()
                                else:
                                    # Выход из программы
                                    print("Выход из программы")
                                    break
                            elif 1 <= action <= len(activeMenu):
                                # Получаем название выбранного пункта
                                selected_item = activeMenu[action - 1]
                                # Проверяем, не является ли пункт текущим меню
                                if selected_item != self.currentMenuTitle:
                                    # Сохраняем текущее меню в историю для возможности возврата
                                    self.menuHistory.append(self.currentMenuTitle)
                                    self.currentMenuTitle = selected_item
                                else:
                                    print("Вы выбрали тот же пункт. Переход невозможен.")
                            else:
                                print("Некорректный выбор. Введите число в пределах списка.")
                        else:
                            print("Пожалуйста, введите число.")
                    #input("продолжить выполнение программы")
                except KeyboardInterrupt:
                    # Вывести сообщение и предложить пользователю завершить работу
                    print("\nЗавершить программу? (y/n): ", end="")
                    choice = input().strip().lower()
                    if choice == 'y':
                        break
                    else:
                        continue




            # Вывод многоуровневого массива
            #pprint.pprint(menu)

            sys.exit(1)

        finally:
            # Закрытие сессии после завершения
            self.db_manager.close_session(self.session)


if __name__ == "__main__":
    app = Application()
    app.run()
