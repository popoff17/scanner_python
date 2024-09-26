from parser import Parser
from helpers import Helper
import requests
from db import DatabaseManager

class MenuItem:
    def __init__(self, name, action=None, sub_menu=None):
        self.name = name
        self.action = action
        self.sub_menu = sub_menu

    def is_leaf(self):
        return self.sub_menu is None

    def run(self):
        if self.is_leaf():
            if self.action:
                self.action()
        else:
            self.show_sub_menu()

    def show_sub_menu(self, breadcrumb):
        Helper.clear_screen()
        print(breadcrumb)  # Выводим навигационную цепочку
        for i, item in enumerate(self.sub_menu):
            print(f"{i + 1}. {item.name}")
        print(f"0. Назад")

class Menu:
    def __init__(self, root_menu, is_root=True, breadcrumb="Главное меню"):
        self.root_menu = root_menu
        self.is_root = is_root
        self.breadcrumb = breadcrumb  # Храним навигационную цепочку

    def navigate(self, session):
        #session = initialize_db()  # Проверяем существование базы данных
        parser = Parser(session)
        while True:
            Helper.clear_screen()
            print(self.breadcrumb)  # Выводим навигационную цепочку
            self.root_menu.show_sub_menu(self.breadcrumb)
            choice = input("Выберите действие: ")

            if choice.isdigit():
                choice = int(choice)
                if choice == 0:
                    if self.is_root:
                        print("Выход.")
                        break
                    else:
                        return
                elif 0 < choice <= len(self.root_menu.sub_menu):
                    selected_item = self.root_menu.sub_menu[choice - 1]
                    if selected_item.is_leaf():
                        selected_item.run()
                    else:
                        # Обновляем навигационную цепочку для подменю
                        submenu = Menu(selected_item, is_root=False, breadcrumb=f"{self.breadcrumb} -> {selected_item.name}")
                        submenu.navigate(session)
                else:
                    print("Неверный выбор.")
            else:
                print("Пожалуйста, введите число.")

    def show_message(self):
        """Пример метода для отображения сообщения."""
        print("Этот метод был вызван!")
        input("Нажмите Enter для продолжения...")
