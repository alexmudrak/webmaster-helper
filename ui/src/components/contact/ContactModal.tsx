import { ContactFormProps } from '../../types'
import ContactForm from './ContactForm'

function ContactModal({
  page_obj,
  endpointName,
  showModal,
  onClose
}: ContactFormProps) {
  return (
    <ContactForm
      page_obj={page_obj}
      endpointName={endpointName}
      useModal={true}
      showModal={showModal}
      onClose={onClose}
    />
  )
}

export default ContactModal
