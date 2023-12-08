import { useEffect, useState } from 'react'
import { Form } from 'react-bootstrap'
import Select from 'react-select'

import { SingleSelectFieldProps } from '../../types'
// TODO: Add typescript

function SingleChoiceField({
  label,
  placeholder,
  values,
  selectedValues,
  onChange
}: SingleSelectFieldProps) {
  const [options, setOptions] = useState([])
  const [inputValue, setInputValue] = useState()

  useEffect(() => {
    const valueOptions = values.map((value) => ({
      value: value?.id,
      label: value?.name
    }))

    setOptions(valueOptions)
    setInputValue({ value: selectedValues?.id, label: selectedValues?.name })
  }, [values, selectedValues])

  const handleSelectChange = (selectedOption) => {
    onChange({
      id: selectedOption?.value,
      name: selectedOption?.label
    })
    setInputValue(selectedOption)
  }

  return (
    <Form.Group className='mb-3'>
      {label && <Form.Label>{label}</Form.Label>}
      <Select
        options={options}
        value={inputValue?.value !== undefined ? inputValue : null}
        onChange={handleSelectChange}
        placeholder={placeholder}
      />
    </Form.Group>
  )
}
export default SingleChoiceField
