import { FC } from 'react'
import { OverlayTrigger, Tooltip } from 'react-bootstrap'

import { CustomTooltipProps } from '../types'

const CustomTooltip: FC<CustomTooltipProps> = ({
  placement,
  delay,
  tooltipText,
  children
}) => (
  <OverlayTrigger
    placement={placement}
    delay={delay}
    overlay={<Tooltip id='button-tooltip'>{tooltipText}</Tooltip>}
  >
    {children}
  </OverlayTrigger>
)

export default CustomTooltip
