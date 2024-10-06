from helpers import Helper

class MainMenu:
    def __init__(self, title=None, action=None):
        self.title = title  # Заголовок меню или пункта меню
        self.action = action  # Действие, если элемент — лист
        self.menu = {
                "title": "Главное меню",
                "active": "y",
                "childs": [
                    {
                        "title": "Анализ сайта",
                        "active": "y",
                        "childs": [
                            {
                                "title": "Установить домен",
                                "active": "y",
                                "action": 'app.parser.set_domain(app)',
                            },
                            {
                                "title": "Сбор всех страниц",
                                "active": "n",
                                "action": 'app.parser.get_all_pages(app)',
                            },
                        ]
                    },
                    {
                        "title": "Второй пункт",
                        "active": "n",
                        "childs": [
                            {
                                "title": "Анализ 2",
                                "active": "y",
                                "action": "test()",
                            },
                            {
                                "title": "Сбор 2",
                                "active": "y",
                                "action": "test()",
                            },
                        ]
                    },
                ]
            }


    def showMenu(self, menuTitle="", current_menu=None):
        # Если текущий элемент не задан, используем основное меню
        if current_menu is None:
            #current_menu = self.menu
            return False
        # Проверяем, если текущий элемент имеет искомый заголовок
        #if current_menu.get("title") == menuTitle and current_menu.get("active") == "y":
        if current_menu.get("title") == menuTitle and current_menu.get("active") == "y":
            if "action" in current_menu:
                return current_menu['action']
            titles = []  # Список для хранения заголовков дочерних элементов
            counter = 1
            for item in current_menu.get("childs", []):
                if item["active"] == "y":
                    titles.append(item["title"])  # Добавляем заголовок в список
                    counter += 1
            return titles  # Возвращаем список заголовков
        # Проходим по дочерним элементам и рекурсивно вызываем функцию
        for item in current_menu.get("childs", []):
            if item["active"] == "y":
                active_titles = self.showMenu(menuTitle, item)
                if active_titles:  # Если список заголовков не пустой, возвращаем его
                    return active_titles
        return []  # Возвращаем пустой список, если ничего не найдено


    def update_menu_item_active(self, menu, titles, new_active_value="y"):
        # Проверяем, что titles — это список
        if not isinstance(titles, list):
            raise TypeError("titles должен быть списком, а получен: {}".format(type(titles)))

        # Если titles пустой, возвращаем False
        if not titles:
            return False

        # Проходим по каждому элементу в titles
        for title in titles:
            # Проверяем, если title совпадает с текущим пунктом меню
            if menu.get("title") == title:
                # Обновляем "active" для текущего пункта
                menu["active"] = new_active_value

            # Если есть дочерние элементы, рекурсивно проходим по ним
            if "childs" in menu and isinstance(menu["childs"], list):
                for child in menu["childs"]:
                    self.update_menu_item_active(child, [title], new_active_value)

        return True  # Возвращаем True, если успешно прошли по списку
