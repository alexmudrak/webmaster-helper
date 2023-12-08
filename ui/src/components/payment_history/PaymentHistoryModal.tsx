import { PaymentHistoryFormProps } from '../../types'
import PaymentHistoryForm from './PaymentHistoryForm'

function PaymentHistoryModal({
  page_obj,
  endpointName,
  showModal,
  onClose
}: PaymentHistoryFormProps) {
  return (
    <PaymentHistoryForm
      page_obj={page_obj}
      endpointName={endpointName}
      useModal={true}
      showModal={showModal}
      onClose={onClose}
    />
  )
}

export default PaymentHistoryModal
