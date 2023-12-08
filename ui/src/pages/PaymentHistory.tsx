import { useState } from 'react'
import { Button, Stack } from 'react-bootstrap'
import useSWR from 'swr'

import PaymentHistoryModal from '../components/payment_history/PaymentHistoryModal'
import PaymentHistoryTable from '../components/payment_history/PaymentHistoryTable'
import { fetcher } from '../helper/axios'

function PaymentHistory() {
  const endpointName = 'payment-history'
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
          Add new payment
        </Button>
        {isFormOpen && (
          <PaymentHistoryModal
            endpointName={endpointName}
            showModal={isFormOpen}
            onClose={closeForm}
          />
        )}
      </Stack>
      <PaymentHistoryTable
        data={data}
        endpointName={endpointName}
        response={response}
        perPage={perPage}
        handlerChange={handlerChange}
      />
    </>
  )
}

export default PaymentHistory
