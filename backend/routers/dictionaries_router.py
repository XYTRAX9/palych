from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.models import Group, Lesson, Teacher, LessonType, SkillsKnowledge
from database.schemas import (
    GroupResponse,
    LessonResponse,
    TeacherResponse,
    LessonTypeResponse,
    SkillsKnowledgeResponse
)
from database.dependencies import get_main_db

# Создаём роутер для справочников
router = APIRouter(
    prefix="/api/dictionaries",
    tags=["Справочники"]
)


# Получить список всех групп
@router.get("/groups", response_model=list[GroupResponse])
def get_groups(db: Session = Depends(get_main_db)):
    return db.query(Group).all()


# Получить список всех предметов
@router.get("/lessons", response_model=list[LessonResponse])
def get_lessons(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех предметов из справочника.
    """
    return db.query(Lesson).all()


# Получить список всех преподавателей
@router.get("/teachers", response_model=list[TeacherResponse])
def get_teachers(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех преподавателей из справочника.
    """
    return db.query(Teacher).all()


# Получить список всех типов уроков
@router.get("/lesson-types", response_model=list[LessonTypeResponse])
def get_lesson_types(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех типов уроков из справочника.
    """
    return db.query(LessonType).all()


# Получить список знаний и умений
@router.get("/skills-knowledge", response_model=list[SkillsKnowledgeResponse])
def get_skills_knowledge(db: Session = Depends(get_main_db)):
    """
    Возвращает список знаний и умений из справочника.
    """
    return db.query(SkillsKnowledge).all()
