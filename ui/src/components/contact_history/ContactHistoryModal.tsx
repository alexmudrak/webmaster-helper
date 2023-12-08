import { ContactHistoryFormProps } from '../../types'
import ContactHistoryForm from './ContactHistoryForm'

function ContactHistoryModal({
  page_obj,
  endpointName,
  showModal,
  onClose
}: ContactHistoryFormProps) {
  return (
    <ContactHistoryForm
      page_obj={page_obj}
      endpointName={endpointName}
      useModal={true}
      showModal={showModal}
      onClose={onClose}
    />
  )
}

export default ContactHistoryModal
