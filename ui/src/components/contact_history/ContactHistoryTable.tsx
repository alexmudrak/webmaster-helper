import { TableColumn } from 'react-data-table-component'

import { formatDate } from '../../helper/dateUtils'
import { ContactHistoryDataRow, ContactHistoryTableProps } from '../../types'
import CustomTooltip from '../CustomTooltip'
import TableBase from '../TableBase'
import ContactHistoryActionButtons from './ContactHistoryActionButtons'

function ContactHistoryTable({
  data,
  endpointName,
  response,
  perPage,
  handlerChange
}: ContactHistoryTableProps) {
  const dateSort = (rowA, rowB) => {
    const dateA = new Date(rowA.created)
    const dateB = new Date(rowB.created)

    if (dateA < dateB) {
      return -1
    }
    if (dateA > dateB) {
      return 1
    }
    return 0
  }
  const columns: TableColumn<ContactHistoryDataRow>[] = [
    {
      name: 'Date',
      selector: (row) => formatDate(row.created),
      sortable: true,
      width: '170px',
      sortFunction: dateSort
    },
    {
      name: 'Subject',
      cell: (row) => (
        <CustomTooltip
          placement='top'
          delay={{ show: 250, hide: 400 }}
          tooltipText={row.body}
        >
          <a href='#'>{row.subject}</a>
        </CustomTooltip>
      ),
      sortable: false,
      width: '120px'
    },
    {
      name: 'Webmaster',
      selector: (row) => row.webmaster?.name || '-',
      sortable: true,
      width: '120px'
    },
    {
      name: 'Website',
      selector: (row) => row.website?.name || '-',
      sortable: true,
      width: '120px'
    },
    {
      name: 'Project',
      selector: (row) => row.project?.name || '-',
      sortable: true,
      width: '120px'
    },
    {
      name: 'Contact type',
      selector: (row) => row.contact.type,
      width: '120px'
    },
    {
      name: 'Contact',
      selector: (row) => row.contact.contact
    },
    {
      name: 'Action',
      cell: (row) => (
        <ContactHistoryActionButtons
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
      title='Contact history'
      columns={columns}
      data={data}
      totalRows={response?.data?.count || 0}
      perPageCount={perPage}
      handlerChange={handlerChange}
      sortAsc={false}
    />
  )
}

export default ContactHistoryTable
