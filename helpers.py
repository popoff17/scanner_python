import os
import sys
import time

class Helper:
    def __init__(self):
        pass  # Здесь можно добавить начальные параметры, если они понадобятся

    def set_encoding(self):
        # Установим кодировку
        pass

    def test_text(self):
        print("TEST TEXT")

    def getClassAndMethod(input_string):
        # Разделяем строку по последней точке
        before_dot, separator, after_dot = input_string.rpartition('.')
        # Добавляем скобки к последней части (метод с вызовом)
        after_dot_with_brackets = after_dot
        # Возвращаем список из двух частей
        return [before_dot, after_dot_with_brackets]


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

