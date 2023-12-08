import { faEye } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { Button, OverlayTrigger, Tooltip } from 'react-bootstrap'

import { MailActionButtonsProps } from '../../types'

function MailActionButtons({
  endpointName,
  object,
  refresh
}: MailActionButtonsProps) {
  const handleConversation = () => {
    console.log('Open modal with contact form and conversation')
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
          overlay={renderTooltip(`Check as read`)}
        >
          <Button variant='primary' size='sm' onClick={handleConversation}>
            <FontAwesomeIcon icon={faEye} />
          </Button>
        </OverlayTrigger>

      </div>
    </>
  )
}

export default MailActionButtons
