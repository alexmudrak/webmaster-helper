import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'

import Login from './Login'

describe('Login', () => {
  it('Check login page', async () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    )

    await waitFor(() => screen.getByText('Login', { selector: 'h2' }), {
      timeout: 5000
    })

    const loginForm = screen.getByTestId('login-form')
    expect(loginForm).toBeInTheDocument()

    const errorMessages = screen.getAllByText("It's required field")
    expect(errorMessages).toHaveLength(2)

    const usernameField = screen.getByTestId('form-username-field')
    const passwordField = screen.getByTestId('form-password-field')
    expect(usernameField).toBeInTheDocument()
    expect(passwordField).toBeInTheDocument()

    const loginButton = screen.getByRole('button', { name: /login/i })
    expect(loginButton).toBeInTheDocument()

    const registrationLink = screen.getByText(/register here/i)
    expect(registrationLink).toBeInTheDocument()
  })
})
