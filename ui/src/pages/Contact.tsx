import { useState } from 'react'
import { Button, Stack, Tab, Tabs } from 'react-bootstrap'
import useSWR from 'swr'

import ContactModal from '../components/contact/ContactModal'
import ContactTable from '../components/contact/ContactTable'
import ContactHistoryModal from '../components/contact_history/ContactHistoryModal'
import ContactHistoryTable from '../components/contact_history/ContactHistoryTable'
import MailCheckButtons from '../components/mail/MailCheckButtons'
import MailTable from '../components/mail/MailTable'
import { fetcher } from '../helper/axios'

// TODO: Add types
function useDataFetching(endpoint, perPage, offset, onDataSuccess) {
  const response = useSWR(
    `/${endpoint}/?limit=${perPage}&offset=${offset * perPage}`,
    fetcher,
    {
      refreshInterval: 10000,
      onSuccess: (data) => {
        onDataSuccess(data?.results)
      },
      onError: (error) => {
        console.error('Error fetching data:', error)
        onDataSuccess([])
      }
    }
  )

  return response
}

function Contact() {
  const [endpointName, setEndpointName] = useState('contact')
  const [contactsData, setContactsData] = useState([])
  const [contactHistoryData, setContactHistoryData] = useState([])
  const [mailsData, setMailsData] = useState([])
  const [perPage, setPerPage] = useState(10)
  const [offset, setOffset] = useState(0)
  const [activeTab, setActiveTab] = useState('contact')
  const [isFormOpen, setFormOpen] = useState(false)

  const getResponse = () => {
    switch (activeTab) {
      case 'contact':
        return useDataFetching(endpointName, perPage, offset, (data) =>
          setContactsData(data)
        )
      case 'messages':
        return useDataFetching(endpointName, perPage, offset, (data) =>
          setContactHistoryData(data)
        )
      case 'mails':
        return useDataFetching(endpointName, perPage, offset, (data) =>
          setMailsData(data)
        )
      default:
        return null
    }
  }

  const modalComponents = {
    contact: ContactModal,
    messages: ContactHistoryModal
  }

  const handlerChange = (offset: number, perPage: number) => {
    setOffset(offset)
    setPerPage(perPage)
  }

  const handleTabChange = (key: string) => {
    setActiveTab(key)
    setEndpointName(key)
  }

  const handleAddClick = () => {
    setFormOpen(true)
  }

  const closeForm = () => {
    response?.mutate()
    setFormOpen(false)
  }

  const getModalComponent = () => {
    const ModalComponent = modalComponents[activeTab]
    return ModalComponent || null
  }

  const ModalComponent = getModalComponent()

  const response = getResponse()

  return (
    <>
      <Stack direction='horizontal' gap={3}>
        {activeTab !== 'mails' && (
          <Button
            variant='primary'
            size='sm'
            className='p-2 ms-auto'
            onClick={handleAddClick}
          >
            {`Add new ${activeTab}`}
          </Button>
        )}
        {isFormOpen && ModalComponent && (
          <ModalComponent
            showModal={isFormOpen}
            endpointName={endpointName}
            onClose={closeForm}
          />
        )}
        {activeTab === 'mails' && <MailCheckButtons />}
      </Stack>
      <Tabs
        onSelect={handleTabChange}
        defaultActiveKey={activeTab}
        id='justify-tab-example'
        className='my-3'
        justify
      >
        <Tab eventKey='contact' title='Contacts'>
          <ContactTable
            data={contactsData}
            endpointName={endpointName}
            response={response}
            perPage={perPage}
            handlerChange={handlerChange}
          />
        </Tab>
        <Tab eventKey='messages' title='Contact history'>
          <ContactHistoryTable
            data={contactHistoryData}
            endpointName={endpointName}
            response={response}
            perPage={perPage}
            handlerChange={handlerChange}
          />
        </Tab>
        <Tab eventKey='mails' title='Mails'>
          <MailTable
            data={mailsData}
            endpointName={endpointName}
            response={response}
            perPage={perPage}
            handlerChange={handlerChange}
          />
        </Tab>
      </Tabs>
    </>
  )
}

export default Contact
