from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Таблица "group_name" - Группы
class Group(Base):
    __tablename__ = "group_name"

    primary_key = Column(Integer, primary_key=True, index=True)
    curator_group = Column(Text, nullable=True)  # Куратор группы
    group_name = Column(Text, nullable=True)  # Название группы


# Таблица "lesson" - Предметы
class Lesson(Base):
    __tablename__ = "lesson"

    primary_key = Column(Integer, primary_key=True, index=True)
    name_lesson = Column(Text, nullable=False)  # Название предмета


# Таблица "lesson_type" - Типы уроков
class LessonType(Base):
    __tablename__ = "lesson_type"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson_type = Column(Text, nullable=False)  # Тип урока


# Таблица "name_teacher" - ФИО преподавателей
class Teacher(Base):
    __tablename__ = "name_teacher"

    primary_key = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)  # ФИО преподавателя


# Таблица "skills_and_Knowledge" - Знания и умения
class SkillsKnowledge(Base):
    __tablename__ = "skills_and_Knowledge"

    primary_key = Column(Integer, primary_key=True, index=True)
    skill = Column(Text, nullable=True)  # Умения
    knowledge = Column(Text, nullable=True)  # Знания