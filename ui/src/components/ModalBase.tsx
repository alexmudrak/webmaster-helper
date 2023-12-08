import '../style.css'

import { ReactNode } from 'react'
import { Modal } from 'react-bootstrap'

type ModalBaseProps = {
  show: boolean
  title: string
  children: ReactNode
  customButton: ReactNode
  handleClose: () => void
  widthSize?: string
}

const ModalBase = ({
  show,
  title,
  children,
  customButton,
  handleClose,
  widthSize = '50'
}: ModalBaseProps) => {
  return (
    <Modal
      show={show}
      onHide={handleClose}
      dialogClassName={`modal-${widthSize}w mx-auto mt-3`}
    >
      <Modal.Header closeButton className='border-0'>
        <Modal.Title>
          <b>{title}</b>
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>{children}</Modal.Body>
      <Modal.Footer>{customButton}</Modal.Footer>
    </Modal>
  )
}

export default ModalBase
