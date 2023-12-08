import React, { useState } from 'react'
import { Form, Button } from 'react-bootstrap'
import { useUserActions } from '../../hooks/user.actions'

function RegistrationForm() {
    const [validated, setValidated] = useState(false)
    const [error, setError] = useState(null)
    const [form, setForm] = useState({
        username: '',
        email: '',
        password: '',
    })

    const userAction = useUserActions()

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault()
        const registrationForm = event.currentTarget as HTMLFormElement

        if (registrationForm.checkValidity() === false) {
            event.stopPropagation()
        }
        setValidated(true)

        const data = {
            username: form.username,
            email: form.email,
            password: form.password,
        }

        userAction.register(data).catch((err) => {
            if (err.message) {
                setError(err.request.response)
            }
        })
    }
    return (
        <Form
            id='registration-form'
            className='border p-4 rounded'
            noValidate
            validated={validated}
            onSubmit={handleSubmit}
            data-testid='registration-form'
        >
            <Form.Group className='mb-3'>
                <Form.Label>Username</Form.Label>
                <Form.Control
                    value={form.username}
                    onChange={(e) =>
                        setForm({ ...form, username: e.target.value })
                    }
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
                <Form.Label>Email</Form.Label>
                <Form.Control
                    value={form.email}
                    onChange={(e) =>
                        setForm({ ...form, email: e.target.value })
                    }
                    required
                    type='text'
                    placeholder='Enter your email'
                    data-testid='form-email-field'
                />
                <Form.Control.Feedback type='invalid'>
                    It's required field
                </Form.Control.Feedback>
            </Form.Group>
            <Form.Group className='mb-3'>
                <Form.Label>Password</Form.Label>
                <Form.Control
                    value={form.password}
                    minLength={8}
                    onChange={(e) =>
                        setForm({ ...form, password: e.target.value })
                    }
                    required
                    type='password'
                    placeholder='Enter your password'
                    data-testid='form-password-field'
                />
                <Form.Control.Feedback type='invalid'>
                    It's required field
                </Form.Control.Feedback>
            </Form.Group>

            <div className='text-content text-danger'>
                {error && <p>{error}</p>}
            </div>

            <Button variant='primary' type='submit'>
                Register
            </Button>
        </Form>
    )
}

export default RegistrationForm
