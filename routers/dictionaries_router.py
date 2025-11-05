from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

# ========== ИМПОРТЫ МОДЕЛЕЙ ==========
from database.models import (
    Lesson, Teacher, Group, LessonType, SkillsKnowledge,
    LearningOutcome, LessonTopic, Profession, OK, PK,
    Application, Department
)

# ========== ИМПОРТЫ СХЕМ ==========
from database.schemas import (
    GroupResponse, TeacherResponse, LessonResponse, LessonTypeResponse,
    ProfessionResponse, OKResponse, PKResponse, LearningOutcomeResponse,
    LessonTopicResponse, SkillsKnowledgeResponse,
    ApplicationResponse, DepartmentResponse
)

# ========== ИМПОРТЫ ЗАВИСИМОСТЕЙ ==========
from database.dependencies import get_main_db

# ========== СОЗДАНИЕ РОУТЕРА ==========
router = APIRouter(
    prefix="/api",
    tags=["Справочники"]
)


# ==================== СПРАВОЧНИКИ: ОСНОВНЫЕ ТАБЛИЦЫ ====================

# ========== ПОЛУЧИТЬ ВСЕ ГРУППЫ ==========
@router.get("/dictionaries/groups", response_model=List[GroupResponse])
def get_groups(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех групп.

    Возвращает:
    - Список групп с ID и названием
    """
    # Запрашиваем все записи из таблицы group_name
    return db.query(Group).all()


# ========== ПОЛУЧИТЬ ВСЕ ПРЕПОДАВАТЕЛЕЙ ==========
@router.get("/dictionaries/teachers", response_model=List[TeacherResponse])
def get_teachers(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех преподавателей.

    Возвращает:
    - Список преподавателей с ID и ФИО
    """
    # Запрашиваем всех преподавателей из таблицы name_teacher
    return db.query(Teacher).all()


# ========== ПОЛУЧИТЬ ВСЕ ТИПЫ УРОКОВ ==========
@router.get("/dictionaries/lesson-types", response_model=List[LessonTypeResponse])
def get_lesson_types(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех типов уроков.

    Возвращает:
    - Список типов уроков (лекция, практика, семинар и т.д.)
    """
    # Запрашиваем все типы уроков из таблицы lesson_type
    return db.query(LessonType).all()


# ========== ПОЛУЧИТЬ ВСЕ ПРЕДМЕТЫ ==========
@router.get("/dictionaries/lessons", response_model=List[LessonResponse])
def get_all_lessons(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех предметов.

    Возвращает:
    - Список предметов с ID и названием
    """
    # Запрашиваем все предметы из таблицы lesson
    return db.query(Lesson).all()


# ========== ПОЛУЧИТЬ ВСЕ ПРОФЕССИИ ==========
@router.get("/dictionaries/professions", response_model=List[ProfessionResponse])
def get_professions(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех профессий/специальностей.

    Возвращает:
    - Список профессий с ID и названием
    """
    # Запрашиваем все профессии из таблицы profession
    return db.query(Profession).all()


# ==================== КОМПЕТЕНЦИИ ====================

# ========== ПОЛУЧИТЬ ВСЕ ОБЩИЕ КОМПЕТЕНЦИИ (ОК) ==========
@router.get("/dictionaries/ok", response_model=List[OKResponse])
def get_ok(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех общих компетенций (ОК).

    Возвращает:
    - Список общих компетенций с ID предмета и текстом компетенции
    """
    # Запрашиваем все общие компетенции из таблицы ok
    return db.query(OK).all()


# ========== ПОЛУЧИТЬ ВСЕ ПРОФЕССИОНАЛЬНЫЕ КОМПЕТЕНЦИИ (ПК) ==========
@router.get("/dictionaries/pk", response_model=List[PKResponse])
def get_pk(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех профессиональных компетенций (ПК).

    Возвращает:
    - Список профессиональных компетенций с ID предмета и текстом компетенции
    """
    # Запрашиваем все профессиональные компетенции из таблицы pk
    return db.query(PK).all()


# ========== ПОЛУЧИТЬ КОМПЕТЕНЦИИ ПО ПРЕДМЕТУ ==========
@router.get("/dictionaries/competencies/by-lesson/{lesson_id}")
def get_competencies_by_lesson(lesson_id: int, db: Session = Depends(get_main_db)):
    """
    Возвращает все компетенции (ОК и ПК) для конкретного предмета.

    Параметры:
    - lesson_id: ID предмета

    Возвращает:
    - Объект с двумя массивами: ok и pk
    """
    # Получаем общие компетенции для этого предмета
    ok_list = db.query(OK).filter(OK.lesson == lesson_id).all()

    # Получаем профессиональные компетенции для этого предмета
    pk_list = db.query(PK).filter(PK.lesson == lesson_id).all()

    # Возвращаем структурированный ответ
    return {
        "lesson_id": lesson_id,
        "ok": ok_list,
        "pk": pk_list
    }


# ==================== РЕЗУЛЬТАТЫ ОБУЧЕНИЯ И ЗНАНИЯ ====================

# ========== ПОЛУЧИТЬ РЕЗУЛЬТАТЫ ОБУЧЕНИЯ ==========
@router.get("/dictionaries/learning-outcomes", response_model=List[LearningOutcomeResponse])
def get_learning_outcomes(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех результатов обучения.

    Возвращает:
    - Список результатов обучения (связь предмета с компетенциями и умениями)
    """
    # Запрашиваем все результаты обучения из таблицы learning_outcomes
    return db.query(LearningOutcome).all()


# ========== ПОЛУЧИТЬ РЕЗУЛЬТАТЫ ОБУЧЕНИЯ ПО ПРЕДМЕТУ ==========
@router.get("/dictionaries/learning-outcomes/by-lesson/{lesson_id}", response_model=List[LearningOutcomeResponse])
def get_learning_outcomes_by_lesson(lesson_id: int, db: Session = Depends(get_main_db)):
    """
    Возвращает все результаты обучения для конкретного предмета.

    Параметры:
    - lesson_id: ID предмета

    Возвращает:
    - Список результатов обучения для этого предмета
    """
    # Фильтруем результаты обучения по ID предмета
    return db.query(LearningOutcome).filter(LearningOutcome.lesson == lesson_id).all()


# ========== ПОЛУЧИТЬ ТЕМЫ ПРЕДМЕТОВ ==========
@router.get("/dictionaries/lesson-topics", response_model=List[LessonTopicResponse])
def get_lesson_topics(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех тем по предметам.

    Возвращает:
    - Список тем с ID предмета и названием темы
    """
    # Запрашиваем все темы из таблицы lesson_topic
    return db.query(LessonTopic).all()


# ========== ПОЛУЧИТЬ ТЕМЫ ДЛЯ КОНКРЕТНОГО ПРЕДМЕТА ==========
@router.get("/dictionaries/lesson-topics/by-lesson/{lesson_id}", response_model=List[LessonTopicResponse])
def get_topics_by_lesson(lesson_id: int, db: Session = Depends(get_main_db)):
    """
    Возвращает все темы для конкретного предмета.

    Параметры:
    - lesson_id: ID предмета

    Возвращает:
    - Список тем этого предмета
    """
    # Фильтруем темы по ID предмета
    return db.query(LessonTopic).filter(LessonTopic.lesson == lesson_id).all()


# ========== ПОЛУЧИТЬ ЗНАНИЯ И УМЕНИЯ ==========
@router.get("/dictionaries/skills-knowledge", response_model=List[SkillsKnowledgeResponse])
def get_skills_knowledge(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех знаний и умений.

    Возвращает:
    - Список знаний и умений с привязкой к предметам
    """
    # Запрашиваем все записи из таблицы skills_and_Knowledge
    return db.query(SkillsKnowledge).all()


# ========== ПОЛУЧИТЬ ЗНАНИЯ И УМЕНИЯ ПО ПРЕДМЕТУ ==========
@router.get("/dictionaries/skills-knowledge/by-lesson/{lesson_id}", response_model=List[SkillsKnowledgeResponse])
def get_skills_knowledge_by_lesson(lesson_id: int, db: Session = Depends(get_main_db)):
    """
    Возвращает знания и умения для конкретного предмета.

    Параметры:
    - lesson_id: ID предмета

    Возвращает:
    - Список знаний и умений этого предмета
    """
    # Фильтруем знания и умения по ID предмета
    return db.query(SkillsKnowledge).filter(SkillsKnowledge.lesson == lesson_id).all()


# ==================== ПРИЛОЖЕНИЯ ====================

# ========== ПОЛУЧИТЬ ВСЕ ПРИЛОЖЕНИЯ - ИСПРАВЛЕНО! ==========
@router.get("/dictionaries/applications", response_model=List[ApplicationResponse])
def get_applications(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех приложений к урокам.

    ВАЖНО: Автоматически преобразуем пустые строки в None,
    чтобы избежать ошибок валидации Pydantic.

    Возвращает:
    - Список приложений с привязкой к предметам
    """
    # Запрашиваем все приложения из таблицы applications
    applications = db.query(Application).all()

    # Преобразуем пустые строки в None для валидации Pydantic
    # Это нужно, потому что в БД может быть пустая строка '' вместо NULL
    for app in applications:
        # Если lesson - пустая строка, меняем на None
        if app.lesson == '':
            app.lesson = None

    return applications


# ========== ПОЛУЧИТЬ ПРИЛОЖЕНИЯ ПО ПРЕДМЕТУ ==========
@router.get("/dictionaries/applications/by-lesson/{lesson_id}", response_model=List[ApplicationResponse])
def get_applications_by_lesson(lesson_id: int, db: Session = Depends(get_main_db)):
    """
    Возвращает все приложения для конкретного предмета.

    Параметры:
    - lesson_id: ID предмета

    Возвращает:
    - Список приложений этого предмета
    """
    # Фильтруем приложения по ID предмета
    # Исключаем пустые строки из фильтра
    applications = db.query(Application).filter(
        or_(
            Application.lesson == lesson_id,
            Application.lesson == str(lesson_id)  # На случай, если это строка
        )
    ).all()

    # Преобразуем пустые строки в None для валидации
    for app in applications:
        if app.lesson == '':
            app.lesson = None

    return applications


# ==================== ОТДЕЛЕНИЯ ====================

# ========== ПОЛУЧИТЬ ВСЕ ОТДЕЛЕНИЯ ==========
@router.get("/dictionaries/departments", response_model=List[DepartmentResponse])
def get_departments(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех отделений/кафедр.

    Возвращает:
    - Список отделений с привязкой к преподавателям
    """
    # Запрашиваем все отделения из таблицы departments
    return db.query(Department).all()


# ========== ПОЛУЧИТЬ ОТДЕЛЕНИЯ ПО ПРЕПОДАВАТЕЛЮ ==========
@router.get("/dictionaries/departments/by-teacher/{teacher_id}", response_model=List[DepartmentResponse])
def get_departments_by_teacher(teacher_id: int, db: Session = Depends(get_main_db)):
    """
    Возвращает все отделения преподавателя.

    Параметры:
    - teacher_id: ID преподавателя

    Возвращает:
    - Список отделений этого преподавателя
    """
    # Фильтруем отделения по ID преподавателя
    return db.query(Department).filter(Department.teacher == teacher_id).all()
