import { FC } from 'react'
import { Form } from 'react-bootstrap'

import { FormFieldProps } from '../../types'

const FormField: FC<FormFieldProps> = ({
  label,
  type,
  placeholder,
  value,
  onChange,
  disabled = false
}) => (
  <Form.Group className='mb-3'>
    {label && <Form.Label>{label}</Form.Label>}
    <Form.Control
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      disabled={disabled}
    />
  </Form.Group>
)

export default FormField
