from pydantic import BaseModel
from typing import Optional, List


# ==================== СХЕМЫ ДЛЯ СПРАВОЧНИКОВ ====================

# ========== СХЕМА ДЛЯ ГРУППЫ ==========
class GroupResponse(BaseModel):
    primary_key: int  # ID группы
    curator_group: Optional[str]  # Куратор группы (может быть пустым)
    group_name: Optional[str]  # Название группы (может быть пустым)

    class Config:
        from_attributes = True  # Позволяет создавать из SQLAlchemy-моделей


# ========== СХЕМА ДЛЯ ПРЕПОДАВАТЕЛЯ ==========
class TeacherResponse(BaseModel):
    primary_key: int  # ID преподавателя
    full_name: str  # ФИО преподавателя

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ТИПА УРОКА ==========
class LessonTypeResponse(BaseModel):
    primary_key: int  # ID типа урока
    lesson_type: str  # Тип урока (лекция, практика и т.д.)

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ПРЕДМЕТА (ПРОСТАЯ) ==========
class LessonResponse(BaseModel):
    primary_key: int  # ID предмета
    name_lesson: str  # Название предмета

    class Config:
        from_attributes = True


# ==================== СХЕМЫ ДЛЯ ПРЕДМЕТОВ С ПОДРОБНОСТЯМИ ====================

# ========== СХЕМА ДЛЯ ПРЕДМЕТА С СВЯЗЯМИ (ID) ==========
# Используется, когда нужно вернуть предмет со всеми связями (ID преподавателя, группы и т.д.)
class LessonDetailResponse(BaseModel):
    primary_key: int  # ID предмета
    name_lesson: str  # Название предмета
    Teacher: Optional[int]  # ID преподавателя (может быть пустым)
    Group_name: Optional[int]  # ID группы (может быть пустым)
    type_lesson: Optional[int]  # ID типа урока (может быть пустым)

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ РАСШИРЕННОГО ОТВЕТА С ИМЕНАМИ ==========
# Используется, когда нужно вернуть не только ID, но и читаемые названия
class LessonExtendedResponse(BaseModel):
    primary_key: int  # ID предмета
    name_lesson: str  # Название предмета
    teacher_id: Optional[int]  # ID преподавателя
    teacher_name: Optional[str]  # ФИО преподавателя (читаемое имя)
    group_id: Optional[int]  # ID группы
    group_name: Optional[str]  # Название группы (читаемое название)
    type_lesson_id: Optional[int]  # ID типа урока
    type_lesson_name: Optional[str]  # Название типа урока (читаемое название)

    class Config:
        from_attributes = True


# ==================== СХЕМЫ ДЛЯ НОВЫХ ТАБЛИЦ ====================

# ========== СХЕМА ДЛЯ РЕЗУЛЬТАТОВ ОБУЧЕНИЯ ==========
# ВАЖНО: поле lesson теперь Optional[int], так как в БД могут быть старые записи с NULL
class LearningOutcomeResponse(BaseModel):
    primary_key: int  # ID записи
    lesson: Optional[int]  # ID предмета (может быть None для старых записей)
    skill: Optional[str]  # Что должен уметь студент
    know: Optional[str]  # Что должен знать студент

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ТЕМ ПРЕДМЕТА ==========
# ВАЖНО: поле lesson теперь Optional[int], так как в БД могут быть старые записи с NULL
class LessonTopicResponse(BaseModel):
    primary_key: int  # ID записи
    lesson: Optional[int]  # ID предмета (может быть None для старых записей)
    topic: str  # Название темы

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ КОМПЕТЕНЦИЙ ==========
# ВАЖНО: поле lesson теперь Optional[int], так как в БД могут быть старые записи с NULL
class PkAndOkResponse(BaseModel):
    primary_key: int  # ID записи
    lesson: Optional[int]  # ID предмета (может быть None для старых записей)
    prof_comp: Optional[str]  # Профессиональные компетенции (ПК)
    general_comp: Optional[str]  # Общие компетенции (ОК)

    class Config:
        from_attributes = True


# ========== СХЕМА ДЛЯ ЗНАНИЙ И УМЕНИЙ (ОБНОВЛЁННАЯ) ==========
# ВАЖНО: поле lesson теперь Optional[int], так как в БД могут быть старые записи с NULL
class SkillsKnowledgeResponse(BaseModel):
    primary_key: int  # ID записи
    lesson: Optional[int]  # ID предмета (может быть None для старых записей)
    skill: Optional[str]  # Умения
    knowledge: Optional[str]  # Знания

    class Config:
        from_attributes = True


