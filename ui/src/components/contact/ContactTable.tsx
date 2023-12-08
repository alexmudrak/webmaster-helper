import { TableColumn } from 'react-data-table-component'

import { formatDate } from '../../helper/dateUtils'
import { ContactDataRow, ContactTableProps } from '../../types'
import TableBase from '../TableBase'
import ContactActionButtons from './ContactActionButtons'

function ContactTable({
  data,
  endpointName,
  response,
  perPage,
  handlerChange
}: ContactTableProps) {
  const columns: TableColumn<ContactDataRow>[] = [
    {
      name: 'Webmaster',
      selector: (row) => row.webmaster?.name,
      sortable: true,
      width: '170px'
    },
    {
      name: 'Type',
      selector: (row) => row.type,
      sortable: false,
      width: '120px'
    },
    {
      name: 'Contact',
      selector: (row) => row.contact,
      sortable: false,
      width: '170px'
    },
    {
      name: 'Update date',
      selector: (row) => formatDate(row.updated),
      sortable: true,
      width: '170px'
    },
    {
      name: 'Last contact date',
      cell: (row) =>
        row.last_contact_date !== null
          ? formatDate(row.last_contact_date)
          : 'No latest contact'
    },
    {
      name: 'Action',
      cell: (row) => (
        <ContactActionButtons
          endpointName={endpointName}
          object={row}
          refresh={response.mutate}
        />
      ),
      width: '270px',
      ignoreRowClick: true,
      allowOverflow: true,
      button: true
    }
  ]

  return (
    <TableBase
      title='Contacts'
      columns={columns}
      data={data}
      totalRows={response?.data?.count || 0}
      perPageCount={perPage}
      handlerChange={handlerChange}
    />
  )
}

export default ContactTable
