import React, { useState, useEffect } from 'react';
import './TechCardForm.css';

const API_BASE_URL = 'http://localhost:8000';

function TechCardForm() {
    const [formData, setFormData] = useState({
        group_id: '',
        lesson_id: '',
        teacher_id: '',
        lesson_type_id: '',
        tema: '',
        nomer_zanyatiya: '',
        ped_tech: '',
        cel_zanyatiya: '',
        zadachi_obuch: '',
        zadachi_razv: '',
        zadachi_vosp: '',
        prognoz_result: '',
        oborudovanie: '',
        istochniki: '',
        stages: []
    });

    // Справочники
    const [groups, setGroups] = useState([]);
    const [lessons, setLessons] = useState([]);
    const [teachers, setTeachers] = useState([]);
    const [lessonTypes, setLessonTypes] = useState([]);

    const [errors, setErrors] = useState({});
    const [notification, setNotification] = useState(null);
    const [loading, setLoading] = useState(true);

    // Загрузка справочников при монтировании компонента
    useEffect(() => {
        loadDictionaries();
    }, []);

    const loadDictionaries = async () => {
        try {
            setLoading(true);

            const [groupsRes, lessonsRes, teachersRes, lessonTypesRes] = await Promise.all([
                fetch(`${API_BASE_URL}/api/dictionaries/groups`),
                fetch(`${API_BASE_URL}/api/dictionaries/lessons`),
                fetch(`${API_BASE_URL}/api/dictionaries/teachers`),
                fetch(`${API_BASE_URL}/api/dictionaries/lesson-types`)
            ]);

            if (!groupsRes.ok || !lessonsRes.ok || !teachersRes.ok || !lessonTypesRes.ok) {
                throw new Error('Ошибка загрузки справочников');
            }

            const groupsData = await groupsRes.json();
            const lessonsData = await lessonsRes.json();
            const teachersData = await teachersRes.json();
            const lessonTypesData = await lessonTypesRes.json();

            setGroups(groupsData);
            setLessons(lessonsData);
            setTeachers(teachersData);
            setLessonTypes(lessonTypesData);

            setLoading(false);
        } catch (error) {
            console.error('Ошибка загрузки справочников:', error);
            showNotification('error', 'Не удалось загрузить данные из базы. Проверьте подключение к серверу.');
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const validateForm = () => {
        const newErrors = {};

        if (!formData.tema.trim()) {
            newErrors.tema = 'Поле "Тема занятия" обязательно для заполнения';
        } else if (formData.tema.trim().length < 3) {
            newErrors.tema = 'Тема занятия должна содержать минимум 3 символа';
        }

        if (!formData.group_id) {
            newErrors.group_id = 'Выберите группу';
        }

        if (!formData.lesson_id) {
            newErrors.lesson_id = 'Выберите предмет';
        }

        if (!formData.teacher_id) {
            newErrors.teacher_id = 'Выберите преподавателя';
        }

        if (!formData.lesson_type_id) {
            newErrors.lesson_type_id = 'Выберите тип урока';
        }

        return newErrors;
    };

    const showNotification = (type, message) => {
        setNotification({ type, message });
        setTimeout(() => {
            setNotification(null);
        }, 4000);
    };

    const handleSubmit = async () => {
        const validationErrors = validateForm();

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            showNotification('error', 'Пожалуйста, заполните все обязательные поля');
            return;
        }

        try {
            // Сохраняем техкарту (используем ID=1 для обновления существующей)
            const response = await fetch(`${API_BASE_URL}/api/techcards/1`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Ошибка сохранения технологической карты');
            }

            showNotification('success', 'Документ успешно сгенерирован! Скачивание начнётся через несколько секунд...');

            // Запускаем скачивание файла через 2 секунды
            setTimeout(async () => {
                try {
                    const downloadResponse = await fetch(`${API_BASE_URL}/api/techcards/download`);

                    if (!downloadResponse.ok) {
                        throw new Error('Ошибка скачивания файла');
                    }

                    const blob = await downloadResponse.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'tekhnologicheskaya_karta.docx';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                } catch (error) {
                    console.error('Ошибка скачивания:', error);
                    showNotification('error', 'Ошибка при скачивании документа');
                }
            }, 2000);

        } catch (error) {
            console.error('Ошибка:', error);
            showNotification('error', 'Произошла ошибка при генерации документа. Попробуйте снова.');
        }
    };

    if (loading) {
        return (
            <div className="tech-card-container">
                <header className="tech-card-header">
                    <h1>ГЕНЕРАТОР ТЕХНОЛОГИЧЕСКОЙ КАРТЫ УРОКА</h1>
                </header>
                <div className="tech-card-content">
                    <div className="tech-card-form">
                        <p style={{ textAlign: 'center', fontSize: '16px', color: '#666' }}>
                            Загрузка данных...
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="tech-card-container">
            {notification && (
                <div className={`notification ${notification.type}`}>
                    <span>{notification.message}</span>
                    <button
                        className="notification-close"
                        onClick={() => setNotification(null)}
                    >
                        ×
                    </button>
                </div>
            )}

            <header className="tech-card-header">
                <h1>ГЕНЕРАТОР ТЕХНОЛОГИЧЕСКОЙ КАРТЫ УРОКА</h1>
            </header>

            <div className="tech-card-content">
                <div className="tech-card-form">
                    <div className="form-group">
                        <label>Группа *</label>
                        <select
                            name="group_id"
                            value={formData.group_id}
                            onChange={handleInputChange}
                            className={errors.group_id ? 'error' : ''}
                        >
                            <option value="">Выберите группу</option>
                            {groups.map(group => (
                                <option key={group.primary_key} value={group.primary_key}>
                                    {group.group_name}
                                </option>
                            ))}
                        </select>
                        {errors.group_id && <span className="error-message">{errors.group_id}</span>}
                    </div>

                    <div className="form-group">
                        <label>Предмет *</label>
                        <select
                            name="lesson_id"
                            value={formData.lesson_id}
                            onChange={handleInputChange}
                            className={errors.lesson_id ? 'error' : ''}
                        >
                            <option value="">Выберите предмет</option>
                            {lessons.map(lesson => (
                                <option key={lesson.primary_key} value={lesson.primary_key}>
                                    {lesson.name_lesson}
                                </option>
                            ))}
                        </select>
                        {errors.lesson_id && <span className="error-message">{errors.lesson_id}</span>}
                    </div>

                    <div className="form-group">
                        <label>Преподаватель *</label>
                        <select
                            name="teacher_id"
                            value={formData.teacher_id}
                            onChange={handleInputChange}
                            className={errors.teacher_id ? 'error' : ''}
                        >
                            <option value="">Выберите преподавателя</option>
                            {teachers.map(teacher => (
                                <option key={teacher.primary_key} value={teacher.primary_key}>
                                    {teacher.full_name}
                                </option>
                            ))}
                        </select>
                        {errors.teacher_id && <span className="error-message">{errors.teacher_id}</span>}
                    </div>

                    <div className="form-group">
                        <label>Тип урока *</label>
                        <select
                            name="lesson_type_id"
                            value={formData.lesson_type_id}
                            onChange={handleInputChange}
                            className={errors.lesson_type_id ? 'error' : ''}
                        >
                            <option value="">Выберите тип урока</option>
                            {lessonTypes.map(type => (
                                <option key={type.primary_key} value={type.primary_key}>
                                    {type.lesson_type}
                                </option>
                            ))}
                        </select>
                        {errors.lesson_type_id && <span className="error-message">{errors.lesson_type_id}</span>}
                    </div>

                    <div className="form-group">
                        <label>Тема занятия *</label>
                        <input
                            type="text"
                            name="tema"
                            value={formData.tema}
                            onChange={handleInputChange}
                            placeholder="Введите тему занятия"
                            className={errors.tema ? 'error' : ''}
                        />
                        {errors.tema && <span className="error-message">{errors.tema}</span>}
                    </div>

                    <div className="form-group">
                        <label>Номер занятия по теме</label>
                        <input
                            type="text"
                            name="nomer_zanyatiya"
                            value={formData.nomer_zanyatiya}
                            onChange={handleInputChange}
                            placeholder="Например: 1"
                        />
                    </div>

                    <div className="form-group">
                        <label>Педагогические технологии</label>
                        <input
                            type="text"
                            name="ped_tech"
                            value={formData.ped_tech}
                            onChange={handleInputChange}
                            placeholder="Укажите используемые технологии"
                        />
                    </div>

                    <div className="form-group">
                        <label>Цель занятия</label>
                        <input
                            type="text"
                            name="cel_zanyatiya"
                            value={formData.cel_zanyatiya}
                            onChange={handleInputChange}
                            placeholder="Введите цель занятия"
                        />
                    </div>

                    <div className="form-group">
                        <label>Обучающие задачи</label>
                        <input
                            type="text"
                            name="zadachi_obuch"
                            value={formData.zadachi_obuch}
                            onChange={handleInputChange}
                            placeholder="Обучающие задачи"
                        />
                    </div>

                    <div className="form-group">
                        <label>Развивающие задачи</label>
                        <input
                            type="text"
                            name="zadachi_razv"
                            value={formData.zadachi_razv}
                            onChange={handleInputChange}
                            placeholder="Развивающие задачи"
                        />
                    </div>

                    <div className="form-group">
                        <label>Воспитательные задачи</label>
                        <input
                            type="text"
                            name="zadachi_vosp"
                            value={formData.zadachi_vosp}
                            onChange={handleInputChange}
                            placeholder="Воспитательные задачи"
                        />
                    </div>

                    <div className="form-group">
                        <label>Прогнозируемый результат</label>
                        <input
                            type="text"
                            name="prognoz_result"
                            value={formData.prognoz_result}
                            onChange={handleInputChange}
                            placeholder="Знания, умения, компетенции"
                        />
                    </div>

                    <div className="form-group">
                        <label>Оборудование</label>
                        <input
                            type="text"
                            name="oborudovanie"
                            value={formData.oborudovanie}
                            onChange={handleInputChange}
                            placeholder="Перечислите оборудование"
                        />
                    </div>

                    <div className="form-group">
                        <label>Список источников</label>
                        <input
                            type="text"
                            name="istochniki"
                            value={formData.istochniki}
                            onChange={handleInputChange}
                            placeholder="Список использованных источников"
                        />
                    </div>

                    <button onClick={handleSubmit} className="submit-button">
                        Сгенерировать технологическую карту
                    </button>
                </div>
            </div>
        </div>
    );
}

export default TechCardForm;