import { useState } from 'react'
import { Button, Card, Col, Form, Nav, Row, Tab } from 'react-bootstrap'
import useSWR from 'swr'

import axiosService, { fetcher } from '../../helper/axios'
import { getUser } from '../../hooks/user.actions'
import { UserData } from '../../types'
import MailSettingsFieldsGroup from '../mail_settings/MailSettingsFieldsGroup'

const UserProfileForm: React.FC = () => {
  const userStore = getUser()
  const [form, setForm] = useState<UserData>({
    id: '',
    username: '',
    email: '',
    created: '',
    updated: '',
    is_active: false,
    mail_settings: {
      mail_folders: '',
      smtp_server: '',
      smtp_port: 0,
      smtp_username: '',
      smtp_password: '',
      imap_ssl: false,
      imap_server: '',
      imap_port: 0,
      imap_username: '',
      imap_password: ''
    }
  })

  const { data: user, mutate } = useSWR<UserData>(
    `/user/${userStore.id}/`,
    fetcher,
    {
      onSuccess: (data) => {
        setForm({ ...data })
      }
    }
  )

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target

    setForm((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleUpdateMailSettings = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value, type, checked } = e.target

    setForm((prevForm: UserData) => ({
      ...prevForm,
      mail_settings: {
        ...prevForm.mail_settings,
        [name]: type === 'checkbox' ? checked : value
      }
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const requestData = {
      username: form.username,
      email: form.email,
      mail_settings: form.mail_settings
    }

    const requestMethod = 'patch'
    axiosService
      .request({
        url: `/user/${user?.id}/`,
        method: requestMethod,
        data: requestData
      })
      .then(() => {
        mutate()
      })
      .catch((err) => console.error('Error during API request:', err))
  }

  return (
    <Form onSubmit={handleSubmit}>
      <Card className='mb-3'>
        <Card.Body>
          <Form.Group className='mb-3'>
            <Form.Label htmlFor='name'>Name</Form.Label>
            <Form.Control
              type='text'
              id='name'
              name='name'
              value={form.username}
              onChange={handleChange}
            />
          </Form.Group>
          <Form.Group className='mb-3'>
            <Form.Label htmlFor='email'>Email</Form.Label>
            <Form.Control
              type='email'
              id='email'
              name='email'
              value={form.email}
              onChange={handleChange}
            />
          </Form.Group>
        </Card.Body>
      </Card>

      <Tab.Container id='left-tabs-example' defaultActiveKey='mail-settings'>
        <Row>
          <Col sm={3}>
            <Nav variant='pills' className='flex-column'>
              <Nav.Item>
                <Nav.Link eventKey='mail-settings'>Mail Settings</Nav.Link>
              </Nav.Item>

              <Nav.Item>
                <Nav.Link disabled eventKey='proxy'>
                  Proxy Settings
                </Nav.Link>
              </Nav.Item>

              <Nav.Item>
                <Nav.Link disabled eventKey='parser'>
                  Parsers
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>
          <Col sm={9}>
            <Tab.Content>
              <Tab.Pane eventKey='mail-settings'>
                <MailSettingsFieldsGroup
                  form={form?.mail_settings}
                  onChange={handleUpdateMailSettings}
                />
              </Tab.Pane>
            </Tab.Content>
          </Col>
        </Row>
      </Tab.Container>

      <div className='d-flex justify-content-end'>
        <Button type='submit' variant='primary'>
          Save Changes
        </Button>
      </div>
    </Form>
  )
}

export default UserProfileForm
