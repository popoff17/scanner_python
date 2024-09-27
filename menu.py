from helpers import Helper

class MenuItem:
    def __init__(self, title, action=None, sub_menu=None):
        self.title = title  # Заголовок меню или пункта меню
        self.action = action  # Действие, если элемент — лист
        self.sub_menu = sub_menu or []  # Список подменю

    def is_leaf(self):
        """Проверяет, является ли элемент конечным (листом)."""
        return self.action is not None

    def run(self):
        """Запускает действие, если это лист."""
        if self.is_leaf() and self.action:
            self.action()

class Menu:
    def __init__(self, root_menu):
        self.root_menu = root_menu

    def navigate(self, current_menu, breadcrumb):
        """Выводит меню и возвращает выбор пользователя."""

        # Печатаем навигационную цепочку
        print(" > ".join([item.title for item in breadcrumb]))

        # Печатаем заголовок текущего меню
        print(f"=== {current_menu.title} ===")

        # Печатаем список пунктов меню
        for i, item in enumerate(current_menu.sub_menu, 1):
            print(f"{i}. {item.title}")

        # В главном меню пункт 0 должен быть "Выход", в подменю — "Назад"
        if breadcrumb and current_menu == breadcrumb[0]:
            print("0. Выход")
        else:
            print("0. Назад")

        # Ожидаем выбор пользователя
        choice = input("Выберите действие: ").strip()

        # Обработка ввода
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return 'exit'
            elif 1 <= choice <= len(current_menu.sub_menu):
                return current_menu.sub_menu[choice - 1]

        # Если выбор некорректен, возвращаем None
        return None
