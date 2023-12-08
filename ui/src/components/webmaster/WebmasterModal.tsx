import { WebmasterFormProps } from '../../types'
import WebmasterForm from './WebmasterForm'

function WebmasterModal({
  page_obj,
  endpointName,
  showModal,
  onClose
}: WebmasterFormProps) {
  return (
    <WebmasterForm
      page_obj={page_obj}
      endpointName={endpointName}
      useModal={true}
      showModal={showModal}
      onClose={onClose}
    />
  )
}

export default WebmasterModal
