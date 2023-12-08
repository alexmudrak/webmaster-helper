import { TableColumn } from 'react-data-table-component'

import { formatDate } from '../../helper/dateUtils'
import { WebmasterDataRow, WebmasterTableProps } from '../../types'
import TableBase from '../TableBase'
import WebmasterActionButtons from './WebmasterActionButtons'

function WebmasterTable({
  data,
  endpointName,
  response,
  perPage,
  handlerChange
}: WebmasterTableProps) {
  const columns: TableColumn<WebmasterDataRow>[] = [
    { name: 'Webmaster', sortable: true, selector: (row) => row.name },
    {
      name: 'Count of Websites',
      sortable: true,
      selector: (row) => row.websites.length
    },
    {
      name: 'Spend Value',
      sortable: true,
      selector: (row) =>
        row.payments.reduce((sum, item) => sum + item.total_spend, 0) + '$'
    },
    {
      name: 'Last Contact Date',
      sortable: false,
      width: '350px',
      cell: (row) => {
        const sortedProjects = row.contacts.sort((a, b) =>
          a.type.localeCompare(b.type)
        )

        const contactList = sortedProjects.map((project) => {
          const { type, contact, latest_contact } = project
          return `<li>${type} - ${contact} - ${
            latest_contact !== null ? formatDate(latest_contact) : 'No latest contact'
          }</li>`
        })

        return (
          <ul dangerouslySetInnerHTML={{ __html: contactList.join('') }} />
        )
      }
    },
    {
      name: 'Action',
      cell: (row) => (
        <WebmasterActionButtons
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
      title='Webmasters'
      columns={columns}
      data={data}
      totalRows={response?.data?.count || 0}
      perPageCount={perPage}
      handlerChange={handlerChange}
    />
  )
}

export default WebmasterTable
