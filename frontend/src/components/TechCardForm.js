import React, { useState } from 'react';
import './TechCardForm.css';

function TechCardForm() {
    const [formData, setFormData] = useState({
        subject: '',
        class: '',
        topic: '',
        lessonType: '',
        duration: ''
    });

    const [errors, setErrors] = useState({});
    const [notification, setNotification] = useState(null);

    const lessonTypes = [
        'Изучение нового материала',
        'Закрепление знаний',
        'Комбинированный урок',
        'Контрольный урок',
        'Практическая работа'
    ];

    const classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'];
    const durations = ['40 минут', '45 минут', '60 минут', '90 минут'];

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        // Убираем ошибку при вводе
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const validateForm = () => {
        const newErrors = {};

        if (!formData.subject.trim()) {
            newErrors.subject = 'Поле "Предмет" обязательно для заполнения';
        } else if (formData.subject.trim().length < 2) {
            newErrors.subject = 'Название предмета должно содержать минимум 2 символа';
        }

        if (!formData.class) {
            newErrors.class = 'Выберите класс';
        }

        if (!formData.topic.trim()) {
            newErrors.topic = 'Поле "Тема урока" обязательно для заполнения';
        } else if (formData.topic.trim().length < 3) {
            newErrors.topic = 'Тема урока должна содержать минимум 3 символа';
        }

        if (!formData.lessonType) {
            newErrors.lessonType = 'Выберите тип урока';
        }

        if (!formData.duration) {
            newErrors.duration = 'Выберите продолжительность урока';
        }

        return newErrors;
    };

    const showNotification = (type, message) => {
        setNotification({ type, message });
        setTimeout(() => {
            setNotification(null);
        }, 4000);
    };

    const handleSubmit = () => {
        const validationErrors = validateForm();

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            showNotification('error', 'Пожалуйста, заполните все поля корректно');
            return;
        }

        // Успешная валидация
        console.log('Данные формы:', formData);
        showNotification('success', 'Документ успешно сгенерирован! Скачивание начнётся через несколько секунд...');

        // Здесь будет логика скачивания файла
        setTimeout(() => {
            // TODO: Добавить логику скачивания документа
            console.log('Начало скачивания документа...');
        }, 2000);

        // Очистка формы после успешной отправки (опционально)
        // setFormData({
        //   subject: '',
        //   class: '',
        //   topic: '',
        //   lessonType: '',
        //   duration: ''
        // });
    };

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
                        <label>Предмет</label>
                        <input
                            type="text"
                            name="subject"
                            value={formData.subject}
                            onChange={handleInputChange}
                            placeholder="Например: Математика"
                            className={errors.subject ? 'error' : ''}
                        />
                        {errors.subject && <span className="error-message">{errors.subject}</span>}
                    </div>

                    <div className="form-group">
                        <label>Класс</label>
                        <select
                            name="class"
                            value={formData.class}
                            onChange={handleInputChange}
                            className={errors.class ? 'error' : ''}
                        >
                            <option value="">Выберите класс</option>
                            {classes.map(cls => (
                                <option key={cls} value={cls}>{cls} класс</option>
                            ))}
                        </select>
                        {errors.class && <span className="error-message">{errors.class}</span>}
                    </div>

                    <div className="form-group">
                        <label>Тема урока</label>
                        <input
                            type="text"
                            name="topic"
                            value={formData.topic}
                            onChange={handleInputChange}
                            placeholder="Введите тему урока"
                            className={errors.topic ? 'error' : ''}
                        />
                        {errors.topic && <span className="error-message">{errors.topic}</span>}
                    </div>

                    <div className="form-group">
                        <label>Тип урока</label>
                        <select
                            name="lessonType"
                            value={formData.lessonType}
                            onChange={handleInputChange}
                            className={errors.lessonType ? 'error' : ''}
                        >
                            <option value="">Выберите тип урока</option>
                            {lessonTypes.map(type => (
                                <option key={type} value={type}>{type}</option>
                            ))}
                        </select>
                        {errors.lessonType && <span className="error-message">{errors.lessonType}</span>}
                    </div>

                    <div className="form-group">
                        <label>Продолжительность</label>
                        <select
                            name="duration"
                            value={formData.duration}
                            onChange={handleInputChange}
                            className={errors.duration ? 'error' : ''}
                        >
                            <option value="">Выберите продолжительность</option>
                            {durations.map(dur => (
                                <option key={dur} value={dur}>{dur}</option>
                            ))}
                        </select>
                        {errors.duration && <span className="error-message">{errors.duration}</span>}
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