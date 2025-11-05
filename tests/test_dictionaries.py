# ========== ИМПОРТЫ ==========
import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в sys.path, чтобы можно было импортировать main
# Это нужно, потому что тесты запускаются из папки tests/, а main.py в корне
sys.path.insert(0, str(Path(__file__).parent.parent))

# Теперь импортируем app из main
from main import app
from fastapi.testclient import TestClient

# ========== СОЗДАНИЕ ТЕСТОВОГО КЛИЕНТА ==========
# TestClient позволяет тестировать API без запуска реального сервера
client = TestClient(app)


# ==================== ТЕСТЫ: СПРАВОЧНИКИ ====================

# ========== ТЕСТ: ПОЛУЧИТЬ ВСЕ ГРУППЫ ==========
def test_get_groups():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/groups возвращает список групп

    ПРОВЕРЯЕТ:
    - Статус код 200 (OK)
    - Ответ - это список (array)
    - Каждый элемент имеет поля primary_key и group_name
    """
    # Отправляем GET запрос
    response = client.get("/api/dictionaries/groups")

    # Проверяем статус код
    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"

    # Проверяем, что ответ - список
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    # Если данные есть - проверяем структуру первого элемента
    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "group_name" in data[0], "Отсутствует поле group_name"

    print("✓ test_get_groups пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ВСЕ ПРЕПОДАВАТЕЛЕЙ ==========
def test_get_teachers():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/teachers возвращает список преподавателей

    ПРОВЕРЯЕТ:
    - Статус код 200
    - Ответ - это список
    - Каждый элемент имеет поля primary_key и full_name
    """
    response = client.get("/api/dictionaries/teachers")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "full_name" in data[0], "Отсутствует поле full_name"

    print("✓ test_get_teachers пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ВСЕ ТИПЫ УРОКОВ ==========
def test_get_lesson_types():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/lesson-types возвращает список типов уроков
    """
    response = client.get("/api/dictionaries/lesson-types")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "lesson_type" in data[0], "Отсутствует поле lesson_type"

    print("✓ test_get_lesson_types пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ВСЕ ПРЕДМЕТЫ ==========
def test_get_all_lessons():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/lessons возвращает список предметов
    """
    response = client.get("/api/dictionaries/lessons")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "name_lesson" in data[0], "Отсутствует поле name_lesson"

    print("✓ test_get_all_lessons пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ВСЕ ПРОФЕССИИ ==========
def test_get_professions():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/professions возвращает список профессий
    """
    response = client.get("/api/dictionaries/professions")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    print("✓ test_get_professions пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ВСЕ ОБЩИЕ КОМПЕТЕНЦИИ (ОК) ==========
def test_get_ok():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/ok возвращает список ОК
    """
    response = client.get("/api/dictionaries/ok")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "lesson" in data[0], "Отсутствует поле lesson"
        assert "general_comp" in data[0], "Отсутствует поле general_comp"

    print("✓ test_get_ok пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ВСЕ ПРОФЕССИОНАЛЬНЫЕ КОМПЕТЕНЦИИ (ПК) ==========
def test_get_pk():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/pk возвращает список ПК
    """
    response = client.get("/api/dictionaries/pk")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "lesson" in data[0], "Отсутствует поле lesson"
        assert "prof_comp" in data[0], "Отсутствует поле prof_comp"

    print("✓ test_get_pk пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ РЕЗУЛЬТАТЫ ОБУЧЕНИЯ ==========
def test_get_learning_outcomes():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/learning-outcomes возвращает результаты
    """
    response = client.get("/api/dictionaries/learning-outcomes")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "lesson" in data[0], "Отсутствует поле lesson"

    print("✓ test_get_learning_outcomes пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ТЕМЫ ПРЕДМЕТОВ ==========
def test_get_lesson_topics():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/lesson-topics возвращает темы
    """
    response = client.get("/api/dictionaries/lesson-topics")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "lesson" in data[0], "Отсутствует поле lesson"
        assert "topic" in data[0], "Отсутствует поле topic"

    print("✓ test_get_lesson_topics пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ЗНАНИЯ И УМЕНИЯ ==========
def test_get_skills_knowledge():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/skills-knowledge возвращает данные
    """
    response = client.get("/api/dictionaries/skills-knowledge")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "lesson" in data[0], "Отсутствует поле lesson"
        assert "skill" in data[0], "Отсутствует поле skill"
        assert "knowledge" in data[0], "Отсутствует поле knowledge"

    print("✓ test_get_skills_knowledge пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ПРИЛОЖЕНИЯ ==========
def test_get_applications():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/applications возвращает приложения
    """
    response = client.get("/api/dictionaries/applications")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "lesson" in data[0], "Отсутствует поле lesson"

    print("✓ test_get_applications пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ОТДЕЛЕНИЯ ==========
def test_get_departments():
    """
    НАЗНАЧЕНИЕ: Проверить, что эндпоинт /api/dictionaries/departments возвращает отделения
    """
    response = client.get("/api/dictionaries/departments")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    if len(data) > 0:
        assert "primary_key" in data[0], "Отсутствует поле primary_key"
        assert "teacher" in data[0], "Отсутствует поле teacher"

    print("✓ test_get_departments пройден")


# ==================== ТЕСТЫ: ФИЛЬТРАЦИЯ ====================

# ========== ТЕСТ: ПОЛУЧИТЬ КОМПЕТЕНЦИИ ПО ПРЕДМЕТУ ==========
def test_get_competencies_by_lesson():
    """
    НАЗНАЧЕНИЕ: Проверить фильтрацию компетенций по ID предмета

    ПРОВЕРЯЕТ:
    - Статус код 200
    - Ответ содержит поля ok и pk (массивы)
    """
    # Используем lesson_id = 1 (предполагаем, что такой есть)
    response = client.get("/api/dictionaries/competencies/by-lesson/1")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()

    # Проверяем структуру ответа
    assert "lesson_id" in data, "Отсутствует поле lesson_id"
    assert "ok" in data, "Отсутствует поле ok"
    assert "pk" in data, "Отсутствует поле pk"
    assert isinstance(data["ok"], list), "Поле ok должно быть списком"
    assert isinstance(data["pk"], list), "Поле pk должно быть списком"

    print("✓ test_get_competencies_by_lesson пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ РЕЗУЛЬТАТЫ ОБУЧЕНИЯ ПО ПРЕДМЕТУ ==========
def test_get_learning_outcomes_by_lesson():
    """
    НАЗНАЧЕНИЕ: Проверить фильтрацию результатов обучения по ID предмета
    """
    response = client.get("/api/dictionaries/learning-outcomes/by-lesson/1")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    print("✓ test_get_learning_outcomes_by_lesson пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ТЕМЫ ДЛЯ ПРЕДМЕТА ==========
def test_get_topics_by_lesson():
    """
    НАЗНАЧЕНИЕ: Проверить фильтрацию тем по ID предмета
    """
    response = client.get("/api/dictionaries/lesson-topics/by-lesson/1")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    print("✓ test_get_topics_by_lesson пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ЗНАНИЯ И УМЕНИЯ ПО ПРЕДМЕТУ ==========
def test_get_skills_knowledge_by_lesson():
    """
    НАЗНАЧЕНИЕ: Проверить фильтрацию знаний и умений по ID предмета
    """
    response = client.get("/api/dictionaries/skills-knowledge/by-lesson/1")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    print("✓ test_get_skills_knowledge_by_lesson пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ПРИЛОЖЕНИЯ ПО ПРЕДМЕТУ ==========
def test_get_applications_by_lesson():
    """
    НАЗНАЧЕНИЕ: Проверить фильтрацию приложений по ID предмета
    """
    response = client.get("/api/dictionaries/applications/by-lesson/1")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    print("✓ test_get_applications_by_lesson пройден")


# ========== ТЕСТ: ПОЛУЧИТЬ ОТДЕЛЕНИЯ ПО ПРЕПОДАВАТЕЛЮ ==========
def test_get_departments_by_teacher():
    """
    НАЗНАЧЕНИЕ: Проверить фильтрацию отделений по ID преподавателя
    """
    response = client.get("/api/dictionaries/departments/by-teacher/1")

    assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"

    print("✓ test_get_departments_by_teacher пройден")


# ==================== ЗАПУСК ВСЕХ ТЕСТОВ ====================

# ========== ФУНКЦИЯ ДЛЯ ЗАПУСКА ВРУЧНУЮ ==========
if __name__ == "__main__":
    """
    Запуск всех тестов вручную (без pytest)

    ИСПОЛЬЗОВАНИЕ:
    python tests/test_dictionaries.py
    """
    print("\n" + "=" * 60)
    print("НАЧАЛО ТЕСТИРОВАНИЯ API")
    print("=" * 60 + "\n")

    # Справочники
    print("[СПРАВОЧНИКИ]")
    test_get_groups()
    test_get_teachers()
    test_get_lesson_types()
    test_get_all_lessons()
    test_get_professions()

    print("\n[КОМПЕТЕНЦИИ]")
    test_get_ok()
    test_get_pk()

    print("\n[РЕЗУЛЬТАТЫ ОБУЧЕНИЯ]")
    test_get_learning_outcomes()
    test_get_lesson_topics()
    test_get_skills_knowledge()

    print("\n[ПРИЛОЖЕНИЯ И ОТДЕЛЕНИЯ]")
    test_get_applications()
    test_get_departments()

    print("\n[ФИЛЬТРАЦИЯ]")
    test_get_competencies_by_lesson()
    test_get_learning_outcomes_by_lesson()
    test_get_topics_by_lesson()
    test_get_skills_knowledge_by_lesson()
    test_get_applications_by_lesson()
    test_get_departments_by_teacher()

    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! ✓")
    print("=" * 60 + "\n")
