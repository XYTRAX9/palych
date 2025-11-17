// jest-dom добавляет пользовательские jest matchers для проверки узлов DOM.
// позволяет делать такие вещи, как:
// expect(element).toHaveTextContent(/react/i)
// узнайте больше: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// Мокируем window.URL.createObjectURL
global.URL.createObjectURL = jest.fn(() => 'mock-url');
global.URL.revokeObjectURL = jest.fn();

// Мокируем console.error для более чистого вывода тестов
const originalError = console.error;
beforeAll(() => {
    console.error = jest.fn();
});

afterAll(() => {
    console.error = originalError;
});
