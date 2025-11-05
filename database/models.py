from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# ========== СОЗДАНИЕ БАЗОВОГО КЛАССА ==========
Base = declarative_base()


# ==================== СПРАВОЧНИКИ ====================

# ========== ТАБЛИЦА: group_name (Группы) ==========
class Group(Base):
    __tablename__ = "group_name"

    primary_key = Column(Integer, primary_key=True, index=True)
    group_name = Column(Text, nullable=True)


# ========== ТАБЛИЦА: name_teacher (Преподаватели) ==========
class Teacher(Base):
    __tablename__ = "name_teacher"

    primary_key = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)


# ========== ТАБЛИЦА: lesson_type (Типы уроков) ==========
class LessonType(Base):
    __tablename__ = "lesson_type"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson_type = Column(Text, nullable=False)


# ========== ТАБЛИЦА: lesson (Предметы) ==========
class Lesson(Base):
    __tablename__ = "lesson"

    primary_key = Column(Integer, primary_key=True, index=True)
    name_lesson = Column(Text, nullable=False)


# ========== ТАБЛИЦА: profession (Профессии) ==========
class Profession(Base):
    __tablename__ = "profession"

    primary_key = Column(Integer, primary_key=True, index=True)
    profession = Column(Text, nullable=True)


# ==================== КОМПЕТЕНЦИИ ====================

# ========== ТАБЛИЦА: ok (Общие компетенции) ==========
class OK(Base):
    __tablename__ = "ok"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)
    general_comp = Column(Text, nullable=True)


# ========== ТАБЛИЦА: pk (Профессиональные компетенции) ==========
class PK(Base):
    __tablename__ = "pk"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)
    prof_comp = Column(Text, nullable=True)


# ==================== РЕЗУЛЬТАТЫ ОБУЧЕНИЯ И ЗНАНИЯ ====================

# ========== ТАБЛИЦА: learning_outcomes ==========
class LearningOutcome(Base):
    __tablename__ = "learning_outcomes"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)
    pk = Column(Integer, ForeignKey("pk.primary_key"), nullable=True)
    ok = Column(Integer, ForeignKey("ok.primary_key"), nullable=True)
    skills = Column(Integer, nullable=True)
    know = Column(Integer, nullable=True)


# ========== ТАБЛИЦА: lesson_topic ==========
class LessonTopic(Base):
    __tablename__ = "lesson_topic"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)
    topic = Column(Text, nullable=False)


# ========== ТАБЛИЦА: skills_and_Knowledge ==========
class SkillsKnowledge(Base):
    __tablename__ = "skills_and_Knowledge"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=False)
    skill = Column(Text, nullable=True)
    knowledge = Column(Text, nullable=True)


# ==================== ПРИЛОЖЕНИЯ ====================

# ========== ТАБЛИЦА: applications ==========
class Application(Base):
    __tablename__ = "applications"

    primary_key = Column(Integer, primary_key=True, index=True)
    lesson = Column(Integer, ForeignKey("lesson.primary_key"), nullable=True)  # ВАЖНО: nullable=True!
    name = Column(Text, nullable=True)
    applications_tb = Column(Text, nullable=True)


# ==================== ОТДЕЛЕНИЯ ====================

# ========== ТАБЛИЦА: departments ==========
class Department(Base):
    __tablename__ = "departments"

    primary_key = Column(Integer, primary_key=True, index=True)
    teacher = Column(Integer, ForeignKey("name_teacher.primary_key"), nullable=False)
    departments = Column(Text, nullable=True)
