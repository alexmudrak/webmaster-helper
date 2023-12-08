import '@testing-library/jest-dom'

import { fireEvent, render, screen } from '@testing-library/react'

import Login from './pages/Login'

describe('Login Form', () => {
  test('renders login form correctly', () => {
    render(<Login />)

    // Проверяем, что форма корректно отрендерена
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument()
  })

  test('handles form submission', () => {
    render(<Login />)

    // Моделируем ввод данных в форму
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'testuser' }
    })
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'testpassword' }
    })

    // Моделируем отправку формы
    fireEvent.click(screen.getByRole('button', { name: /login/i }))

    // Проверяем, что данные были переданы корректно
    // Здесь вы можете добавить дополнительные проверки в зависимости от того, как ваш компонент обрабатывает введенные данные.
  })
})
