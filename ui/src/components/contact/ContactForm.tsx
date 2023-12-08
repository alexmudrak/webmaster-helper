import 'react-datepicker/dist/react-datepicker.css'
import 'bootstrap/dist/css/bootstrap.min.css'

import React, { useEffect, useState } from 'react'
import { Button, Col, Form, Row } from 'react-bootstrap'

import axiosService from '../../helper/axios'
import { useWebmastersActions } from '../../hooks/webmaster.actions'
import {
  ContactDataRow,
  ContactFormContentProps,
  ContactFormProps
} from '../../types'
import FormField from '../form_fields/FormField'
import SingleChoiceField from '../form_fields/SingleChoiceField'
import ModalBase from '../ModalBase'

const contactOptions = [
  { id: 'email', name: 'Email' },
  { id: 'skype', name: 'Skype' },
  { id: 'telegram', name: 'Telegram' },
  { id: 'other', name: 'Other' }
]

const ContactFormContent = ({
  form,
  handleSubmit,
  updateFormValue,
  buttons
}: ContactFormContentProps) => {
  const [webmastersData, setWebmastersData] = useState(null)
  const { getWebmasters } = useWebmastersActions()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const webmastersData = await getWebmasters()
        setWebmastersData(webmastersData)
      } catch (error) {
        console.error('Error fetching webmasters:', error)
      }
    }
    fetchData()
  }, [])

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <div className='card mb-3'>
          <div className='card-body'>
            <SingleChoiceField
              placeholder='Select webmaster'
              values={webmastersData || []}
              selectedValues={{
                id: form.webmaster?.id,
                name: form.webmaster?.name
              }}
              onChange={(value) => updateFormValue(`webmaster`, value)}
            />
            <Row key={1} className='mb-1' xs={10}>
              <Col xs={4}>
                <SingleChoiceField
                  placeholder='Select type'
                  values={contactOptions}
                  selectedValues={contactOptions.find(
                    (option) => option.id === form.type?.toLowerCase()
                  )}
                  onChange={(value) => updateFormValue(`type`, value.id)}
                />
              </Col>
              <Col xs={8}>
                <FormField
                  type='text'
                  placeholder='Please enter contact details'
                  value={form?.contact || ''}
                  onChange={(value) => updateFormValue('contact', value)}
                />
              </Col>
            </Row>
          </div>
        </div>

        {buttons}
      </Form>
    </>
  )
}

const emptyContactDataRow: ContactDataRow = {
  id: '',
  contact: '',
  type: '',
  last_contact_date: null,
  updated: ''
}

function ContactForm({
  page_obj,
  endpointName,
  useModal,
  showModal,
  onClose
}: ContactFormProps) {
  const [show, setShow] = useState(showModal)
  const [form, setForm] = useState(
    page_obj ? page_obj : { ...emptyContactDataRow }
  )
  const handleClose = () => {
    setShow(false)
    onClose()
  }

  useEffect(() => {
    setShow(showModal)
  }, [showModal])

  const updateFormValue = (field: string, value: string | object) => {
    setForm((prevForm) => {
      const fieldParts = field.split('.')
      const newForm = { ...prevForm }
      let currentObject = newForm

      for (let i = 0; i < fieldParts.length - 1; i++) {
        currentObject = currentObject[fieldParts[i]]
      }

      currentObject[fieldParts[fieldParts.length - 1]] = value
      return newForm
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const apiUrl = form.id
      ? `/${endpointName}/${form.id}/`
      : `/${endpointName}/`
    const requestMethod = form.id ? 'patch' : 'post'

    axiosService
      .request({
        url: apiUrl,
        method: requestMethod,
        data: { ...form }
      })
      .then(() => {
        handleClose()
      })
      .catch((err) =>
        console.error('Error during API request:', err?.response?.data)
      )
  }

  const formButtons: JSX.Element = (
    <Button
      variant='primary'
      onClick={handleSubmit}
      disabled={form.contact === ''}
    >
      {form.id ? 'Update' : 'Add'}
    </Button>
  )

  return useModal ? (
    <ModalBase
      show={show}
      title='Contact'
      handleClose={handleClose}
      customButton={formButtons}
      widthSize='70'
    >
      <ContactFormContent
        form={form}
        handleSubmit={handleSubmit}
        updateFormValue={updateFormValue}
      />
    </ModalBase>
  ) : (
    <ContactFormContent
      form={form}
      handleSubmit={handleSubmit}
      updateFormValue={updateFormValue}
      buttons={formButtons}
    />
  )
}

export default ContactForm
