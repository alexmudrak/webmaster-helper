import {
  faEnvelope,
  faPenToSquare,
  faTrash
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useState } from 'react'
import { Button, OverlayTrigger, Tooltip } from 'react-bootstrap'

import axiosService from '../../helper/axios'
import { WebmasterActionButtonsProps } from '../../types'
import ContactHistoryModal from '../contact_history/ContactHistoryModal'
import ModalBase from '../ModalBase'
import WebmasterModal from './WebmasterModal'

function WebmasterActionButtons({
  endpointName,
  object,
  refresh
}: WebmasterActionButtonsProps) {
  const [isFormOpen, setFormOpen] = useState(false)
  const [isMessageFormOpen, setMessageFormOpen] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const messageObject = {
    webmaster: {id: object.id, name: object.name},
  }

  const handleContact = () => {
    setMessageFormOpen(true)
  }

  const handleEdit = () => {
    setFormOpen(true)
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
          overlay={renderTooltip(`Edit the ${endpointName}`)}
        >
          <Button variant='dark' size='sm' onClick={handleEdit}>
            <FontAwesomeIcon icon={faPenToSquare} />
          </Button>
        </OverlayTrigger>

        <div className='vr m-2' />

        <OverlayTrigger
          placement='top'
          delay={{ show: 250, hide: 400 }}
          overlay={renderTooltip(`Delete the ${endpointName}`)}
        >
          <Button variant='danger' size='sm' onClick={handleShowDeleteModal}>
            <FontAwesomeIcon icon={faTrash} />
          </Button>
        </OverlayTrigger>
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
        <WebmasterModal
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

export default WebmasterActionButtons
