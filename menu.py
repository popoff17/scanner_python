from helpers import Helper

class MenuItem:
    def __init__(self, name, action=None, sub_menu=None):
        self.name = name
        self.action = action
        self.sub_menu = sub_menu

    def is_leaf(self):
        """Проверка, является ли элемент конечным."""
        return self.sub_menu is None

    def run(self):
        """Запуск действия, если элемент конечный."""
        if self.is_leaf():
            if self.action:
                self.action()
        else:
            print("Это не конечный элемент, невозможно запустить действие.")

    def show_sub_menu(self, breadcrumb):
        """Отображение подменю."""
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
        """Навигация по меню."""
        while True:
            Helper.clear_screen()
            print(self.breadcrumb)  # Выводим навигационную цепочку
            self.root_menu.show_sub_menu(self.breadcrumb)  # Показываем подменю
            choice = input("Выберите действие: ")

            if choice.isdigit():
                choice = int(choice)
                if choice == 0:
                    if self.is_root:
                        print("Выход.")
                        return "exit"  # Возвращаем команду для выхода
                    else:
                        return
                elif 0 < choice <= len(self.root_menu.sub_menu):
                    selected_item = self.root_menu.sub_menu[choice - 1]
                    if selected_item.is_leaf():
                        selected_item.run()
                    else:
                        # Создаем подменю
                        submenu = Menu(selected_item, is_root=False, breadcrumb=f"{self.breadcrumb} -> {selected_item.name}")
                        submenu.navigate(session)
                else:
                    print("Неверный выбор.")
                    input("Нажмите Enter для продолжения.")
            else:
                print("Пожалуйста, введите число.")
                input("Нажмите Enter для продолжения.")

    def show_message(self):
        """Пример метода для отображения сообщения."""
        print("Этот метод был вызван!")
        input("Нажмите Enter для продолжения...")
