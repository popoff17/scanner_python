import os
import sys
import time

class Helper:
    def __init__(self):
        pass  # Здесь можно добавить начальные параметры, если они понадобятся

    def set_encoding(self):
        # Установим кодировку
        pass

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
