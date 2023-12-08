import { faPenToSquare, faTrash } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useState } from 'react'
import { Button } from 'react-bootstrap'

import axiosService from '../../helper/axios'
import { ContactHistoryActionButtonsProps } from '../../types'
import CustomTooltip from '../CustomTooltip'
import ModalBase from '../ModalBase'
import ContactHistoryModal from './ContactHistoryModal'

function ContactHistoryActionButtons({
  endpointName,
  object,
  refresh
}: ContactHistoryActionButtonsProps) {
  const [isFormOpen, setFormOpen] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)

  const handleEdit = () => {
    setFormOpen(true)
  }

  const closeForm = () => {
    refresh()
    setFormOpen(false)
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

  return (
    <>
      <div className='d-flex justify-content-between align-items-center'>
        <CustomTooltip
          placement='top'
          delay={{ show: 250, hide: 400 }}
          tooltipText='Edit message'
        >
          <Button variant='dark' size='sm' onClick={handleEdit}>
            <FontAwesomeIcon icon={faPenToSquare} />
          </Button>
        </CustomTooltip>
        <div className='vr m-2' />

        <CustomTooltip
          placement='top'
          delay={{ show: 250, hide: 400 }}
          tooltipText='Delete message'
        >
          <Button variant='danger' size='sm' onClick={handleShowDeleteModal}>
            <FontAwesomeIcon icon={faTrash} />
          </Button>
        </CustomTooltip>
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
        <ContactHistoryModal
          page_obj={object}
          endpointName={endpointName}
          showModal={isFormOpen}
          onClose={closeForm}
        />
      )}
    </>
  )
}

export default ContactHistoryActionButtons
