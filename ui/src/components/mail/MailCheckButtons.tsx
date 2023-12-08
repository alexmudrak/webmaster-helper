import { useState } from 'react'
import { Badge, Button, Spinner } from 'react-bootstrap'
import useSWR from 'swr'

import { fetcher } from '../../helper/axios'
import { useMailActions } from '../../hooks/mail.actions'

function MailCheckButtons() {
  const { runMailCollectors } = useMailActions()
  const [settingsData, setSettingsData] = useState([])
  const [loading, setLoading] = useState(true)

  const response = useSWR(`/mails/get-mailbox-status/`, fetcher, {
    refreshInterval: 10000,
    onSuccess: (data) => {
      setSettingsData(data)
      const allDone = data.every((mailbox) => mailbox.status === 'DONE')
      setLoading(!allDone)
    },
    onError: (error) => {
      console.error('Error fetching data:', error)
      setSettingsData([])
    }
  })

  const handleCheckClick = async () => {

    try {
      setLoading(true)
      await runMailCollectors()
      response?.mutate()
    } catch (error) {
      console.error('Error during API request:', error)
    }
  }

  return (
    <>
      <div className='border p-2'>
        {settingsData.map((mailbox) => (
          <div key={mailbox?.mailbox} className='mt-1 d-flex justify-content-end'>
            {mailbox?.mailbox}
            {' - '}
            <Badge bg={mailbox?.status === 'DONE' ? 'success' : 'secondary'}>
              {mailbox?.status}
            </Badge>
          </div>
        ))}
      </div>

      <Button
        variant='warning'
        size='sm'
        className='p-2 ms-auto'
        onClick={handleCheckClick}
        disabled={loading}
      >
        {loading ? (
          <>
            <Spinner
              as='span'
              animation='border'
              size='sm'
              role='status'
              aria-hidden='true'
              className='me-1'
            />
            Checking mails...
          </>
        ) : (
          'Check mails'
        )}
      </Button>
    </>
  )
}

export default MailCheckButtons
