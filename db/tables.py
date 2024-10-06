from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Базовый класс для декларативного стиля
Base = declarative_base()

# Класс для таблицы SEOData
class SEOData(Base):
    __tablename__ = 'seo_data'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)

# Класс для таблицы пользователей
class UserTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    # Связь с таблицей another_table (один ко многим) с каскадным удалением
    another_data = relationship("AnotherTable", back_populates="user", cascade="all, delete")

# Класс для таблицы AnotherTable
class AnotherTable(Base):
    __tablename__ = 'another_table'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    # Внешний ключ на id из таблицы users с каскадным удалением
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    # Связь с таблицей users (многие к одному)
    user = relationship("UserTable", back_populates="another_data")



"""


# Пример создания нового пользователя и связанных данных
new_user = UserTable(username='john_doe', password='secret', name='John Doe')
another_entry1 = AnotherTable(data='Some data 1', user=new_user)
another_entry2 = AnotherTable(data='Some data 2', user=new_user)

session.add(new_user)
session.add(another_entry1)
session.add(another_entry2)
session.commit()

# Удаление пользователя
user = session.query(UserTable).filter_by(username='john_doe').first()
session.delete(user)
session.commit()

# После этого связанные записи в AnotherTable также будут удалены


"""
