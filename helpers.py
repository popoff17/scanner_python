import os
import sys
import time
import re

class Helper:
    def __init__(self):
        pass  # Здесь можно добавить начальные параметры, если они понадобятся

    def set_encoding(self):
        # Установим кодировку
        pass

    def test_text(self):
        print("TEST TEXT")

    def print_message(message, error_title="ОШИБКА!"):
        continue_message = "Нажмите ENTER для продолжения"
        padding = 2  # Отступы по бокам от текста
        # Разбиваем сообщение на строки по символам переноса \n
        message_lines = message.split('\n')
        # Определяем максимальную длину строки, включая отступы
        max_length = max(
            len(error_title),
            max(len(line) for line in message_lines),  # Длина самой длинной строки в сообщении
            len(continue_message)
        ) + padding * 2
        # Строим рамку
        border = "#" * (max_length + 4)  # По 2 символа на каждую сторону для отступов
        empty_line = f"# {' ' * max_length} #"
        title_line = f"# {' ' * padding}{error_title.center(max_length - padding * 2)}{' ' * padding} #"
        # Строим линии сообщения
        message_lines = [f"# {' ' * padding}{line.ljust(max_length - padding * 2)}{' ' * padding} #" for line in message_lines]
        continue_line = f"# {' ' * padding}{continue_message.center(max_length - padding * 2)}{' ' * padding} #"
        # Печатаем результат
        print(border)
        print(empty_line)
        print(title_line)
        for line in message_lines:
            print(line)
        print(empty_line)
        print(continue_line)
        print(border)
        input()



    def getClassAndMethod(input_string):
        # Разделяем строку по последней точке
        before_dot, separator, after_dot = input_string.rpartition('.')
        # Регулярное выражение для поиска имени метода и аргументов в скобках
        match = re.match(r"(\w+)\((.*)\)", after_dot)
        if match:
            method_name = match.group(1)  # Имя метода
            method_args = match.group(2)  # Аргументы внутри скобок
        else:
            method_name = after_dot
            method_args = ""  # Если аргументов нет, возвращаем пустую строку
        return [before_dot, method_name, method_args]
        # Пример использования
        #result = getClassAndMethod("app.helper.test_method('arg1', 2)")
        #print(result)  # ['app.helper', 'test_method', "'arg1', 2"]



    @staticmethod
    def clear_screen():
        """Очищает экран, в зависимости от операционной системы."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def format_url(self, url):
        """Форматирует URL. Если URL не начинается с http, добавляет префикс http://"""
        return url if url.startswith('http') else f'http://{url}'

    def progress_bar(self, seconds):
        """Выводит прогресс-бар в консоли на указанное количество секунд."""
        for i in range(seconds):
            time.sleep(1)
            progress = int((i + 1) / seconds * 100)
            sys.stdout.write(f"\rПрогресс: {progress}%")
            sys.stdout.flush()
        print("\nПрогресс: 100% Завершено.")

    @staticmethod
    def print_nested_array(arr, level=0):
        for item in arr:
            if isinstance(item, list):
                print("  " * level + "[")
                Helper.print_nested_array(item, level + 1)  # Вызов статического метода
                print("  " * level + "]")
            else:
                print("  " * level + str(item))

