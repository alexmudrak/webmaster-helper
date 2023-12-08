import { ProjectFormProps } from '../../types'
import ProjectForm from './ProjectForm'

function ProjectModal({
  page_obj,
  endpointName,
  showModal,
  onClose
}: ProjectFormProps) {
  return (
    <ProjectForm
      page_obj={page_obj}
      endpointName={endpointName}
      useModal={true}
      showModal={showModal}
      onClose={onClose}
    />
  )
}

export default ProjectModal
