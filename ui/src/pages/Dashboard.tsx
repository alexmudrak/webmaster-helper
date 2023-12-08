import { useState } from 'react'
import { Button, Stack } from 'react-bootstrap'
import useSWR from 'swr'

import DashboardModal from '../components/dashboard/DashboardModal'
import DashboardTable from '../components/dashboard/DashboardTable'
import { fetcher } from '../helper/axios'

// TODO: Add types
function Dashboard() {
  const endpointName = 'url'
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
          Add new site
        </Button>
        {isFormOpen && (
          <DashboardModal
            showModal={isFormOpen}
            endpointName={endpointName}
            onClose={closeForm}
          />
        )}
      </Stack>
      <DashboardTable
        data={data}
        endpointName={endpointName}
        response={response}
        perPage={perPage}
        handlerChange={handlerChange}
      />
    </>
  )
}

export default Dashboard
