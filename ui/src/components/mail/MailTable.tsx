import { TableColumn } from 'react-data-table-component'

import { formatDate } from '../../helper/dateUtils'
import { MailDataRow, MailTableProps } from '../../types'
import TableBase from '../TableBase'
import MailActionButtons from './MailActionButtons'

function MailTable({
  data,
  endpointName,
  response,
  perPage,
  handlerChange
}: MailTableProps) {
  const dateSort = (rowA: MailDataRow, rowB: MailDataRow) => {
    const dateA = new Date(rowA.receive_date)
    const dateB = new Date(rowB.receive_date)

    if (dateA < dateB) {
      return -1
    }
    if (dateA > dateB) {
      return 1
    }
    return 0
  }
  const columns: TableColumn<MailDataRow>[] = [
    {
      name: 'Date',
      selector: (row) => formatDate(row.receive_date),
      sortable: true,
      width: '110px',
      sortFunction: dateSort
    },
    {
      name: 'Account',
      selector: (row) => row.account_name,
      width: '150px'
    },
    {
      name: 'Mail box',
      selector: (row) => row.mail_box,
      width: '150px'
    },
    {
      name: 'From',
      selector: (row) => row.author_mail,
      width: '200px'
    },
    {
      name: 'To',
      selector: (row) => row.replay_to,
      width: '150px'
    },
    {
      name: 'Subject',
      selector: (row) => row.subject
    },
    {
      name: 'Action',
      cell: (row) => (
        <MailActionButtons
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
      title='Mails'
      columns={columns}
      data={data}
      totalRows={response?.data?.count || 0}
      perPageCount={perPage}
      handlerChange={handlerChange}
      sortAsc={false}
    />
  )
}

export default MailTable
