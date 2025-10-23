from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Получаем абсолютный путь к папке database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')

# ========== ПОДКЛЮЧЕНИЕ К ОСНОВНОЙ БД (databaseforbros.db) ==========
main_db_path = os.path.join(DATABASE_DIR, 'databaseforbros.db')
engine_main = create_engine(f'sqlite:///{main_db_path}', echo=True)
SessionMainDB = sessionmaker(bind=engine_main)

# ========== ПОДКЛЮЧЕНИЕ К БД ТЕХКАРТ (techcards.db) ==========
techcard_db_path = os.path.join(DATABASE_DIR, 'techcards.db')
engine_techcard = create_engine(f'sqlite:///{techcard_db_path}', echo=True)
SessionTechCardDB = sessionmaker(bind=engine_techcard)


# ========== ФУНКЦИИ ДЛЯ ПОЛУЧЕНИЯ СЕССИЙ БД ==========

# Получение сессии основной БД
async def get_main_db():
    db = SessionMainDB()
    try:
        yield db
    finally:
        db.close()


# Получение сессии БД техкарт
async def get_techcard_db():
    db = SessionTechCardDB()
    try:
        yield db
    finally:
        db.close()
