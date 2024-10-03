from helpers import Helper

class MainMenu:
    def __init__(self, title=None, action=None):
        self.title = title  # Заголовок меню или пункта меню
        self.action = action  # Действие, если элемент — лист
        self.menu = {
                "title": "Главное меню",
                "childs": [
                    {
                        "title": "Анализ сайта",
                        "childs": [
                            {
                                "title": "Установить домен",
                                "action": "app.helper.test_text",
                            },
                            {
                                "title": "Сбор всех страниц",
                                "action": "test()",
                            },
                        ]
                    },
                    {
                        "title": "Второй пнукт",
                        "childs": [
                            {
                                "title": "Анализ 2",
                                "action": "test()",
                            },
                            {
                                "title": "Сбор 2",
                                "action": "test()",
                            },
                        ]
                    },
                ]
            }


    def showMenu(self, menuTitle="", current_menu=None):
        # Если текущий элемент не задан, используем основное меню
        if current_menu is None:
            current_menu = self.menu
        # Проверяем, если текущий элемент имеет искомый заголовок
        if current_menu.get("title") == menuTitle:
            if "action" in current_menu:
                return current_menu['action']
            titles = []  # Список для хранения заголовков дочерних элементов
            counter = 1
            for item in current_menu.get("childs", []):
                titles.append(item["title"])  # Добавляем заголовок в список
                counter += 1
            return titles  # Возвращаем список заголовков
        # Проходим по дочерним элементам и рекурсивно вызываем функцию
        for item in current_menu.get("childs", []):
            active_titles = self.showMenu(menuTitle, item)
            if active_titles:  # Если список заголовков не пустой, возвращаем его
                return active_titles
        return []  # Возвращаем пустой список, если ничего не найдено



class MenuItem:
    def __init__(self, title, action=None, sub_menu=None):
        self.title = title  # Заголовок меню или пункта меню
        self.action = action  # Действие, если элемент — лист
        self.sub_menu = sub_menu or []  # Список подменю

    def __repr__(self):
        return f"MenuItem(title={self.title}, sub_menu={[item.title for item in self.sub_menu]}, action={self.action})"

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
