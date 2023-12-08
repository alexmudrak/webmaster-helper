import { FC } from 'react'
import { Form } from 'react-bootstrap'

import { FormFieldProps } from '../../types'

const FormTextarea: FC<FormFieldProps> = ({
  label,
  placeholder,
  value,
  onChange,
  rowsCount = 3,
  disabled = false,
}) => (
  <Form.Group className='mb-3'>
    {label && <Form.Label>{label}</Form.Label>}
    <Form.Control
      as='textarea'
      placeholder={placeholder}
      rows={rowsCount}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      disabled={disabled}
    />
  </Form.Group>
)

export default FormTextarea
