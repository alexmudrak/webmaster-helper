import React, { useEffect, useState } from 'react'
import { Button, Form } from 'react-bootstrap'

import axiosService from '../../helper/axios'
import {
  ProjectFormContentProps,
  ProjectFormProps
} from '../../types'
import FormField from '../form_fields/FormField'
import MailSettingsFieldsGroup from '../mail_settings/MailSettingsFieldsGroup'
import ModalBase from '../ModalBase'

const ProjectFormContent = ({
  form,
  handleSubmit,
  updateFormValue,
  showMailSettingsForm,
  handleToggleMailSettingsForm,
  handleUpdateMailSettings,
  buttons
}: ProjectFormContentProps) => {
  return (
    <>
      <Form onSubmit={handleSubmit}>
        <div className='card mb-3'>
          <div className='card-body'>
            <FormField
              label='Project name'
              type='text'
              placeholder='Please enter project name'
              value={form?.name || ''}
              onChange={(value) => updateFormValue('name', value)}
            />

            <FormField
              label='Url'
              type='text'
              placeholder='Please enter project url'
              value={form?.url?.url || ''}
              onChange={(value) => updateFormValue('url.url', value)}
            />
          </div>
        </div>

        <Button className='mb-3' variant='secondary' onClick={handleToggleMailSettingsForm}>
          {showMailSettingsForm ? 'Hide Mail Settings' : 'Show Mail Settings'}
        </Button>

        {showMailSettingsForm && (
          <MailSettingsFieldsGroup
            form={form?.mail_settings}
            onChange={handleUpdateMailSettings}
          />
        )}
        {buttons}
      </Form>
    </>
  )
}

const ProjectForm = ({
  page_obj,
  endpointName,
  useModal,
  showModal,
  onClose
}: ProjectFormProps) => {
  const [show, setShow] = useState(showModal)
  const [form, setForm] = useState({
    ...page_obj
  })

  const [showMailSettingsForm, setShowMailSettingsForm] = useState(
    !!form?.mail_settings
  )

  const handleClose = () => {
    setShow(false)
    onClose()
  }

  useEffect(() => {
    setShow(showModal)
  }, [showModal])

  const handleUpdateMailSettings = (e) => {
    const { name, value, type, checked } = e.target

    setForm((prevForm) => ({
      ...prevForm,
      mail_settings: {
        ...prevForm.mail_settings,
        [name]: type === 'checkbox' ? checked : value
      }
    }))
  }

  const updateFormValue = (field: string, value: string) => {
    setForm((prevForm) => {
      if (field.includes('.')) {
        const [outerField, innerField] = field.split('.')
        return {
          ...prevForm,
          [outerField]: {
            ...prevForm[outerField],
            [innerField]: value
          }
        }
      } else {
        return {
          ...prevForm,
          [field]: value
        }
      }
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const mailSettingsData = showMailSettingsForm ? form.mail_settings : null

    const apiUrl = form.id
      ? `/${endpointName}/${form.id}/`
      : `/${endpointName}/`
    const requestMethod = form.id ? 'patch' : 'post'

    axiosService
      .request({
        url: apiUrl,
        method: requestMethod,
        data: { ...form, mail_settings: mailSettingsData }
      })
      .then(() => {
        handleClose()
      })
      .catch((err) => console.error('Error during API request:', err))
  }

  const handleToggleMailSettingsForm = () => {
    setShowMailSettingsForm((prev) => !prev)
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
      title='Project'
      handleClose={handleClose}
      customButton={formButtons}
      widthSize='70'
    >
      <ProjectFormContent
        form={form}
        handleSubmit={handleSubmit}
        updateFormValue={updateFormValue}
        showMailSettingsForm={showMailSettingsForm}
        handleToggleMailSettingsForm={handleToggleMailSettingsForm}
        handleUpdateMailSettings={handleUpdateMailSettings}
      />
    </ModalBase>
  ) : (
    <ProjectFormContent
      form={form}
      handleSubmit={handleSubmit}
      updateFormValue={updateFormValue}
      showMailSettingsForm={showMailSettingsForm}
      handleToggleMailSettingsForm={handleToggleMailSettingsForm}
      handleUpdateMailSettings={handleUpdateMailSettings}
      buttons={formButtons}
    />
  )
}

export default ProjectForm
