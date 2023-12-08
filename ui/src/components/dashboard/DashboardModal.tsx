import { DashboardFormProps } from '../../types'
import DashboardForm from './DashboardForm'

function DashboardModal({
  page_obj,
  endpointName,
  showModal,
  onClose
}: DashboardFormProps) {
  return (
    <DashboardForm
      page_obj={page_obj}
      endpointName={endpointName}
      useModal={true}
      showModal={showModal}
      onClose={onClose}
    />
  )
}

export default DashboardModal
