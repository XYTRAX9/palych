import React, { useState, useEffect } from 'react';
import './TechCardForm.css';

const API_BASE_URL = 'http://localhost:8000';

function TechCardForm() {
    const [formData, setFormData] = useState({
        group_id: '',
        lesson_id: '',
        teacher_id: '',
        lesson_type_id: '',
        tema_id: '',
        kafedra_id: '',
        nomer_zanyatiya: '',
        ped_tech: [],
        cel_zanyatiya_id: '',
        zadachi_obuch: '',
        zadachi_razv: '',
        zadachi_vosp: '',
        oborudovanie: '',
        safety_id: '',
        istochniki: '',
        stages: [
            {
                stage_name: 'Актуализация опорных знаний',
                stage_goal: '',
                stage_duration: '',
                teacher_activity: '',
                student_activity: '',
                competencies: ''
            },
            {
                stage_name: 'Сообщение новых знаний',
                stage_goal: '',
                stage_duration: '',
                teacher_activity: '',
                student_activity: '',
                competencies: ''
            },
            {
                stage_name: 'Закрепление знаний',
                stage_goal: '',
                stage_duration: '',
                teacher_activity: '',
                student_activity: '',
                competencies: ''
            },
            {
                stage_name: 'Итог занятия. Домашнее задание',
                stage_goal: '',
                stage_duration: '',
                teacher_activity: '',
                student_activity: '',
                competencies: ''
            }
        ]
    });

    // Справочники из API
    const [groups, setGroups] = useState([]);
    const [lessons, setLessons] = useState([]);
    const [teachers, setTeachers] = useState([]);
    const [lessonTypes, setLessonTypes] = useState([]);
    const [temas, setTemas] = useState([]);
    const [kafedras, setKafedras] = useState([]);
    const [celZanyatiya, setCelZanyatiya] = useState([]);
    const [safetyItems, setSafetyItems] = useState([]);

    // Список доступных педагогических технологий
    const [availablePedTech, setAvailablePedTech] = useState([
        { id: 1, name: 'Проблемное обучение', checked: false },
        { id: 2, name: 'Игровые технологии', checked: false },
        { id: 3, name: 'ИКТ-технологии', checked: false }
    ]);

    const [newPedTech, setNewPedTech] = useState('');

    const [errors, setErrors] = useState({});
    const [warnings, setWarnings] = useState([]);
    const [notification, setNotification] = useState(null);
    const [showWarningsModal, setShowWarningsModal] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDictionaries();
    }, []);

    const loadDictionaries = async () => {
        try {
            setLoading(true);
            const [
                groupsRes,
                lessonsRes,
                teachersRes,
                lessonTypesRes,
                temasRes,
                kafedrasRes,
                celZanyatiyaRes,
                safetyRes
            ] = await Promise.all([
                fetch(`${API_BASE_URL}/api/dictionaries/groups`),
                fetch(`${API_BASE_URL}/api/dictionaries/lessons`),
                fetch(`${API_BASE_URL}/api/dictionaries/teachers`),
                fetch(`${API_BASE_URL}/api/dictionaries/lesson-types`),
                fetch(`${API_BASE_URL}/api/dictionaries/temas`),
                fetch(`${API_BASE_URL}/api/dictionaries/kafedras`),
                fetch(`${API_BASE_URL}/api/dictionaries/cel-zanyatiya`),
                fetch(`${API_BASE_URL}/api/dictionaries/safety`)
            ]);

            if (!groupsRes.ok || !lessonsRes.ok || !teachersRes.ok || !lessonTypesRes.ok ||
                !temasRes.ok || !kafedrasRes.ok || !celZanyatiyaRes.ok || !safetyRes.ok) {
                throw new Error('Ошибка загрузки справочников');
            }

            const groupsData = await groupsRes.json();
            const lessonsData = await lessonsRes.json();
            const teachersData = await teachersRes.json();
            const lessonTypesData = await lessonTypesRes.json();
            const temasData = await temasRes.json();
            const kafedrasData = await kafedrasRes.json();
            const celZanyatiyaData = await celZanyatiyaRes.json();
            const safetyData = await safetyRes.json();

            setGroups(groupsData);
            setLessons(lessonsData);
            setTeachers(teachersData);
            setLessonTypes(lessonTypesData);
            setTemas(temasData);
            setKafedras(kafedrasData);
            setCelZanyatiya(celZanyatiyaData);
            setSafetyItems(safetyData);
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

    // Работа с педагогическими технологиями
    const handlePedTechCheckbox = (id) => {
        setAvailablePedTech(prev =>
            prev.map(tech =>
                tech.id === id ? { ...tech, checked: !tech.checked } : tech
            )
        );

        // Очистка ошибки при выборе технологии
        if (errors.ped_tech) {
            setErrors(prev => ({
                ...prev,
                ped_tech: ''
            }));
        }
    };

    const addNewPedTech = () => {
        if (newPedTech.trim()) {
            const newTech = {
                id: Date.now(),
                name: newPedTech.trim(),
                checked: false
            };
            setAvailablePedTech(prev => [...prev, newTech]);
            setNewPedTech('');

            // Очистка ошибки при добавлении технологии
            if (errors.ped_tech) {
                setErrors(prev => ({
                    ...prev,
                    ped_tech: ''
                }));
            }
        }
    };

    const removePedTech = (id) => {
        setAvailablePedTech(prev => prev.filter(tech => tech.id !== id));
    };

    // Работа с этапами
    const handleStageChange = (index, field, value) => {
        const newStages = [...formData.stages];
        newStages[index] = {
            ...newStages[index],
            [field]: value
        };
        setFormData(prev => ({
            ...prev,
            stages: newStages
        }));
    };

    const addStage = () => {
        setFormData(prev => ({
            ...prev,
            stages: [...prev.stages, {
                stage_name: '',
                stage_goal: '',
                stage_duration: '',
                teacher_activity: '',
                student_activity: '',
                competencies: ''
            }]
        }));
    };

    const removeStage = (index) => {
        if (formData.stages.length > 1) {
            setFormData(prev => ({
                ...prev,
                stages: prev.stages.filter((_, i) => i !== index)
            }));
        }
    };

    // Валидация обязательных полей
    const validateRequiredFields = () => {
        const newErrors = {};

        if (!formData.lesson_id) {
            newErrors.lesson_id = 'Выберите предмет';
        }

        if (!formData.tema_id) {
            newErrors.tema_id = 'Выберите тему';
        }

        if (!formData.kafedra_id) {
            newErrors.kafedra_id = 'Выберите кафедру';
        }

        if (!formData.group_id) {
            newErrors.group_id = 'Выберите группу';
        }

        if (!formData.teacher_id) {
            newErrors.teacher_id = 'Выберите преподавателя';
        }

        if (!formData.lesson_type_id) {
            newErrors.lesson_type_id = 'Выберите тип занятия';
        }

        // Валидация педагогических технологий
        if (availablePedTech.length === 0) {
            newErrors.ped_tech = 'Добавьте хотя бы одну педагогическую технологию';
        } else if (!availablePedTech.some(tech => tech.checked)) {
            newErrors.ped_tech = 'Выберите хотя бы одну педагогическую технологию';
        }

        return newErrors;
    };

    // Проверка необязательных полей
    const checkOptionalFields = () => {
        const emptyFields = [];

        if (!formData.nomer_zanyatiya.trim()) {
            emptyFields.push('Номер занятия по теме');
        }

        if (!formData.cel_zanyatiya_id) {
            emptyFields.push('Цель занятия');
        }

        if (!formData.zadachi_obuch.trim()) {
            emptyFields.push('Обучающие задачи');
        }

        if (!formData.zadachi_razv.trim()) {
            emptyFields.push('Развивающие задачи');
        }

        if (!formData.zadachi_vosp.trim()) {
            emptyFields.push('Воспитательные задачи');
        }

        if (!formData.oborudovanie.trim()) {
            emptyFields.push('Оборудование');
        }

        if (!formData.safety_id) {
            emptyFields.push('Техника безопасности');
        }

        if (!formData.istochniki.trim()) {
            emptyFields.push('Список использованных источников');
        }

        // Проверка этапов
        formData.stages.forEach((stage, index) => {
            if (!stage.stage_name.trim()) {
                emptyFields.push(`Этап ${index + 1}: Название этапа`);
            }
            if (!stage.stage_goal.trim()) {
                emptyFields.push(`Этап ${index + 1}: Цель`);
            }
            if (!stage.stage_duration.trim()) {
                emptyFields.push(`Этап ${index + 1}: Длительность`);
            }
            if (!stage.teacher_activity.trim()) {
                emptyFields.push(`Этап ${index + 1}: Деятельность преподавателя`);
            }
            if (!stage.student_activity.trim()) {
                emptyFields.push(`Этап ${index + 1}: Деятельность обучающихся`);
            }
            if (!stage.competencies.trim()) {
                emptyFields.push(`Этап ${index + 1}: Формируемые компетенции`);
            }
        });

        return emptyFields;
    };

    const showNotification = (type, message) => {
        setNotification({ type, message });
        setTimeout(() => {
            setNotification(null);
        }, 4000);
    };

    const handleSubmit = async () => {
        const validationErrors = validateRequiredFields();

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            showNotification('error', 'Пожалуйста, заполните все обязательные поля');
            return;
        }

        const emptyOptionalFields = checkOptionalFields();

        if (emptyOptionalFields.length > 0) {
            setWarnings(emptyOptionalFields);
            setShowWarningsModal(true);
            return;
        }

        await submitForm();
    };

    const submitForm = async () => {
        try {
            // Подготовка данных для отправки
            const dataToSend = {
                ...formData,
                ped_tech: availablePedTech
                    .filter(tech => tech.checked)
                    .map(tech => tech.name)
                    .join(', ')
            };

            const response = await fetch(`${API_BASE_URL}/api/techcards/1`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend)
            });

            if (!response.ok) {
                throw new Error('Ошибка сохранения технологической карты');
            }

            showNotification('success', 'Документ успешно сгенерирован! Скачивание начнётся через несколько секунд...');

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

            setShowWarningsModal(false);
        } catch (error) {
            console.error('Ошибка:', error);
            showNotification('error', 'Произошла ошибка при генерации документа. Попробуйте снова.');
            setShowWarningsModal(false);
        }
    };

    const handleContinueWithWarnings = () => {
        submitForm();
    };

    const handleCancelSubmit = () => {
        setShowWarningsModal(false);
        setWarnings([]);
    };

    if (loading) {
        return (
            <div className="tech-card-container">
                <div className="tech-card-content">
                    <div className="loading">Загрузка данных...</div>
                </div>
            </div>
        );
    }

    return (
        <div className="tech-card-container">
            {notification && (
                <div className={`notification ${notification.type}`}>
                    {notification.message}
                    <button
                        className="notification-close"
                        onClick={() => setNotification(null)}
                    >
                        ×
                    </button>
                </div>
            )}

            {showWarningsModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>Внимание! Не все поля заполнены</h3>
                        <p>Следующие поля остались пустыми:</p>
                        <ul className="warnings-list">
                            {warnings.map((warning, index) => (
                                <li key={index}>{warning}</li>
                            ))}
                        </ul>
                        <p className="modal-question">Продолжить генерацию документа?</p>
                        <div className="modal-buttons">
                            <button
                                className="modal-btn cancel-btn"
                                onClick={handleCancelSubmit}
                            >
                                Отмена
                            </button>
                            <button
                                className="modal-btn continue-btn"
                                onClick={handleContinueWithWarnings}
                            >
                                Продолжить
                            </button>
                        </div>
                    </div>
                </div>
            )}

            <div className="tech-card-header">
                <h1>Технологическая карта урока</h1>
            </div>

            <div className="tech-card-content">
                <div className="tech-card-form">
                    <table className="tech-card-table">
                        <tbody>
                        {/* Предмет */}
                        <tr>
                            <td className="label-cell">
                                Предмет / МДК <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <select
                                    name="lesson_id"
                                    value={formData.lesson_id}
                                    onChange={handleInputChange}
                                    className={errors.lesson_id ? 'error' : ''}
                                >
                                    <option value="">Выберите предмет</option>
                                    {lessons.map(lesson => (
                                        <option key={lesson.id} value={lesson.id}>
                                            {lesson.name}
                                        </option>
                                    ))}
                                </select>
                                {errors.lesson_id && (
                                    <span className="error-message">{errors.lesson_id}</span>
                                )}
                            </td>
                        </tr>

                        {/* Тема */}
                        <tr>
                            <td className="label-cell">
                                Тема <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <select
                                    name="tema_id"
                                    value={formData.tema_id}
                                    onChange={handleInputChange}
                                    className={errors.tema_id ? 'error' : ''}
                                >
                                    <option value="">Выберите тему</option>
                                    {temas.map(tema => (
                                        <option key={tema.id} value={tema.id}>
                                            {tema.name}
                                        </option>
                                    ))}
                                </select>
                                {errors.tema_id && (
                                    <span className="error-message">{errors.tema_id}</span>
                                )}
                            </td>
                        </tr>

                        {/* Кафедра */}
                        <tr>
                            <td className="label-cell">
                                Кафедра <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <select
                                    name="kafedra_id"
                                    value={formData.kafedra_id}
                                    onChange={handleInputChange}
                                    className={errors.kafedra_id ? 'error' : ''}
                                >
                                    <option value="">Выберите кафедру</option>
                                    {kafedras.map(kafedra => (
                                        <option key={kafedra.id} value={kafedra.id}>
                                            {kafedra.name}
                                        </option>
                                    ))}
                                </select>
                                {errors.kafedra_id && (
                                    <span className="error-message">{errors.kafedra_id}</span>
                                )}
                            </td>
                        </tr>
                        </tbody>
                    </table>

                    <h3 className="section-title">Технологическая карта конструирования учебного занятия</h3>

                    <table className="tech-card-table">
                        <tbody>
                        {/* Группа */}
                        <tr>
                            <td className="label-cell">
                                Предмет, группа <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <select
                                    name="group_id"
                                    value={formData.group_id}
                                    onChange={handleInputChange}
                                    className={errors.group_id ? 'error' : ''}
                                >
                                    <option value="">Выберите группу</option>
                                    {groups.map(group => (
                                        <option key={group.id} value={group.id}>
                                            {group.name}
                                        </option>
                                    ))}
                                </select>
                                {errors.group_id && (
                                    <span className="error-message">{errors.group_id}</span>
                                )}
                            </td>
                        </tr>

                        {/* Номер занятия */}
                        <tr>
                            <td className="label-cell">Тема занятия, № занятия по теме</td>
                            <td className="input-cell">
                                <input
                                    type="text"
                                    name="nomer_zanyatiya"
                                    value={formData.nomer_zanyatiya}
                                    onChange={handleInputChange}
                                    placeholder="Введите номер занятия"
                                />
                            </td>
                        </tr>

                        {/* ФИО преподавателя */}
                        <tr>
                            <td className="label-cell">
                                ФИО преподавателя <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <select
                                    name="teacher_id"
                                    value={formData.teacher_id}
                                    onChange={handleInputChange}
                                    className={errors.teacher_id ? 'error' : ''}
                                >
                                    <option value="">Выберите преподавателя</option>
                                    {teachers.map(teacher => (
                                        <option key={teacher.id} value={teacher.id}>
                                            {teacher.name}
                                        </option>
                                    ))}
                                </select>
                                {errors.teacher_id && (
                                    <span className="error-message">{errors.teacher_id}</span>
                                )}
                            </td>
                        </tr>

                        {/* Тип занятия */}
                        <tr>
                            <td className="label-cell">
                                Тип занятия <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <select
                                    name="lesson_type_id"
                                    value={formData.lesson_type_id}
                                    onChange={handleInputChange}
                                    className={errors.lesson_type_id ? 'error' : ''}
                                >
                                    <option value="">Выберите тип занятия</option>
                                    {lessonTypes.map(type => (
                                        <option key={type.id} value={type.id}>
                                            {type.name}
                                        </option>
                                    ))}
                                </select>
                                {errors.lesson_type_id && (
                                    <span className="error-message">{errors.lesson_type_id}</span>
                                )}
                            </td>
                        </tr>

                        {/* Педагогические технологии */}
                        <tr>
                            <td className="label-cell">
                                Используемые педагогические технологии <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <div className={`ped-tech-container ${errors.ped_tech ? 'error-border' : ''}`}>
                                    {availablePedTech.map((tech) => (
                                        <div key={tech.id} className="checkbox-item">
                                            <label>
                                                <input
                                                    type="checkbox"
                                                    checked={tech.checked}
                                                    onChange={() => handlePedTechCheckbox(tech.id)}
                                                />
                                                <span>{tech.name}</span>
                                            </label>
                                            <button
                                                type="button"
                                                className="checkbox-remove-btn"
                                                onClick={() => removePedTech(tech.id)}
                                                title="Удалить технологию"
                                            >
                                                ×
                                            </button>
                                        </div>
                                    ))}
                                    <div className="add-ped-tech">
                                        <input
                                            type="text"
                                            value={newPedTech}
                                            onChange={(e) => setNewPedTech(e.target.value)}
                                            placeholder="Новая технология"
                                            onKeyPress={(e) => {
                                                if (e.key === 'Enter') {
                                                    e.preventDefault();
                                                    addNewPedTech();
                                                }
                                            }}
                                        />
                                        <button
                                            type="button"
                                            className="add-ped-tech-btn"
                                            onClick={addNewPedTech}
                                        >
                                            Добавить
                                        </button>
                                    </div>
                                </div>
                                {errors.ped_tech && (
                                    <span className="error-message">{errors.ped_tech}</span>
                                )}
                            </td>
                        </tr>

                        {/* Цель занятия */}
                        <tr>
                            <td className="label-cell">Цель занятия</td>
                            <td className="input-cell">
                                <select
                                    name="cel_zanyatiya_id"
                                    value={formData.cel_zanyatiya_id}
                                    onChange={handleInputChange}
                                >
                                    <option value="">Выберите цель занятия</option>
                                    {celZanyatiya.map(cel => (
                                        <option key={cel.id} value={cel.id}>
                                            {cel.name}
                                        </option>
                                    ))}
                                </select>
                            </td>
                        </tr>

                        {/* Задачи */}
                        <tr>
                            <td className="label-cell">Задачи занятия</td>
                            <td className="input-cell">
                                <div className="tasks-grid">
                                    <div className="task-column">
                                        <label>Обучающие</label>
                                        <textarea
                                            name="zadachi_obuch"
                                            value={formData.zadachi_obuch}
                                            onChange={handleInputChange}
                                            placeholder="Введите обучающие задачи"
                                            rows="3"
                                        />
                                    </div>
                                    <div className="task-column">
                                        <label>Развивающие</label>
                                        <textarea
                                            name="zadachi_razv"
                                            value={formData.zadachi_razv}
                                            onChange={handleInputChange}
                                            placeholder="Введите развивающие задачи"
                                            rows="3"
                                        />
                                    </div>
                                    <div className="task-column">
                                        <label>Воспитательные</label>
                                        <textarea
                                            name="zadachi_vosp"
                                            value={formData.zadachi_vosp}
                                            onChange={handleInputChange}
                                            placeholder="Введите воспитательные задачи"
                                            rows="3"
                                        />
                                    </div>
                                </div>
                            </td>
                        </tr>

                        {/* Оборудование */}
                        <tr>
                            <td className="label-cell">Оборудование</td>
                            <td className="input-cell">
                  <textarea
                      name="oborudovanie"
                      value={formData.oborudovanie}
                      onChange={handleInputChange}
                      placeholder="Введите используемое оборудование"
                      rows="2"
                  />
                            </td>
                        </tr>

                        {/* Техника безопасности */}
                        <tr>
                            <td className="label-cell">Техника безопасности</td>
                            <td className="input-cell">
                                <select
                                    name="safety_id"
                                    value={formData.safety_id}
                                    onChange={handleInputChange}
                                >
                                    <option value="">Выберите технику безопасности</option>
                                    {safetyItems.map(safety => (
                                        <option key={safety.id} value={safety.id}>
                                            {safety.name}
                                        </option>
                                    ))}
                                </select>
                            </td>
                        </tr>
                        </tbody>
                    </table>

                    {/* Этапы занятия */}
                    <h3 className="section-title">Организационно-деятельностная структура занятия</h3>

                    {formData.stages.map((stage, index) => (
                        <div key={index} className="stage-block">
                            <div className="stage-header">
                                <h4>Этап {index + 1}</h4>
                                {formData.stages.length > 1 && (
                                    <button
                                        type="button"
                                        className="remove-stage-btn"
                                        onClick={() => removeStage(index)}
                                    >
                                        Удалить этап
                                    </button>
                                )}
                            </div>

                            <table className="tech-card-table stage-table">
                                <tbody>
                                <tr>
                                    <td className="label-cell">Название этапа</td>
                                    <td className="input-cell">
                                        <input
                                            type="text"
                                            value={stage.stage_name}
                                            onChange={(e) => handleStageChange(index, 'stage_name', e.target.value)}
                                            placeholder="Например: Актуализация опорных знаний"
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Цель</td>
                                    <td className="input-cell">
                      <textarea
                          value={stage.stage_goal}
                          onChange={(e) => handleStageChange(index, 'stage_goal', e.target.value)}
                          placeholder="Введите цель этапа"
                          rows="2"
                      />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Длительность этапа</td>
                                    <td className="input-cell">
                                        <input
                                            type="text"
                                            value={stage.stage_duration}
                                            onChange={(e) => handleStageChange(index, 'stage_duration', e.target.value)}
                                            placeholder="Например: 10 минут"
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Деятельность преподавателя</td>
                                    <td className="input-cell">
                      <textarea
                          value={stage.teacher_activity}
                          onChange={(e) => handleStageChange(index, 'teacher_activity', e.target.value)}
                          placeholder="Опишите деятельность преподавателя"
                          rows="3"
                      />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Деятельность обучающихся</td>
                                    <td className="input-cell">
                      <textarea
                          value={stage.student_activity}
                          onChange={(e) => handleStageChange(index, 'student_activity', e.target.value)}
                          placeholder="Опишите деятельность обучающихся"
                          rows="3"
                      />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Формируемые компетенции</td>
                                    <td className="input-cell">
                      <textarea
                          value={stage.competencies}
                          onChange={(e) => handleStageChange(index, 'competencies', e.target.value)}
                          placeholder="Введите формируемые компетенции"
                          rows="2"
                      />
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    ))}

                    <button
                        type="button"
                        className="add-stage-btn"
                        onClick={addStage}
                    >
                        + Добавить этап
                    </button>

                    {/* Источники */}
                    <table className="tech-card-table">
                        <tbody>
                        <tr>
                            <td className="label-cell">Список использованных источников</td>
                            <td className="input-cell">
                  <textarea
                      name="istochniki"
                      value={formData.istochniki}
                      onChange={handleInputChange}
                      placeholder="Введите список источников"
                      rows="3"
                  />
                            </td>
                        </tr>
                        </tbody>
                    </table>

                    <button
                        className="submit-button"
                        onClick={handleSubmit}
                    >
                        Сгенерировать документ
                    </button>
                </div>
            </div>
        </div>
    );
}

export default TechCardForm;
