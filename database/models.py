from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Создаём базовый класс для всех моделей (ОДИН РАЗ!)
Base = declarative_base()


# ========== ТАБЛИЦА: group_name (Группы) ==========
class Group(Base):
    __tablename__ = "group_name"

    primary_key = Column(Integer, primary_key=True, index=True)
    curator_group = Column(Text, nullable=True)  # Куратор группы
    group_name = Column(Text, nullable=True)  # Название группы


# ========== ТАБЛИЦА: name_teacher (Преподаватели) ==========
class Teacher(Base):
    __tablename__ = "name_teacher"

    primary_key = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)  # ФИО преподавателя


# ========== ТАБЛИЦА: lesson_type (Типы уроков) ==========
class LessonType(Base):
    __tablename__ = "lesson_type"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson_type = Column(Text, nullable=False)  # Тип урока (лекция, практика и т.д.)


# ========== ТАБЛИЦА: lesson (Предметы с привязками) ==========
# ВАЖНО: Эта таблица связывает предмет, преподавателя, группу и тип урока!
class Lesson(Base):
    __tablename__ = "lesson"

    primary_key = Column(Integer, primary_key=True, index=True)
    name_lesson = Column(Text, nullable=False)  # Название предмета

    # Внешние ключи (связи с другими таблицами)
    Teacher = Column(Integer, ForeignKey("name_teacher.primary_key"), nullable=True)  # ID преподавателя
    Group_name = Column(Integer, ForeignKey("group_name.primary_key"), nullable=True)  # ID группы
    type_lesson = Column(Integer, ForeignKey("lesson_type.primary_key"), nullable=True)  # ID типа урока

    # SQLAlchemy relationship для удобного доступа к связанным объектам
    # Например: lesson.teacher_rel.full_name вместо запроса в БД
    teacher_rel = relationship("Teacher", foreign_keys=[Teacher])
    group_rel = relationship("Group", foreign_keys=[Group_name])
    type_rel = relationship("LessonType", foreign_keys=[type_lesson])


# ========== ТАБЛИЦА: learning_outcomes (Результаты обучения) ==========
# Что студент должен знать и уметь после изучения предмета
class LearningOutcome(Base):
    __tablename__ = "learning_outcomes"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)  # К какому предмету относится
    skill = Column(Text, nullable=True)  # Что должен уметь
    know = Column(Text, nullable=True)  # Что должен знать


# ========== ТАБЛИЦА: lesson_topic (Темы предметов) ==========
# Темы, которые изучаются в рамках предмета
class LessonTopic(Base):
    __tablename__ = "lesson_topic"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)  # К какому предмету относится
    topic = Column(Text, nullable=False)  # Название темы


# ========== ТАБЛИЦА: pk_and_ok (Компетенции) ==========
# Профессиональные (ПК) и общие (ОК) компетенции по предмету
class PkAndOk(Base):
    __tablename__ = "pk_and_ok"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)  # К какому предмету относится
    prof_comp = Column(Text, nullable=True)  # Профессиональные компетенции (ПК)
    general_comp = Column(Text, nullable=True)  # Общие компетенции (ОК)


# ========== ТАБЛИЦА: skills_and_Knowledge (Знания и умения) ==========
# Обновлённая версия таблицы с привязкой к предмету
class SkillsKnowledge(Base):
    __tablename__ = "skills_and_Knowledge"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)  # К какому предмету относится
    skill = Column(Text, nullable=True)  # Умения
    knowledge = Column(Text, nullable=True)  # Знания
