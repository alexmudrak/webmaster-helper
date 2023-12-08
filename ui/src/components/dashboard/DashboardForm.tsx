import 'react-datepicker/dist/react-datepicker.css'
import 'bootstrap/dist/css/bootstrap.min.css'

import { faPlus, faTrash } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import React, { useEffect, useState } from 'react'
import { Button, Col, Form, Row } from 'react-bootstrap'
import DatePicker from 'react-datepicker'

import axiosService from '../../helper/axios'
import { useProjectActions} from '../../hooks/project.actions'
import { usePublishPageActions } from '../../hooks/publish_page.actions'
import { useWebmastersActions } from '../../hooks/webmaster.actions'
import {
  DashboardDataRow,
  DashboardFormContentProps,
  DashboardFormProps
} from '../../types'
import FormField from '../form_fields/FormField'
import FormTextarea from '../form_fields/FormTextarea'
import MultiSelectField from '../form_fields/MultiChoiceField'
import ModalBase from '../ModalBase'

const DashboardFormContent = ({
  form,
  handleSubmit,
  updateFormValue,
  buttons
}: DashboardFormContentProps) => {
  const [webmastersData, setWebmastersData] = useState(null)
  const [projectsData, setProjectsData] = useState(null)
  const { getWebmasters } = useWebmastersActions()
  const { getProjects } = useProjectActions()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const webmastersData = await getWebmasters()
        const projectsData = await getProjects()

        setWebmastersData(webmastersData)
        setProjectsData(projectsData)
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    }
    fetchData()
  }, [])

  const { deleteItem } = usePublishPageActions()
  const hasProjects = form.projects.length > 0
  const hasPublishPages = form.projects.some(
    (project) => project.publish_pages && project.publish_pages.length > 0
  )

  if (projectsData?.length > 0 && !hasProjects) {
    const sortedProjects = [...projectsData].sort((a, b) =>
      a.name.localeCompare(b.name)
    )
    updateFormValue(
      'projects',
      sortedProjects.map((project) => ({
        id: project?.id,
        name: project?.name,
        publish_pages: []
      }))
    )
  }

  const [showPublishPagesForm, setPublishPageForm] = useState(hasPublishPages)

  const handleTogglePublishPages = () => {
    setPublishPageForm(!showPublishPagesForm)
  }

  const handleDelete = (index, pageIndex) => () => {
    const itemId = form?.projects[index]?.publish_pages[pageIndex]?.id
    if (itemId) {
      deleteItem(itemId)
    }
    updateFormValue(
      `projects.${index}.publish_pages`,
      form.projects[index].publish_pages.filter((_, i) => i !== pageIndex)
    )
  }

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <div className='card mb-3'>
          <div className='card-body'>
            <FormField
              label='Website url'
              type='text'
              placeholder='Please enter website url'
              value={form?.site?.url || ''}
              onChange={(value) => updateFormValue('site.url', value)}
            />
            <FormField
              label='Website publish cost'
              type='number'
              placeholder='Please enter publish cost'
              value={form?.publish_cost || 0.0}
              onChange={(value) => updateFormValue('publish_cost', value)}
            />
            <MultiSelectField
              label='Webmasters'
              placeholder='Select or create webmasters...'
              values={webmastersData || []}
              selectedValues={form.webmasters || []}
              onChange={(selectedValues) =>
                updateFormValue('webmasters', selectedValues)
              }
            />
            <FormTextarea
              label='Website information'
              placeholder='Please enter website information'
              value={form?.information || ''}
              onChange={(value) => updateFormValue('information', value)}
            />
          </div>
        </div>

        <Button variant='secondary' onClick={handleTogglePublishPages}>
          {showPublishPagesForm ? 'Hide Publish Pages' : 'Show Publish Pages'}
        </Button>

        {buttons}
      </Form>

      {showPublishPagesForm && (
        <>
          {form.projects?.map((project, index) => (
            <Col key={index} className='card my-3'>
              <div className='card-body'>
                <h5>{project.name}</h5>
                <hr />
                {project.publish_pages?.map((page, pageIndex) => (
                  <Row key={`${index}-${pageIndex}`} className='mb-1' xs={12}>
                    <Col xs={3}>
                      <DatePicker
                        selected={
                          page.publish_date
                            ? new Date(page.publish_date)
                            : null
                        }
                        onChange={(value) =>
                          updateFormValue(
                            `projects.${index}.publish_pages.${pageIndex}.publish_date`,
                            value
                          )
                        }
                        dateFormat='dd/M/yyyy'
                        className='form-control'
                        wrapperClassName='w-100'
                      />
                    </Col>
                    <Col xs={7}>
                      <FormField
                        type='text'
                        placeholder='Please enter publish page'
                        value={page.url || ''}
                        onChange={(value) =>
                          updateFormValue(
                            `projects.${index}.publish_pages.${pageIndex}.url`,
                            value
                          )
                        }
                      />
                    </Col>

                    <Col xs={2}>
                      <Button
                        variant='danger'
                        onClick={handleDelete(index, pageIndex)}
                      >
                        <FontAwesomeIcon icon={faTrash} />
                      </Button>
                    </Col>
                  </Row>
                ))}

                <Button
                  variant='success'
                  onClick={() =>
                    updateFormValue(`projects.${index}.publish_pages`, [
                      ...(project.publish_pages || []),
                      { url: '' }
                    ])
                  }
                >
                  <FontAwesomeIcon icon={faPlus} />
                </Button>
              </div>
            </Col>
          ))}
        </>
      )}
    </>
  )
}

const emptyDashboardDataRow: DashboardDataRow = {
  id: '',
  site: {
    id: '',
    url: '',
    seo_status: ''
  },
  seo_data: null,
  webmasters: [],
  projects: []
}

function DashboardForm({
  page_obj,
  endpointName,
  useModal,
  showModal,
  onClose
}: DashboardFormProps) {
  const [show, setShow] = useState(showModal)
  const [form, setForm] = useState(
    page_obj ? page_obj : { ...emptyDashboardDataRow }
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
      disabled={form.site?.url === ''}
    >
      {form.id ? 'Update' : 'Add'}
    </Button>
  )

  return useModal ? (
    <ModalBase
      show={show}
      title='Website'
      handleClose={handleClose}
      customButton={formButtons}
      widthSize='70'
    >
      <DashboardFormContent
        form={form}
        handleSubmit={handleSubmit}
        updateFormValue={updateFormValue}
      />
    </ModalBase>
  ) : (
    <DashboardFormContent
      form={form}
      handleSubmit={handleSubmit}
      updateFormValue={updateFormValue}
      buttons={formButtons}
    />
  )
}

export default DashboardForm
