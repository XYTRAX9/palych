import React, { useState, useEffect } from 'react';
import './TechCardForm.css';

const API_BASE_URL = "/api";

function TechCardForm() {
    // ТОЛЬКО ИСПРАВЛЕНИЕ СВЯЗЕЙ - всё остальное как было
    const [formData, setFormData] = useState({
        group_id: '',
        lesson_id: '',
        teacher_id: '',
        lesson_type_id: '',
        tema: '', // ✅ ИСПРАВЛЕНО: была tema_id
        nomer_zanyatiya: '',
        ped_tech: [], // Остаётся массив как было
        cel_zanyatiya: '', // ✅ ИСПРАВЛЕНО: была cel_zanyatiya_id
        zadachi_obuch: '',
        zadachi_razv: '',
        zadachi_vosp: '',
        oborudovanie: '',
        istochniki: '',
        stages: [
            {
                nomer_etapa: 1,
                nazvanie_etapa: 'Актуализация опорных знаний',
                cel_etapa: '', // ✅ ИСПРАВЛЕНО: было stage_goal
                dlitelnost: '', // ✅ ИСПРАВЛЕНО: было stage_duration
                deyatelnost_prepod: '', // ✅ ИСПРАВЛЕНО: было teacher_activity
                deyatelnost_obuch: '', // ✅ ИСПРАВЛЕНО: было student_activity
                formiruemye_kompetencii: '' // ✅ ИСПРАВЛЕНО: было competencies
            },
            {
                nomer_etapa: 2,
                nazvanie_etapa: 'Сообщение новых знаний',
                cel_etapa: '',
                dlitelnost: '',
                deyatelnost_prepod: '',
                deyatelnost_obuch: '',
                formiruemye_kompetencii: ''
            },
            {
                nomer_etapa: 3,
                nazvanie_etapa: 'Закрепление знаний',
                cel_etapa: '',
                dlitelnost: '',
                deyatelnost_prepod: '',
                deyatelnost_obuch: '',
                formiruemye_kompetencii: ''
            },
            {
                nomer_etapa: 4,
                nazvanie_etapa: 'Итог занятия. Домашнее задание',
                cel_etapa: '',
                dlitelnost: '',
                deyatelnost_prepod: '',
                deyatelnost_obuch: '',
                formiruemye_kompetencii: ''
            }
        ]
    });

    // Справочники - ТОЛЬКО 5 реальных (удалены temas, kafedras, cel_zanyatiya, safety)
    const [groups, setGroups] = useState([]);
    const [lessons, setLessons] = useState([]);
    const [teachers, setTeachers] = useState([]);
    const [lessonTypes, setLessonTypes] = useState([]);
    const [skillsKnowledge, setSkillsKnowledge] = useState([]);

    // Педагогические технологии - как было
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

    // ИСПРАВЛЕНИЕ: Загружаем только 5 реальных эндпоинтов
    const loadDictionaries = async () => {
        try {
            setLoading(true);
            const [
                groupsRes,
                lessonsRes,
                teachersRes,
                lessonTypesRes,
                skillsKnowledgeRes
            ] = await Promise.all([
                fetch(`${API_BASE_URL}/api/dictionaries/groups`),
                fetch(`${API_BASE_URL}/api/dictionaries/lessons`),
                fetch(`${API_BASE_URL}/api/dictionaries/teachers`),
                fetch(`${API_BASE_URL}/api/dictionaries/lesson-types`),
                fetch(`${API_BASE_URL}/api/dictionaries/skills-knowledge`)
            ]);

            // Проверяем ответы
            if (
                !groupsRes.ok ||
                !lessonsRes.ok ||
                !teachersRes.ok ||
                !lessonTypesRes.ok ||
                !skillsKnowledgeRes.ok
            ) {
                throw new Error('Ошибка загрузки справочников');
            }

            // Получаем данные
            const groupsData = await groupsRes.json();
            const lessonsData = await lessonsRes.json();
            const teachersData = await teachersRes.json();
            const lessonTypesData = await lessonTypesRes.json();
            const skillsKnowledgeData = await skillsKnowledgeRes.json();

            setGroups(groupsData);
            setLessons(lessonsData);
            setTeachers(teachersData);
            setLessonTypes(lessonTypesData);
            setSkillsKnowledge(skillsKnowledgeData);
            setLoading(false);
        } catch (error) {
            console.error('Ошибка загрузки справочников:', error);
            setNotification({
                type: 'error',
                message: 'Не удалось загрузить данные из базы. Проверьте подключение к серверу.'
            });
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

    // Работа с педагогическими технологиями - как было
    const handlePedTechCheckbox = (id) => {
        setAvailablePedTech(prev =>
            prev.map(tech =>
                tech.id === id ? { ...tech, checked: !tech.checked } : tech
            )
        );
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

    // Работа с этапами - ИСПРАВЛЕНЫ НАЗВАНИЯ ПОЛЕЙ
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
        const newStageNumber = formData.stages.length + 1;
        setFormData(prev => ({
            ...prev,
            stages: [
                ...prev.stages,
                {
                    nomer_etapa: newStageNumber,
                    nazvanie_etapa: '',
                    cel_etapa: '',
                    dlitelnost: '',
                    deyatelnost_prepod: '',
                    deyatelnost_obuch: '',
                    formiruemye_kompetencii: ''
                }
            ]
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

    // Валидация - ИСПРАВЛЕНО: tema вместо tema_id, cel_zanyatiya вместо cel_zanyatiya_id
    const validateRequiredFields = () => {
        const newErrors = {};

        if (!formData.lesson_id) {
            newErrors.lesson_id = 'Выберите предмет';
        }
        if (!formData.tema) { // ✅ ИСПРАВЛЕНО
            newErrors.tema = 'Введите тему занятия';
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
        if (!formData.cel_zanyatiya.trim()) { // ✅ ИСПРАВЛЕНО
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
        if (!formData.istochniki.trim()) {
            emptyFields.push('Список использованных источников');
        }

        // Проверка этапов - ИСПРАВЛЕНЫ НАЗВАНИЯ ПОЛЕЙ
        formData.stages.forEach((stage, index) => {
            if (!stage.nazvanie_etapa.trim()) {
                emptyFields.push(`Этап ${index + 1}: Название этапа`);
            }
            if (!stage.cel_etapa.trim()) { // ✅ ИСПРАВЛЕНО
                emptyFields.push(`Этап ${index + 1}: Цель`);
            }
            if (!stage.dlitelnost.trim()) { // ✅ ИСПРАВЛЕНО
                emptyFields.push(`Этап ${index + 1}: Длительность`);
            }
            if (!stage.deyatelnost_prepod.trim()) { // ✅ ИСПРАВЛЕНО
                emptyFields.push(`Этап ${index + 1}: Деятельность преподавателя`);
            }
            if (!stage.deyatelnost_obuch.trim()) { // ✅ ИСПРАВЛЕНО
                emptyFields.push(`Этап ${index + 1}: Деятельность обучающихся`);
            }
            if (!stage.formiruemye_kompetencii.trim()) { // ✅ ИСПРАВЛЕНО
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
            // Подготовка данных - ИСПРАВЛЕНО: названия полей для backend
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
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            });

            if (!response.ok) {
                throw new Error('Ошибка сохранения технологической карты');
            }

            showNotification(
                'success',
                'Документ успешно сгенерирован! Скачивание начнётся через несколько секунд...'
            );

            setTimeout(async () => {
                try {
                    const downloadResponse = await fetch(
                        `${API_BASE_URL}/api/techcards/download`
                    );

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
            showNotification(
                'error',
                'Произошла ошибка при генерации документа. Попробуйте снова.'
            );
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
        return <div className="loading">Загрузка справочников...</div>;
    }

    return (
        <div className="tech-card-container">
            <div className="tech-card-header">
                <h1>Генератор технологической карты урока</h1>
            </div>

            {notification && (
                <div className={`notification notification-${notification.type}`}>
                    {notification.message}
                </div>
            )}

            <div className="tech-card-content">
                <div className="tech-card-form">
                    {/* ОСНОВНЫЕ ДАННЫЕ */}
                    <h2 className="section-title">Основные данные</h2>
                    <table className="tech-card-table">
                        <tbody>
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
                                    <option value="">-- Выберите предмет --</option>
                                    {lessons.map(lesson => (
                                        <option key={lesson.primary_key} value={lesson.primary_key}>
                                            {lesson.name_lesson}
                                        </option>
                                    ))}
                                </select>
                                {errors.lesson_id && (
                                    <span className="error-message">{errors.lesson_id}</span>
                                )}
                            </td>
                        </tr>
                        <tr>
                            <td className="label-cell">
                                Тема <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <input
                                    type="text"
                                    name="tema"
                                    value={formData.tema}
                                    onChange={handleInputChange}
                                    placeholder="Введите тему занятия"
                                    className={errors.tema ? 'error' : ''}
                                />
                                {errors.tema && (
                                    <span className="error-message">{errors.tema}</span>
                                )}
                            </td>
                        </tr>
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
                                    <option value="">-- Выберите группу --</option>
                                    {groups.map(group => (
                                        <option key={group.primary_key} value={group.primary_key}>
                                            {group.group_name}
                                        </option>
                                    ))}
                                </select>
                                {errors.group_id && (
                                    <span className="error-message">{errors.group_id}</span>
                                )}
                            </td>
                        </tr>
                        <tr>
                            <td className="label-cell">
                                Тема занятия, № занятия по теме
                            </td>
                            <td className="input-cell">
                                <input
                                    type="text"
                                    name="nomer_zanyatiya"
                                    value={formData.nomer_zanyatiya}
                                    onChange={handleInputChange}
                                    placeholder="Например: 1/5"
                                />
                            </td>
                        </tr>
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
                                    <option value="">-- Выберите преподавателя --</option>
                                    {teachers.map(teacher => (
                                        <option key={teacher.primary_key} value={teacher.primary_key}>
                                            {teacher.full_name}
                                        </option>
                                    ))}
                                </select>
                                {errors.teacher_id && (
                                    <span className="error-message">{errors.teacher_id}</span>
                                )}
                            </td>
                        </tr>
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
                                    <option value="">-- Выберите тип занятия --</option>
                                    {lessonTypes.map(type => (
                                        <option key={type.primary_key} value={type.primary_key}>
                                            {type.lesson_type}
                                        </option>
                                    ))}
                                </select>
                                {errors.lesson_type_id && (
                                    <span className="error-message">{errors.lesson_type_id}</span>
                                )}
                            </td>
                        </tr>
                        <tr>
                            <td className="label-cell">
                                Используемые педагогические технологии{' '}
                                <span className="required-mark">*</span>
                            </td>
                            <td className="input-cell">
                                <div
                                    className={`ped-tech-container ${
                                        errors.ped_tech ? 'error-border' : ''
                                    }`}
                                >
                                    {availablePedTech.map(tech => (
                                        <div key={tech.id} className="checkbox-item">
                                            <label>
                                                <input
                                                    type="checkbox"
                                                    checked={tech.checked}
                                                    onChange={() => handlePedTechCheckbox(tech.id)}
                                                />
                                                <span>{tech.name}</span>
                                            </label>
                                            {tech.id > 3 && (
                                                <button
                                                    type="button"
                                                    className="checkbox-remove-btn"
                                                    onClick={() => removePedTech(tech.id)}
                                                >
                                                    ×
                                                </button>
                                            )}
                                        </div>
                                    ))}
                                </div>
                                {errors.ped_tech && (
                                    <span className="error-message">{errors.ped_tech}</span>
                                )}
                                <div className="add-ped-tech">
                                    <input
                                        type="text"
                                        value={newPedTech}
                                        onChange={e => setNewPedTech(e.target.value)}
                                        placeholder="Новая технология"
                                        onKeyPress={e => {
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
                            </td>
                        </tr>
                        <tr>
                            <td className="label-cell">Цель занятия</td>
                            <td className="input-cell">
                  <textarea
                      name="cel_zanyatiya"
                      value={formData.cel_zanyatiya}
                      onChange={handleInputChange}
                      placeholder="Введите цель занятия"
                  />
                            </td>
                        </tr>
                        </tbody>
                    </table>

                    {/* ЗАДАЧИ ЗАНЯТИЯ */}
                    <h2 className="section-title">Задачи занятия</h2>
                    <div className="tasks-grid">
                        <div className="task-column">
                            <label>Обучающие задачи</label>
                            <textarea
                                name="zadachi_obuch"
                                value={formData.zadachi_obuch}
                                onChange={handleInputChange}
                                placeholder="Введите обучающие задачи"
                            />
                        </div>
                        <div className="task-column">
                            <label>Развивающие задачи</label>
                            <textarea
                                name="zadachi_razv"
                                value={formData.zadachi_razv}
                                onChange={handleInputChange}
                                placeholder="Введите развивающие задачи"
                            />
                        </div>
                        <div className="task-column">
                            <label>Воспитательные задачи</label>
                            <textarea
                                name="zadachi_vosp"
                                value={formData.zadachi_vosp}
                                onChange={handleInputChange}
                                placeholder="Введите воспитательные задачи"
                            />
                        </div>
                    </div>

                    {/* ОБОРУДОВАНИЕ И ИСТОЧНИКИ */}
                    <h2 className="section-title">Материально-техническое обеспечение</h2>
                    <table className="tech-card-table">
                        <tbody>
                        <tr>
                            <td className="label-cell">Оборудование</td>
                            <td className="input-cell">
                  <textarea
                      name="oborudovanie"
                      value={formData.oborudovanie}
                      onChange={handleInputChange}
                      placeholder="Введите необходимое оборудование"
                  />
                            </td>
                        </tr>
                        <tr>
                            <td className="label-cell">
                                Список использованных источников
                            </td>
                            <td className="input-cell">
                  <textarea
                      name="istochniki"
                      value={formData.istochniki}
                      onChange={handleInputChange}
                      placeholder="Введите источники"
                  />
                            </td>
                        </tr>
                        </tbody>
                    </table>

                    {/* ЭТАПЫ ЗАНЯТИЯ */}
                    <h2 className="section-title">Этапы занятия</h2>
                    {formData.stages.map((stage, index) => (
                        <div key={index} className="stage-block">
                            <div className="stage-header">
                                <h4>
                                    Этап {index + 1}: {stage.nazvanie_etapa || 'Новый этап'}
                                </h4>
                                {formData.stages.length > 1 && (
                                    <button
                                        type="button"
                                        className="remove-stage-btn"
                                        onClick={() => removeStage(index)}
                                    >
                                        Удалить
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
                                            value={stage.nazvanie_etapa}
                                            onChange={e =>
                                                handleStageChange(index, 'nazvanie_etapa', e.target.value)
                                            }
                                            placeholder="Например: Актуализация опорных знаний"
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Цель</td>
                                    <td className="input-cell">
                      <textarea
                          value={stage.cel_etapa}
                          onChange={e =>
                              handleStageChange(index, 'cel_etapa', e.target.value)
                          }
                          placeholder="Цель этапа"
                      />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Длительность этапа</td>
                                    <td className="input-cell">
                                        <input
                                            type="text"
                                            value={stage.dlitelnost}
                                            onChange={e =>
                                                handleStageChange(index, 'dlitelnost', e.target.value)
                                            }
                                            placeholder="Например: 10 минут"
                                        />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Деятельность преподавателя</td>
                                    <td className="input-cell">
                      <textarea
                          value={stage.deyatelnost_prepod}
                          onChange={e =>
                              handleStageChange(
                                  index,
                                  'deyatelnost_prepod',
                                  e.target.value
                              )
                          }
                          placeholder="Деятельность преподавателя"
                      />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Деятельность обучающихся</td>
                                    <td className="input-cell">
                      <textarea
                          value={stage.deyatelnost_obuch}
                          onChange={e =>
                              handleStageChange(
                                  index,
                                  'deyatelnost_obuch',
                                  e.target.value
                              )
                          }
                          placeholder="Деятельность обучающихся"
                      />
                                    </td>
                                </tr>
                                <tr>
                                    <td className="label-cell">Формируемые компетенции</td>
                                    <td className="input-cell">
                      <textarea
                          value={stage.formiruemye_kompetencii}
                          onChange={e =>
                              handleStageChange(
                                  index,
                                  'formiruemye_kompetencii',
                                  e.target.value
                              )
                          }
                          placeholder="Формируемые компетенции"
                      />
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    ))}

                    <button type="button" className="add-stage-btn" onClick={addStage}>
                        + Добавить этап
                    </button>

                    {/* КНОПКА ОТПРАВКИ */}
                    <button type="button" className="submit-button" onClick={handleSubmit}>
                        Сохранить и скачать
                    </button>
                </div>
            </div>

            {/* МОДАЛЬНОЕ ОКНО С ПРЕДУПРЕЖДЕНИЯМИ */}
            {showWarningsModal && (
                <div className="modal-overlay" onClick={handleCancelSubmit}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <h3>⚠ Внимание!</h3>
                        <p>Следующие поля остались пустыми:</p>
                        <ul className="warnings-list">
                            {warnings.map((warning, index) => (
                                <li key={index}>{warning}</li>
                            ))}
                        </ul>
                        <p className="modal-question">
                            Продолжить генерацию документа?
                        </p>
                        <div className="modal-buttons">
                            <button
                                type="button"
                                className="modal-btn cancel-btn"
                                onClick={handleCancelSubmit}
                            >
                                Отмена
                            </button>
                            <button
                                type="button"
                                className="modal-btn continue-btn"
                                onClick={handleContinueWithWarnings}
                            >
                                Продолжить
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default TechCardForm;
