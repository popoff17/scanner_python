from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для декларативного стиля
Base = declarative_base()

# Класс для таблицы SEOData
class SEOData(Base):
    __tablename__ = 'seo_data'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)

class UserTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)

# Допустим, вам нужно добавить еще одну таблицу
class AnotherTable(Base):
    __tablename__ = 'another_table'

    id = Column(Integer, primary_key=True)
    data = Column(String)
