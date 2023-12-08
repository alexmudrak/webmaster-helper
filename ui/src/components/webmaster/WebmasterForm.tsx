import 'react-datepicker/dist/react-datepicker.css'
import 'bootstrap/dist/css/bootstrap.min.css'

import { faPlus, faTrash } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import React, { useEffect, useState } from 'react'
import { Button, Col, Form, Row } from 'react-bootstrap'

import axiosService from '../../helper/axios'
import { useContactActions } from '../../hooks/contact.actions'
import { usePaymentActions } from '../../hooks/payment.actions'
import { useWebsiteActions } from '../../hooks/website.actions'
import {
  WebmasterDataRow,
  WebmasterFormContentProps,
  WebmasterFormProps
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

const paymentOptions = [
  { id: 'yandex_money', name: 'Yandex money' },
  { id: 'webmoney', name: 'Webmoney' },
  { id: 'qiwi', name: 'Qiwi' },
  { id: 'card', name: 'Card' },
  { id: 'other', name: 'Other' }
]

const WebmasterFormContent = ({
  form,
  handleSubmit,
  updateFormValue,
  buttons
}: WebmasterFormContentProps) => {
  const { deleteContactItem } = useContactActions()
  const { deletePaymentItem } = usePaymentActions()
  const { deleteWebsiteItem } = useWebsiteActions()

  const handleDelete =
    (index: number, rowType: string, itemId: string) => () => {
      if (itemId) {
        switch (rowType) {
          case 'contacts':
            deleteContactItem(itemId)
            break
          case 'payments':
            deletePaymentItem(itemId)
            break
          case 'websites':
            deleteWebsiteItem(itemId)
            break
          default:
            console.error('Unsupported rowType in Webmaster form')
        }
      }
      updateFormValue(
        `${rowType}`,
        form[rowType].filter((_, i) => i !== index)
      )
    }

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <div className='card mb-3'>
          <div className='card-body'>
            <FormField
              label='Webmaster name'
              type='text'
              placeholder='Please enter website name'
              value={form?.name || ''}
              onChange={(value) => updateFormValue('name', value)}
            />
          </div>
        </div>

        <div className='card mb-3'>
          <div className='card-body'>
            <h5>Contacts</h5>
            <hr />
            {form.contacts?.map((contact, index) => (
              <Row key={index} className='mb-1' xs={10}>
                <Col xs={4}>
                  <SingleChoiceField
                    placeholder='Select type'
                    values={contactOptions}
                    selectedValues={contactOptions.find(
                      (option) => option.id === contact?.type?.toLowerCase()
                    )}
                    onChange={(value) =>
                      updateFormValue(`contacts.${index}.type`, value.id)
                    }
                  />
                </Col>
                <Col xs={6}>
                  <FormField
                    type='text'
                    placeholder='Please enter contact information'
                    value={contact?.contact || ''}
                    onChange={(value) =>
                      updateFormValue(`contacts.${index}.contact`, value)
                    }
                  />
                </Col>
                <Col xs={2}>
                  <Button
                    variant='danger'
                    onClick={handleDelete(index, 'contacts', contact?.id)}
                  >
                    <FontAwesomeIcon icon={faTrash} />
                  </Button>
                </Col>
              </Row>
            ))}
            <Button
              variant='success'
              onClick={() =>
                updateFormValue(`contacts.${form?.contacts?.length}`, {})
              }
            >
              <FontAwesomeIcon icon={faPlus} />
            </Button>
          </div>
        </div>

        <div className='card mb-3'>
          <div className='card-body'>
            <h5>Payments</h5>
            <hr />
            {form.payments?.map((payment, index) => (
              <Row key={index} className='mb-1' xs={10}>
                <Col xs={4}>
                  <SingleChoiceField
                    placeholder='Select type'
                    values={paymentOptions}
                    selectedValues={paymentOptions.find(
                      (option) => option.id === payment?.type?.toLowerCase()
                    )}
                    onChange={(value) =>
                      updateFormValue(`payments.${index}.type`, value.id)
                    }
                  />
                </Col>
                <Col xs={6}>
                  <FormField
                    type='text'
                    placeholder='Please enter payment details'
                    value={payment?.details || ''}
                    onChange={(value) =>
                      updateFormValue(`payments.${index}.details`, value)
                    }
                  />
                </Col>
                <Col xs={2}>
                  <Button
                    variant='danger'
                    onClick={handleDelete(index, 'payments', payment?.id)}
                  >
                    <FontAwesomeIcon icon={faTrash} />
                  </Button>
                </Col>
              </Row>
            ))}
            <Button
              variant='success'
              onClick={() =>
                updateFormValue(`payments.${form?.payments?.length}`, {})
              }
            >
              <FontAwesomeIcon icon={faPlus} />
            </Button>
          </div>
        </div>

        <div className='card mb-3'>
          <div className='card-body'>
            <h5>Websites</h5>
            <hr />
            {form.websites?.map((website, index) => (
              <Row key={index} className='mb-1' xs={10}>
                <Col xs={10}>
                  <FormField
                    type='text'
                    placeholder='Please enter website url'
                    value={website?.site?.url || ''}
                    onChange={(value) =>
                      updateFormValue(`websites.${index}.site.url`, value)
                    }
                  />
                </Col>
                <Col xs={2}>
                  <Button
                    variant='danger'
                    onClick={handleDelete(index, 'websites', website?.id)}
                  >
                    <FontAwesomeIcon icon={faTrash} />
                  </Button>
                </Col>
              </Row>
            ))}
            <Button
              variant='success'
              onClick={() =>
                updateFormValue(`websites.${form?.websites?.length}`, {
                  site: {}
                })
              }
            >
              <FontAwesomeIcon icon={faPlus} />
            </Button>
          </div>
        </div>

        {buttons}
      </Form>
    </>
  )
}

const emptyWebmasterDataRow: WebmasterDataRow = {
  id: '',
  name: '',
  contacts: [],
  payments: [],
  websites: []
}

function WebmasterForm({
  page_obj,
  endpointName,
  useModal,
  showModal,
  onClose
}: WebmasterFormProps) {
  const [show, setShow] = useState(showModal)
  const [form, setForm] = useState(
    page_obj ? page_obj : { ...emptyWebmasterDataRow }
  )
  const handleClose = () => {
    setShow(false)
    onClose()
  }

  useEffect(() => {
    setShow(showModal)
  }, [showModal])

  const updateFormValue = (field: string, value: string) => {
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
      disabled={form.name === ''}
    >
      {form.id ? 'Update' : 'Add'}
    </Button>
  )

  return useModal ? (
    <ModalBase
      show={show}
      title={`Webmaster: ${form.name || ''}`}
      handleClose={handleClose}
      customButton={formButtons}
      widthSize='70'
    >
      <WebmasterFormContent
        form={form}
        handleSubmit={handleSubmit}
        updateFormValue={updateFormValue}
      />
    </ModalBase>
  ) : (
    <WebmasterFormContent
      form={form}
      handleSubmit={handleSubmit}
      updateFormValue={updateFormValue}
      buttons={formButtons}
    />
  )
}

export default WebmasterForm
