import { useState } from 'react'
import { Button, Stack } from 'react-bootstrap'
import useSWR from 'swr'

import ProjectModal from '../components/project/ProjectModal'
import ProjectTable from '../components/project/ProjectTable'
import { fetcher } from '../helper/axios'

function Project() {
  const endpointName = 'project'
  const [data, setData] = useState([])
  const [perPage, setPerPage] = useState(10)
  const [offset, setOffset] = useState(0)
  const [isFormOpen, setFormOpen] = useState(false)

  const response = useSWR(
    `${endpointName}/?limit=${perPage}&offset=${offset * perPage}`,
    fetcher,
    {
      refreshInterval: 10000,
      onSuccess: (data) => {
        setData(data?.results)
      }
    }
  )

  const handlerChange = (offset: number, perPage: number) => {
    setOffset(offset)
    setPerPage(perPage)
  }

  const handleAddClick = () => {
    setFormOpen(true)
  }

  const closeForm = () => {
    response.mutate()
    setFormOpen(false)
  }

  return (
    <>
      <Stack direction='horizontal' gap={3}>
        <Button
          variant='primary'
          size='sm'
          className='p-2 ms-auto'
          onClick={handleAddClick}
        >
          Add new project
        </Button>
        {isFormOpen && (
          <ProjectModal
            endpointName={endpointName}
            showModal={isFormOpen}
            onClose={closeForm}
          />
        )}
      </Stack>
      <ProjectTable
        data={data}
        endpointName={endpointName}
        response={response}
        perPage={perPage}
        handlerChange={handlerChange}
      />
    </>
  )
}

export default Project
