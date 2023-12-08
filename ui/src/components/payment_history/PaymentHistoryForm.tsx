import React, { useEffect, useState } from 'react'
import { Button, Form } from 'react-bootstrap'

import axiosService from '../../helper/axios'
import { usePaymentActions } from '../../hooks/payment.actions'
import { useProjectActions } from '../../hooks/project.actions'
import { useWebmastersActions } from '../../hooks/webmaster.actions'
import { useWebsiteActions } from '../../hooks/website.actions'
import {
  PaymentHistoryDataRow,
  PaymentHistoryFormContentProps,
  PaymentHistoryFormProps
} from '../../types'
import FormField from '../form_fields/FormField'
import SingleChoiceField from '../form_fields/SingleChoiceField'
import ModalBase from '../ModalBase'

const FormContent = ({
  form,
  handleSubmit,
  updateFormValue,
  buttons
}: PaymentHistoryFormContentProps) => {
  const [webmastersData, setWebmastersData] = useState(null)
  const [websitesData, setWebsitesData] = useState(null)
  const [projectsData, setProjectsData] = useState(null)
  const [paymentsData, setPaymentsData] = useState(null)
  const { getWebmasters } = useWebmastersActions()
  const { getWebsites } = useWebsiteActions()
  const { getProjects } = useProjectActions()
  const { getPayments } = usePaymentActions()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const webmastersData = await getWebmasters()
        const projectsData = await getProjects()
        const sortedProjects = [...projectsData].sort((a, b) =>
          a.name.localeCompare(b.name, undefined, { sensitivity: 'base' })
        )

        setWebmastersData(webmastersData)
        setProjectsData(sortedProjects)
      } catch (error) {
        console.error('Error fetching webmasters:', error)
      }
    }
    fetchData()
  }, [])

  useEffect(() => {
    if (form.webmaster?.id) {
      const fetchSites = async () => {
        try {
          const websitesData = await getWebsites()
          const filteredWebsites = websitesData.filter((item) =>
            item.webmasters.some(
              (webmaster) => webmaster.id === form.webmaster?.id
            )
          )
          const websitesList = filteredWebsites.map((item) => {
            const website = item.site
            return {
              id: item?.id,
              name: website?.url
            }
          })

          const paymentsData = await getPayments()
          const filteredPayments = paymentsData.filter(
            (item) => item.webmaster.id === form.webmaster?.id
          )
          const paymentsList = filteredPayments.map((item) => {
            return {
              id: item?.id,
              name: item?.details
            }
          })

          setWebsitesData(websitesList)
          setPaymentsData(paymentsList)
        } catch (error) {
          console.error('Error fetching sites:', error)
        }
      }
      fetchSites()
    }
  }, [form.webmaster?.id])

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <div className='card mb-3'>
          <div className='card-body'>
            <h5>Project data</h5>
            <hr />
            <SingleChoiceField
              placeholder='Select project'
              values={projectsData || []}
              selectedValues={{
                id: form.project?.id,
                name: form.project?.name
              }}
              onChange={(value) => updateFormValue('project', value)}
            />
          </div>
        </div>

        <div className='card mb-3'>
          <div className='card-body'>
            <h5>Webmaster data</h5>
            <hr />
            <SingleChoiceField
              placeholder='Select webmaster'
              values={webmastersData || []}
              selectedValues={{
                id: form.webmaster?.id,
                name: form.webmaster?.name
              }}
              onChange={(value) => {
                updateFormValue(`webmaster`, value)
                updateFormValue('website', null)
                updateFormValue('payment', null)
              }}
            />

            {websitesData && (
              <>
                <SingleChoiceField
                  placeholder='Select website'
                  values={websitesData || []}
                  selectedValues={{
                    id: form.website?.id,
                    name: form.website?.name
                  }}
                  onChange={(value) => updateFormValue('website', value)}
                />
                <SingleChoiceField
                  placeholder='Select payment'
                  values={paymentsData || []}
                  selectedValues={{
                    id: form.payment?.id,
                    name: form.payment?.detail || form.payment?.name
                  }}
                  onChange={(value) => updateFormValue('payment', value)}
                />
                <FormField
                  label='Payment value'
                  type='number'
                  placeholder='Please enter payment value'
                  value={form?.price || ''}
                  onChange={(value) => updateFormValue('price', value)}
                />
              </>
            )}
          </div>
        </div>

        {buttons}
      </Form>
    </>
  )
}

const emptyPaymentHistoryDataRow: PaymentHistoryDataRow = {}

function PaymentForm({
  page_obj,
  endpointName,
  useModal,
  showModal,
  onClose
}: PaymentHistoryFormProps) {
  const [show, setShow] = useState(showModal)
  const [form, setForm] = useState(
    page_obj ? page_obj : { ...emptyPaymentHistoryDataRow }
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
    <Button variant='primary' onClick={handleSubmit} disabled={!form?.price}>
      {form.id ? 'Update' : 'Add'}
    </Button>
  )

  return useModal ? (
    <ModalBase
      show={show}
      title='Message'
      handleClose={handleClose}
      customButton={formButtons}
      widthSize='70'
    >
      <FormContent
        form={form}
        handleSubmit={handleSubmit}
        updateFormValue={updateFormValue}
      />
    </ModalBase>
  ) : (
    <FormContent
      form={form}
      handleSubmit={handleSubmit}
      updateFormValue={updateFormValue}
      buttons={formButtons}
    />
  )
}

export default PaymentForm
