import time
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from db.db import SEOData, SitesTable
from menu import MainMenu
from helpers import Helper

class Parser:
    def __init__(self, app):
        self.session = app.session

    #устанавливаем домен сайта для работыzz
    def set_domain(self, app):
        #получение всех сайтов пользователя
        set_site = False
        user_sites = self.session.query(SitesTable).filter(SitesTable.user_id == app.user.user_id).all()
        if user_sites:
            titles = {}
            counter = 1
            for item in user_sites:
                titles[counter] = item.url
                print(str(counter) + " - " + item.url)
                counter += 1
        domain = input("Введите URL сайта или номер из списка: ")
        if domain.isdigit() and int(domain) <= counter and int(domain) > 0:
            if titles[int(domain)]:
                valid_domain = titles[int(domain)]
                set_site = True
        else:
            valid_domain = self.format_url(app, domain)
            if valid_domain:
                check_site = self.session.query(SitesTable).filter(SitesTable.user_id == app.user.user_id, SitesTable.url == domain).one_or_none()
                if check_site:
                    valid_domain = check_site.url
                    set_site = True
                else:
                    seo_entry = SitesTable(
                        user_id=app.user.user_id,
                        url=valid_domain,
                    )
                    try:
                        self.session.add(seo_entry)
                        self.session.commit()
                        set_site = True
                    except Exception as e:
                        self.session.rollback()
        if set_site:
            app.project_domain = valid_domain
            app.menu.update_menu_item_active(app.menu.menu, ["Сбор всех страниц"])
        else:
            Helper.print_message("Домен не установлен!\nВведите корректный адрес сайта!")



    def get_all_pages(self, app):
        print("Анализ CSS начат...")
        time.sleep(2)
        print("Анализ CSS завершён.")

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


    #Проверка домена
    def is_valid_domain(self, domain):
        # Проверка доменного имени на соответствие стандартам (RFC 1035)
        domain_regex = re.compile(
            r'^(?:[a-zA-Z0-9]'  # первая буква/цифра
            r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'  # буквы/цифры/тире и точка
            r'(?:[a-zA-Z]{2,})$'  # домен верхнего уровня (TLD)
        )
        return domain_regex.match(domain) is not None
    #Проверка домена
    def format_url(self, app, url):
        # 1. Проверка на наличие протокола
        if not re.match(r'^(http|https)://', url):
            if app.config['parser']['https_only']=='Y':
                url = 'https://' + url
            else:
                url = 'http://' + url
        # 2. Парсим URL
        parsed_url = urlparse(url)
        # Проверяем валидность домена
        if not self.is_valid_domain(parsed_url.netloc):
            return False
        # Оставляем только схему (протокол) и домен
        formatted_url = f'{parsed_url.scheme}://{parsed_url.netloc}/'
        # 3. Добавляем слэш на конце
        if not formatted_url.endswith('/'):
            formatted_url += '/'
        return formatted_url


    #Парсинг страниц
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

