from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from database.models import Base
from database.models_techcard import BaseTechCard

# Создаём приложение FastAPI
app = FastAPI()

# Настройка CORS для работы с React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретный адрес React-приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Получаем абсолютный путь к папке database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')

# ========== ПОДКЛЮЧЕНИЕ К ОСНОВНОЙ БД (databaseforbros.db) ==========
main_db_path = os.path.join(DATABASE_DIR, 'databaseforbros.db')
engine_main = create_engine(f'sqlite:///{main_db_path}', echo=True)
SessionMainDB = sessionmaker(bind=engine_main)

# ========== ПОДКЛЮЧЕНИЕ К БД ТЕХКАРТ (techcards.db) ==========
techcard_db_path = os.path.join(DATABASE_DIR, 'techcards.db')
engine_techcard = create_engine(f'sqlite:///{techcard_db_path}', echo=True)
SessionTechCardDB = sessionmaker(bind=engine_techcard)

# Создаём таблицы в БД техкарт (если их ещё нет)
BaseTechCard.metadata.create_all(bind=engine_techcard)


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


# ========== ТЕСТОВЫЙ ENDPOINT ==========
@app.get("/")
async def root():
    return {"message": "API для генератора технологических карт работает!"}