# ==================== СХЕМЫ ДЛЯ ЭТАПОВ УРОКА ====================

# ========== СХЕМА ДЛЯ ЭТАПА УРОКА (ВВОД ДАННЫХ) ==========
# Используется при создании техкарты (передача данных от фронтенда)
class TechCardStageData(BaseModel):
    nomer_etapa: int  # Номер этапа
    nazvanie_etapa: str  # Название этапа
    cel_etapa: Optional[str] = None  # Цель этапа
    dlitelnost: Optional[str] = None  # Длительность этапа
    deyatelnost_prepod: Optional[str] = None  # Деятельность преподавателя
    deyatelnost_obuch: Optional[str] = None  # Деятельность обучающихся
    formiruemye_kompetencii: Optional[str] = None  # Формируемые компетенции


# ========== СХЕМА ДЛЯ ОТВЕТА С ЭТАПОМ УРОКА ==========
# Используется при возврате данных из БД (включает ID из базы)
class TechCardStageResponse(TechCardStageData):
    id: int  # ID этапа в БД
    tech_card_id: int  # ID техкарты, к которой относится этап

    class Config:
        from_attributes = True


# ==================== СХЕМЫ ДЛЯ ТЕХНОЛОГИЧЕСКОЙ КАРТЫ ====================

# ========== СХЕМА ДЛЯ СОХРАНЕНИЯ/ОБНОВЛЕНИЯ ТЕХКАРТЫ ==========
# Используется при создании или обновлении техкарты (от фронтенда к бэкенду)
class TechCardUpdate(BaseModel):
    # ===== ID из справочников (связи с другими таблицами) =====
    group_id: Optional[int] = None  # ID группы
    lesson_id: Optional[int] = None  # ID предмета
    teacher_id: Optional[int] = None  # ID преподавателя
    lesson_type_id: Optional[int] = None  # ID типа урока

    # ===== Данные, вводимые вручную =====
    tema: str  # Тема занятия (обязательное поле)
    nomer_zanyatiya: Optional[str] = None  # Номер занятия
    ped_tech: Optional[str] = None  # Педагогические технологии
    cel_zanyatiya: Optional[str] = None  # Цель занятия

    # ===== Задачи занятия =====
    zadachi_obuch: Optional[str] = None  # Обучающие задачи
    zadachi_razv: Optional[str] = None  # Развивающие задачи
    zadachi_vosp: Optional[str] = None  # Воспитательные задачи

    # ===== Дополнительная информация =====
    prognoz_result: Optional[str] = None  # Прогнозируемый результат
    oborudovanie: Optional[str] = None  # Оборудование
    istochniki: Optional[str] = None  # Источники

    # ===== Список этапов урока =====
    stages: List[TechCardStageData] = []  # Этапы урока (массив объектов)


# ========== СХЕМА ДЛЯ ОТВЕТА С ТЕХКАРТОЙ ==========
# Используется при возврате данных из БД (полные данные техкарты)
class TechCardResponse(BaseModel):
    id: int  # ID техкарты в БД

    # ===== ID из справочников =====
    group_id: Optional[int]  # ID группы
    lesson_id: Optional[int]  # ID предмета
    teacher_id: Optional[int]  # ID преподавателя
    lesson_type_id: Optional[int]  # ID типа урока

    # ===== Данные техкарты =====
    tema: str  # Тема занятия
    nomer_zanyatiya: Optional[str]  # Номер занятия
    ped_tech: Optional[str]  # Педагогические технологии
    cel_zanyatiya: Optional[str]  # Цель занятия

    # ===== Задачи =====
    zadachi_obuch: Optional[str]  # Обучающие задачи
    zadachi_razv: Optional[str]  # Развивающие задачи
    zadachi_vosp: Optional[str]  # Воспитательные задачи

    # ===== Дополнительная информация =====
    prognoz_result: Optional[str]  # Прогнозируемый результат
    oborudovanie: Optional[str]  # Оборудование
    istochniki: Optional[str]  # Источники

    # ===== Список этапов урока =====
    stages: List[TechCardStageResponse] = []  # Этапы урока (с ID из БД)

    class Config:
        from_attributes = True
