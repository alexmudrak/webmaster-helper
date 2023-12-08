import {
  faEnvelope,
  faMagnifyingGlass,
  faMagnifyingGlassChart,
  faPenToSquare,
  faTrash
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useEffect, useState } from 'react'
import { Button, OverlayTrigger, Spinner, Tooltip } from 'react-bootstrap'

import axiosService from '../../helper/axios'
import { DashboardActionButtonsProps } from '../../types'
import ContactHistoryModal from '../contact_history/ContactHistoryModal'
import ModalBase from '../ModalBase'
import DashboardModal from './DashboardModal'

function DashboardActionButtons({
  endpointName,
  object,
  refresh
}: DashboardActionButtonsProps) {
  const [isFormOpen, setFormOpen] = useState(false)
  const [isMessageFormOpen, setMessageFormOpen] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [checkLinksStatus, setCheckLinksStatus] = useState(true)
  const messageObject = {
    webmaster: {
      id: object.webmasters[0]?.id,
      name: object.webmasters[0]?.name
    },
    website: { id: object.id, name: object.site.url }
  }

  useEffect(() => {
    let hasNonDoneStatus = false

    object.projects?.forEach((project) => {
      project?.publish_pages?.forEach((page) => {
        if (page?.check_status !== null && page?.check_status !== 'DONE') {
          hasNonDoneStatus = true
        }
      })
    })

    setCheckLinksStatus(!hasNonDoneStatus)
  }, [object])

  const handleEdit = () => {
    setFormOpen(true)
  }

  const handleContact = () => {
    setMessageFormOpen(true)
  }

  const closeForm = () => {
    refresh()
    setFormOpen(false)
    setMessageFormOpen(false)
  }

  const handleShowDeleteModal = () => {
    setShowDeleteModal(true)
  }

  const handleCloseDeleteModal = () => {
    setShowDeleteModal(false)
  }

  const handleConfirmDelete = () => {
    handleCloseDeleteModal()
    axiosService
      .delete(`/${endpointName}/${object.id}/`)
      .then(() => {
        console.log(`Delete ${endpointName}:`, object.id)
        refresh()
      })
      .catch((err) => console.error(err))
  }

  const handleClickRunSeoTask = (urlId: string) => {
    axiosService
      .post(`/${endpointName}/${urlId}/run-seo-task/`)
      .then(() => {
        console.log('Send the task for getting seo data')
        refresh()
      })
      .catch(() => {
        console.log('Error sending task for getting seo data')
      })
  }

  const handleClickRunCheckLinks = (urlId: string) => {
    axiosService
      .post(`/${endpointName}/${urlId}/run-check-links/`)
      .then(() => {
        console.log('Send the task for checking links', urlId)
        refresh()
      })
      .catch((err) => {
        console.log('Error sending task for checking links', urlId, err)
      })
  }

  const renderTooltip = (tooltipText: string) => (
    <Tooltip id='button-tooltip'>{tooltipText}</Tooltip>
  )
  return (
    <>
      <div className='d-flex justify-content-between align-items-center'>
        <OverlayTrigger
          placement='top'
          delay={{ show: 250, hide: 400 }}
          overlay={renderTooltip(`Send message`)}
        >
          <Button variant='primary' size='sm' onClick={handleContact}>
            <FontAwesomeIcon icon={faEnvelope} />
          </Button>
        </OverlayTrigger>

        <div className='vr m-2' />

        <OverlayTrigger
          placement='top'
          delay={{ show: 250, hide: 400 }}
          overlay={renderTooltip('Check publish links')}
        >
          {!checkLinksStatus ? (
            <Button variant='warning' size='sm' disabled>
              <Spinner
                as='span'
                animation='border'
                size='sm'
                role='status'
                aria-hidden='true'
              />{' '}
              <span className='visually-hidden'>Loading...</span>
            </Button>
          ) : (
            <Button
              variant='warning'
              onClick={() => handleClickRunCheckLinks(object.id)}
              size='sm'
            >
              <FontAwesomeIcon icon={faMagnifyingGlass} />
            </Button>
          )}
        </OverlayTrigger>

        <div className='vr m-2' />

        <OverlayTrigger
          placement='top'
          delay={{ show: 250, hide: 400 }}
          overlay={renderTooltip('Check SEO metrics')}
        >
          {object.site.seo_status !== 'DONE' ? (
            <Button variant='success' size='sm' disabled>
              <Spinner
                as='span'
                animation='border'
                size='sm'
                role='status'
                aria-hidden='true'
              />{' '}
              <span className='visually-hidden'>Loading...</span>
            </Button>
          ) : (
            <Button
              variant='success'
              onClick={() => handleClickRunSeoTask(object.site.id)}
              size='sm'
            >
              <FontAwesomeIcon icon={faMagnifyingGlassChart} />
            </Button>
          )}
        </OverlayTrigger>

        <div className='vr m-2' />

        <Button variant='dark' size='sm' onClick={handleEdit}>
          <FontAwesomeIcon icon={faPenToSquare} />
        </Button>

        <div className='vr m-2' />

        <Button variant='danger' size='sm' onClick={handleShowDeleteModal}>
          <FontAwesomeIcon icon={faTrash} />
        </Button>
      </div>

      <ModalBase
        title='Confirm Delete'
        show={showDeleteModal}
        handleClose={handleCloseDeleteModal}
        customButton={
          <>
            <Button variant='secondary' onClick={handleCloseDeleteModal}>
              Cancel
            </Button>
            <Button variant='danger' onClick={handleConfirmDelete}>
              Delete
            </Button>
          </>
        }
      >
        <>Are you sure you want to delete this {endpointName}?</>
      </ModalBase>

      {isFormOpen && (
        <DashboardModal
          page_obj={object}
          endpointName={endpointName}
          showModal={isFormOpen}
          onClose={closeForm}
        />
      )}
      {isMessageFormOpen && (
        <ContactHistoryModal
          page_obj={messageObject}
          endpointName='messages'
          showModal={isMessageFormOpen}
          onClose={closeForm}
        />
      )}
    </>
  )
}

export default DashboardActionButtons
