import React, { useState } from 'react'
import { Button, Form } from 'react-bootstrap'

import { useUserActions } from '../../hooks/user.actions'

function LoginForm() {
  const [validated, setValidated] = useState(false)
  const [form, setForm] = useState({
    username: '',
    password: ''
  })
  const [error, setError] = useState(null)
  const userActions = useUserActions()

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()
    const loginForm = event.currentTarget as HTMLFormElement

    if (loginForm.checkValidity() === false) {
      event.stopPropagation()
    }
    setValidated(true)

    const data = {
      username: form.username,
      password: form.password
    }

    userActions.login(data).catch((err) => {
      if (err.message) {
        console.error(err.message)
        setError(err.request.response)
      }
    })
  }

  return (
    <Form
      id='login-form'
      className='border p-4 rounded'
      noValidate
      validated={validated}
      onSubmit={handleSubmit}
      data-testid='login-form'
    >
      <Form.Group className='mb-3'>
        <Form.Label>Username</Form.Label>
        <Form.Control
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
          type='text'
          placeholder='Enter your username'
          data-testid='form-username-field'
        />
        <Form.Control.Feedback type='invalid'>
          It's required field
        </Form.Control.Feedback>
      </Form.Group>
      <Form.Group className='mb-3'>
        <Form.Label>Password</Form.Label>
        <Form.Control
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
          type='password'
          placeholder='Enter your password'
          data-testid='form-password-field'
        />
        <Form.Control.Feedback type='invalid'>
          It's required field
        </Form.Control.Feedback>
      </Form.Group>

      <div className='text-content text-danger'>{error && <p>{error}</p>}</div>

      <Button variant='primary' type='submit'>
        Login
      </Button>
    </Form>
  )
}

export default LoginForm
