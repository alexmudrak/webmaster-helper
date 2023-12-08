import { Card, Col, Form, Row } from 'react-bootstrap'

const MailSettingsFieldsGroup = ({ form, onChange }) => (
  <>
    <Row>
      <Col>
        <Card className='mb-3'>
          <Card.Body>
            <Card.Title>Mailbox Settings</Card.Title>
            <hr />
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='smtp_server'>Mailbox folders</Form.Label>
              <Form.Control
                type='text'
                id='mail_folders'
                name='mail_folders'
                value={form?.mail_folders}
                onChange={onChange}
              />
              <Form.Text className='text-muted'>
                Enter the names of your mailbox folders, separated by commas.
              </Form.Text>
            </Form.Group>
          </Card.Body>
        </Card>
      </Col>
    </Row>
    <Row>
      {/* SMTP Settings */}
      <Col md={6}>
        <Card className='mb-3'>
          <Card.Body>
            <Card.Title>SMTP Settings</Card.Title>
            <hr />
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='smtp_server'>SMTP Host</Form.Label>
              <Form.Control
                type='text'
                id='smtp_server'
                name='smtp_server'
                value={form?.smtp_server}
                onChange={onChange}
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='smtp_port'>SMTP Port</Form.Label>
              <Form.Control
                type='text'
                id='smtp_port'
                name='smtp_port'
                value={form?.smtp_port}
                onChange={onChange}
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='smtp_username'>SMTP Username</Form.Label>
              <Form.Control
                type='text'
                id='smtp_username'
                name='smtp_username'
                value={form?.smtp_username}
                onChange={onChange}
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='smtp_password'>SMTP Password</Form.Label>
              <Form.Control
                type='password'
                id='smtp_password'
                name='smtp_password'
                value={form?.smtp_password}
                onChange={onChange}
              />
            </Form.Group>
          </Card.Body>
        </Card>
      </Col>

      {/* IMAP Settings */}
      <Col md={6}>
        <Card className='mb-3'>
          <Card.Body>
            <Card.Title>IMAP Settings</Card.Title>
            <hr />
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='imap_server'>IMAP Host</Form.Label>
              <Row className='align-items-center'>
                <Col md={3}>
                  <Form.Check
                    type='checkbox'
                    id='imap_ssl'
                    name='imap_ssl'
                    checked={form?.imap_ssl}
                    onChange={onChange}
                    label='SSL'
                  />
                </Col>
                <Col md={9}>
                  <Form.Control
                    type='text'
                    id='imap_server'
                    name='imap_server'
                    value={form?.imap_server}
                    onChange={onChange}
                  />
                </Col>
              </Row>
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='imap_port'>IMAP Port</Form.Label>
              <Form.Control
                type='text'
                id='imap_port'
                name='imap_port'
                value={form?.imap_port}
                onChange={onChange}
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='imap_username'>IMAP Username</Form.Label>
              <Form.Control
                type='text'
                id='imap_username'
                name='imap_username'
                value={form?.imap_username}
                onChange={onChange}
              />
            </Form.Group>
            <Form.Group className='mb-3'>
              <Form.Label htmlFor='imap_password'>IMAP Password</Form.Label>
              <Form.Control
                type='password'
                id='imap_password'
                name='imap_password'
                value={form?.imap_password}
                onChange={onChange}
              />
            </Form.Group>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  </>
)

export default MailSettingsFieldsGroup
