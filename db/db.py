import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .tables import Base, SEOData, AnotherTable, UserTable  # Импортируйте все нужные классы из файла tables

class DatabaseManager:
    data_folder = 'data'
    DB_PATH = data_folder + '/seo_analysis.db'

    @classmethod
    def create_engine_and_db(cls):
        return create_engine(f'sqlite:///{cls.DB_PATH}', echo=False)

    @classmethod
    def initialize_db(cls):
        need_create = False
        if not os.path.exists(cls.DB_PATH):
            answer = input("База данных не найдена. Создать новую базу данных? (y/n): ").strip().lower()
            if answer == 'y':
                need_create = True
            else:
                print("Программа завершена. База данных не была создана.")
                exit()
        if need_create:
            if not os.path.exists(cls.data_folder):
                os.makedirs(cls.data_folder)  # Создаем директорию, если она отсутствует
            engine = cls.create_engine_and_db()
            Base.metadata.create_all(engine)
            print("База данных и таблицы успешно созданы.")

            # Создание сессии и добавление пользователей
            Session = sessionmaker(bind=engine)
            session = Session()

            # Добавляем пользователей в таблицу UserTable
            initial_users = [
                UserTable(username='qwe', password='123', name='Admin'),
            ]
            session.add_all(initial_users)
            session.commit()
            print("Начальные пользователи добавлены в базу данных.")

            cls.close_session(session)

        engine = cls.create_engine_and_db()
        Session = sessionmaker(bind=engine)
        return Session()  # Возвращаем сессию, если база данных уже существует

    @staticmethod
    def close_session(session):
        session.close()
        print("Закрытие сессии")
