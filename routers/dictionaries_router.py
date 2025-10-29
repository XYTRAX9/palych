from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# ========== ИМПОРТЫ МОДЕЛЕЙ ==========
from database.models import (
    Lesson, Teacher, Group, LessonType, SkillsKnowledge,
    LearningOutcome, LessonTopic, PkAndOk
)

# ========== ИМПОРТЫ СХЕМ ==========
from database.schemas import (
    LessonDetailResponse, LessonExtendedResponse,
    GroupResponse, TeacherResponse, LessonResponse, LessonTypeResponse,
    SkillsKnowledgeResponse, LearningOutcomeResponse, LessonTopicResponse,
    PkAndOkResponse
)

# ========== ИМПОРТЫ ЗАВИСИМОСТЕЙ ==========
from database.dependencies import get_main_db

# ========== СОЗДАНИЕ РОУТЕРА ==========
router = APIRouter(
    prefix="/api",  # Общий префикс для всех ручек
    tags=["Справочники и Фильтрация"]
)


# ==================== РАЗДЕЛ: СПРАВОЧНИКИ ====================

# ========== ПОЛУЧИТЬ ВСЕ ГРУППЫ ==========
@router.get("/dictionaries/groups", response_model=List[GroupResponse])
def get_groups(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех групп из справочника.

    Возвращает:
    - Список групп с ID, названием и куратором
    """
    # Запрашиваем все группы из таблицы group_name
    return db.query(Group).all()


# ========== ПОЛУЧИТЬ ВСЕ ПРЕПОДАВАТЕЛЕЙ ==========
@router.get("/dictionaries/teachers", response_model=List[TeacherResponse])
def get_teachers(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех преподавателей из справочника.

    Возвращает:
    - Список преподавателей с ID и ФИО
    """
    # Запрашиваем всех преподавателей из таблицы name_teacher
    return db.query(Teacher).all()


# ========== ПОЛУЧИТЬ ВСЕ ТИПЫ УРОКОВ ==========
@router.get("/dictionaries/lesson-types", response_model=List[LessonTypeResponse])
def get_lesson_types(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех типов уроков из справочника.

    Возвращает:
    - Список типов уроков (лекция, практика, семинар и т.д.)
    """
    # Запрашиваем все типы уроков из таблицы lesson_type
    return db.query(LessonType).all()


# ========== ПОЛУЧИТЬ ВСЕ ПРЕДМЕТЫ ==========
@router.get("/dictionaries/lessons", response_model=List[LessonResponse])
def get_all_lessons(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех предметов из справочника.

    Возвращает:
    - Список предметов с ID и названием
    """
    # Запрашиваем все предметы из таблицы lesson
    return db.query(Lesson).all()


# ========== ПОЛУЧИТЬ ВСЕ ЗНАНИЯ И УМЕНИЯ ==========
@router.get("/dictionaries/skills-knowledge", response_model=List[SkillsKnowledgeResponse])
def get_skills_knowledge(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех знаний и умений по предметам.

    Возвращает:
    - Список элементов с ID предмета, умениями и знаниями
    """
    # Запрашиваем все записи из таблицы skills_and_Knowledge
    return db.query(SkillsKnowledge).all()


# ========== ПОЛУЧИТЬ РЕЗУЛЬТАТЫ ОБУЧЕНИЯ ==========
@router.get("/dictionaries/learning-outcomes", response_model=List[LearningOutcomeResponse])
def get_learning_outcomes(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех результатов обучения по предметам.

    Возвращает:
    - Список результатов обучения (что студент должен знать и уметь)
    """
    # Запрашиваем все результаты обучения из таблицы learning_outcomes
    return db.query(LearningOutcome).all()


# ========== ПОЛУЧИТЬ ТЕМЫ ПРЕДМЕТОВ ==========
@router.get("/dictionaries/lesson-topics", response_model=List[LessonTopicResponse])
def get_lesson_topics(db: Session = Depends(get_main_db)):
    """
    Возвращает список всех тем по предметам.

    Возвращает:
    - Список тем, которые изучаются в рамках каждого предмета
    """
    # Запрашиваем все темы из таблицы lesson_topic
    return db.query(LessonTopic).all()


# ========== ПОЛУЧИТЬ КОМПЕТЕНЦИИ ==========
@router.get("/dictionaries/pk-and-ok", response_model=List[PkAndOkResponse])
def get_pk_and_ok(db: Session = Depends(get_main_db)):
    """
    Возвращает список профессиональных и общих компетенций по предметам.

    Возвращает:
    - Список компетенций (ПК и ОК) для каждого предмета
    """
    # Запрашиваем все компетенции из таблицы pk_and_ok
    return db.query(PkAndOk).all()


# ==================== РАЗДЕЛ: ФИЛЬТРАЦИЯ ====================

# ========== ПОЛУЧИТЬ ВСЕ ПРЕДМЕТЫ ПРЕПОДАВАТЕЛЯ ==========
@router.get("/filter/lessons/by-teacher/{teacher_id}", response_model=List[LessonDetailResponse])
def get_lessons_by_teacher(teacher_id: int, db: Session = Depends(get_main_db)):
    """
    Возвращает все предметы, которые ведёт указанный преподаватель.

    Параметры:
    - teacher_id (path): ID преподавателя из таблицы name_teacher

    Возвращает:
    - Список предметов этого преподавателя
    """
    # Фильтруем предметы по ID преподавателя
    lessons = db.query(Lesson).filter(Lesson.Teacher == teacher_id).all()
    return lessons


# ========== ПОЛУЧИТЬ ВСЕ ПРЕДМЕТЫ ДЛЯ ГРУППЫ ==========
@router.get("/filter/lessons/by-group/{group_id}", response_model=List[LessonDetailResponse])
def get_lessons_by_group(group_id: int, db: Session = Depends(get_main_db)):
    """
    Возвращает все предметы, которые ведутся в указанной группе.

    Параметры:
    - group_id (path): ID группы из таблицы group_name

    Возвращает:
    - Список предметов для этой группы
    """
    # Фильтруем предметы по ID группы
    lessons = db.query(Lesson).filter(Lesson.Group_name == group_id).all()
    return lessons


# ========== УНИВЕРСАЛЬНАЯ ФИЛЬТРАЦИЯ ПРЕДМЕТОВ ==========
@router.get("/filter/lessons", response_model=List[LessonExtendedResponse])
def filter_lessons(
        teacher_id: Optional[int] = Query(None, description="ID преподавателя для фильтрации"),
        group_id: Optional[int] = Query(None, description="ID группы для фильтрации"),
        lesson_type_id: Optional[int] = Query(None, description="ID типа урока для фильтрации"),
        db: Session = Depends(get_main_db)
):
    """
    Универсальная фильтрация предметов по одному или нескольким параметрам.

    Параметры (все опциональные, можно комбинировать):
    - teacher_id: ID преподавателя
    - group_id: ID группы
    - lesson_type_id: ID типа урока

    Примеры запросов:
    - GET /api/filter/lessons?teacher_id=5 → все предметы преподавателя 5
    - GET /api/filter/lessons?group_id=3 → все предметы группы 3
    - GET /api/filter/lessons?teacher_id=5&group_id=3 → предметы преподавателя 5 для группы 3
    - GET /api/filter/lessons?lesson_type_id=1 → все лекции (или другой тип)

    Возвращает:
    - Список предметов с подробной информацией (имена преподавателей, групп, тип урока)
    """
    # Начинаем с базового запроса к таблице Lesson
    query = db.query(Lesson)

    # Добавляем фильтры, если они указаны
    if teacher_id is not None:
        # Фильтр: только предметы этого преподавателя
        query = query.filter(Lesson.Teacher == teacher_id)

    if group_id is not None:
        # Фильтр: только предметы этой группы
        query = query.filter(Lesson.Group_name == group_id)

    if lesson_type_id is not None:
        # Фильтр: только предметы этого типа урока
        query = query.filter(Lesson.type_lesson == lesson_type_id)

    # Выполняем запрос к БД и получаем результаты
    lessons = query.all()

    # Формируем расширенный ответ с читаемыми названиями
    result = []
    for lesson in lessons:
        # Получаем связанные объекты (преподаватель, группа, тип урока)
        # Используем first() так как нам нужна одна запись, а не все
        teacher = (
            db.query(Teacher).filter(Teacher.primary_key == lesson.Teacher).first()
            if lesson.Teacher else None
        )
        group = (
            db.query(Group).filter(Group.primary_key == lesson.Group_name).first()
            if lesson.Group_name else None
        )
        lesson_type = (
            db.query(LessonType).filter(LessonType.primary_key == lesson.type_lesson).first()
            if lesson.type_lesson else None
        )

        # Формируем ответ с полной информацией
        result.append({
            "primary_key": lesson.primary_key,
            "name_lesson": lesson.name_lesson,
            "teacher_id": lesson.Teacher,
            "teacher_name": teacher.full_name if teacher else None,  # Читаемое ФИО вместо ID
            "group_id": lesson.Group_name,
            "group_name": group.group_name if group else None,  # Читаемое название вместо ID
            "type_lesson_id": lesson.type_lesson,
            "type_lesson_name": lesson_type.lesson_type if lesson_type else None  # Читаемый тип вместо ID
        })

    return result
