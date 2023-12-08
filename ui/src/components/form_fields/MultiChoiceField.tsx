import { useEffect, useState } from 'react'
import { Form } from 'react-bootstrap'
import CreatableSelect from 'react-select'
// TODO: Add typescript

function MultiSelectField({
  label,
  placeholder,
  values,
  selectedValues,
  onChange
}) {
  const [options, setOptions] = useState([])
  const [inputValue, setInputValue] = useState('')

  useEffect(() => {
    const valueOptions = values.map((value) => ({
      value: value.id,
      label: value.name
    }))

    setOptions(valueOptions)
  }, [values])

  const handleSelectChange = (selectedOption) => {
    onChange(
      selectedOption.map((option) => ({
        id: option.value,
        name: option.label
      }))
    )
  }
  const handleInputChange = (input) => {
    setInputValue(input)
  }
  const handleCreateOption = () => {
    onChange([...selectedValues, { id: null, name: inputValue }])
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleCreateOption()
    }
  }

  return (
    <Form.Group className='mb-3'>
      <Form.Label>{label}</Form.Label>
      <CreatableSelect
        isMulti
        options={options}
        value={selectedValues.map((value) => ({
          value: value.id,
          label: value.name
        }))}
        onChange={handleSelectChange}
        onInputChange={handleInputChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        isClearable
      />
    </Form.Group>
  )
}
export default MultiSelectField
