from pydantic import BaseModel
from typing import Optional, List


# ==================== СХЕМЫ ДЛЯ СПРАВОЧНИКОВ ====================

# ========== СХЕМА ДЛЯ ГРУППЫ ==========
class GroupResponse(BaseModel):
    primary_key: int
    group_name: Optional[str]

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ПРЕПОДАВАТЕЛЯ ==========
class TeacherResponse(BaseModel):
    primary_key: int
    full_name: str

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ТИПА УРОКА ==========
class LessonTypeResponse(BaseModel):
    primary_key: int
    lesson_type: str

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ПРЕДМЕТА ==========
class LessonResponse(BaseModel):
    primary_key: int
    name_lesson: str

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ПРОФЕССИИ ==========
class ProfessionResponse(BaseModel):
    primary_key: int
    profession: Optional[str]

    class Config:
        from_attributes = True


# ==================== КОМПЕТЕНЦИИ ====================

# ========== СХЕМА ДЛЯ ОБЩИХ КОМПЕТЕНЦИЙ (ОК) ==========
class OKResponse(BaseModel):
    primary_key: int
    lesson: Optional[int]  # ИСПРАВЛЕНО: может быть None
    general_comp: Optional[str]

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ПРОФЕССИОНАЛЬНЫХ КОМПЕТЕНЦИЙ (ПК) ==========
class PKResponse(BaseModel):
    primary_key: int
    lesson: Optional[int]  # ИСПРАВЛЕНО: может быть None
    prof_comp: Optional[str]

    class Config:
        from_attributes = True


# ==================== РЕЗУЛЬТАТЫ ОБУЧЕНИЯ ====================

# ========== СХЕМА ДЛЯ РЕЗУЛЬТАТОВ ОБУЧЕНИЯ ==========
class LearningOutcomeResponse(BaseModel):
    primary_key: int
    lesson: Optional[int]  # ИСПРАВЛЕНО: может быть None
    pk: Optional[int]
    ok: Optional[int]
    skills: Optional[int]
    know: Optional[int]

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ТЕМ ПРЕДМЕТА ==========
class LessonTopicResponse(BaseModel):
    primary_key: int
    lesson: Optional[int]  # ИСПРАВЛЕНО: может быть None
    topic: str

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ЗНАНИЙ И УМЕНИЙ ==========
class SkillsKnowledgeResponse(BaseModel):
    primary_key: int
    lesson: Optional[int]  # ИСПРАВЛЕНО: может быть None
    skill: Optional[str]
    knowledge: Optional[str]

    class Config:
        from_attributes = True


# ==================== ПРИЛОЖЕНИЯ ====================

# ========== СХЕМА ДЛЯ ПРИЛОЖЕНИЙ ==========
class ApplicationResponse(BaseModel):
    primary_key: int
    lesson: Optional[int]  # ИСПРАВЛЕНО: может быть None
    name: Optional[str]
    applications_tb: Optional[str]

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ОТДЕЛЕНИЙ ==========
class DepartmentResponse(BaseModel):
    primary_key: int
    teacher: Optional[int]  # может быть None
    departments: Optional[str]

    class Config:
        from_attributes = True


# ==================== СХЕМЫ ДЛЯ ТЕХНОЛОГИЧЕСКОЙ КАРТЫ ====================

# ========== СХЕМА ДЛЯ ДАННЫХ ЭТАПА (ВВОД) ==========
# Используется при создании техкарты (данные от фронтенда)
class TechCardStageData(BaseModel):
    # ВАЖНО: номер и название этапа обязательны
    nomer_etapa: int  # Номер этапа (1, 2, 3 и т.д.)
    nazvanie_etapa: str  # Название этапа (Организационный момент, Актуализация и т.д.)

    # Опциональные поля
    cel_etapa: Optional[str] = None  # Цель этапа
    dlitelnost: Optional[str] = None  # Длительность этапа (в минутах, строка)
    deyatelnost_prepod: Optional[str] = None  # Деятельность преподавателя
    deyatelnost_obuch: Optional[str] = None  # Деятельность обучающихся
    formiruemye_kompetencii: Optional[str] = None  # Формируемые компетенции


# ========== СХЕМА ДЛЯ ОТВЕТА ЭТАПА (ВЫВОД) ==========
# Используется при возврате данных из БД (включает ID)
class TechCardStageResponse(TechCardStageData):
    id: int  # ID этапа в БД
    tech_card_id: int  # ID техкарты, к которой относится этап

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ СОХРАНЕНИЯ/ОБНОВЛЕНИЯ ТЕХКАРТЫ ==========
# Используется при создании или обновлении техкарты (от фронтенда к бэкенду)
class TechCardUpdate(BaseModel):
    # ===== ID из справочников =====
    group_id: Optional[int] = None  # ID группы
    lesson_id: Optional[int] = None  # ID предмета
    teacher_id: Optional[int] = None  # ID преподавателя
    lesson_type_id: Optional[int] = None  # ID типа урока

    # ===== ОСНОВНЫЕ ДАННЫЕ =====
    tema: str  # Тема занятия (ОБЯЗАТЕЛЬНО)
    nomer_zanyatiya: Optional[str] = None  # Номер занятия
    ped_tech: Optional[str] = None  # Педагогические технологии
    cel_zanyatiya: Optional[str] = None  # Цель занятия

    # ===== ЗАДАЧИ ЗАНЯТИЯ =====
    zadachi_obuch: Optional[str] = None  # Обучающие задачи
    zadachi_razv: Optional[str] = None  # Развивающие задачи
    zadachi_vosp: Optional[str] = None  # Воспитательные задачи

    # ===== ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ =====
    prognoz_result: Optional[str] = None  # Прогнозируемый результат
    oborudovanie: Optional[str] = None  # Оборудование
    istochniki: Optional[str] = None  # Источники

    # ===== ЭТАПЫ УРОКА =====
    stages: List[TechCardStageData] = []  # Массив этапов урока


# ========== СХЕМА ДЛЯ ОТВЕТА С ТЕХКАРТОЙ ==========
# Используется при возврате данных из БД (полные данные)
class TechCardResponse(BaseModel):
    # ===== ID ТЕХКАРТЫ =====
    id: int  # ID техкарты в БД

    # ===== ID ИЗ СПРАВОЧНИКОВ =====
    group_id: Optional[int]  # ID группы
    lesson_id: Optional[int]  # ID предмета
    teacher_id: Optional[int]  # ID преподавателя
    lesson_type_id: Optional[int]  # ID типа урока

    # ===== ОСНОВНЫЕ ДАННЫЕ =====
    tema: str  # Тема занятия
    nomer_zanyatiya: Optional[str]  # Номер занятия
    ped_tech: Optional[str]  # Педагогические технологии
    cel_zanyatiya: Optional[str]  # Цель занятия

    # ===== ЗАДАЧИ ЗАНЯТИЯ =====
    zadachi_obuch: Optional[str]  # Обучающие задачи
    zadachi_razv: Optional[str]  # Развивающие задачи
    zadachi_vosp: Optional[str]  # Воспитательные задачи

    # ===== ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ =====
    prognoz_result: Optional[str]  # Прогнозируемый результат
    oborudovanie: Optional[str]  # Оборудование
    istochniki: Optional[str]  # Источники

    # ===== ЭТАПЫ УРОКА =====
    stages: List[TechCardStageResponse] = []  # Массив этапов с ID из БД

    class Config:
        from_attributes = True
