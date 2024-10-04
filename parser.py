import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from db.db import SEOData
from menu import MainMenu


class Parser:
    def __init__(self, session):
        self.session = session

    def set_domain(self, app, project_domain=""):
        print("устанавливаем сайт...")
        app.project_domain = project_domain
        print("сайт установлен.")
        menuActive = ["Сбор всех страниц"]
        app.menu.update_menu_item_active(app.menu.menu, menuActive)


    def analyze_css(self):
        print("Анализ CSS начат...")
        time.sleep(2)
        print("Анализ CSS завершён.")

    def analyze_js(self):
        print("Анализ JS начат...")
        time.sleep(2)
        print("Анализ JS завершён.")

    def process_site(self):
        print("Обрабатываем сайт полностью...")
        time.sleep(3)
        print("Обработка завершена.")

    def save_to_sqlalchemy(self, data):
        seo_entry = SEOData(
            url=data['url'],
            title=data['title'],
        )
        try:
            self.session.add(seo_entry)
            self.session.commit()
            print("Данные успешно сохранены в SQLite через SQLAlchemy")
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при сохранении данных: {e}")

    def is_internal_link(self, base_url, link):
        return urlparse(link).netloc == urlparse(base_url).netloc

    def url_exists(self, url):
        return session.query(SEOData).filter_by(url=url).first() is not None

    def scrape_page(self, url, depth=2, visited=set()):
        if depth < 0 or url in visited:
            return  # Прекращаем рекурсию, если глубина меньше 0 или URL уже посещен

        visited.add(url)  # Добавляем URL в множество посещенных

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Собираем основную информацию о странице
            data = {
                'url': url,
                'title': soup.title.string if soup.title else None,
            }

            # Проверяем, существует ли URL в базе, если нет, сохраняем
            if not self.url_exists(url):
                self.save_to_sqlalchemy(data)  # Сохраняем данные через SQLAlchemy
            else:
                print(f"URL {url} уже существует в базе данных.")

            # Если глубина больше 0, продолжаем парсинг по внутренним ссылкам
            if depth > 0:
                links = []
                for a in soup.find_all('a', href=True):
                    full_url = urljoin(url, a['href'])
                    if self.is_internal_link(url, full_url):  # Проверяем, является ли ссылка внутренней
                        links.append(full_url)

                for link in links:
                    self.scrape_page(link, depth - 1, visited)  # Передаем множество посещенных ссылок

        except Exception as e:
            print(f"Ошибка при обработке {url}: {e}")

    def set_page(self):
        url = input("Введите URL сайта: ")
        self.scrape_page(url)  # Запускаем парсинг для введённого URL
