import { TableColumn } from 'react-data-table-component'

import { formatDate } from '../../helper/dateUtils'
import { PaymentHistoryDataRow, PaymentHistoryTableProps } from '../../types'
import TableBase from '../TableBase'
import PaymentHistoryActionButtons from './PaymentHistoryActionButtons'

function PaymentHistoryTable({
  data,
  endpointName,
  response,
  perPage,
  handlerChange
}: PaymentHistoryTableProps) {
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
  const columns: TableColumn<PaymentHistoryDataRow>[] = [
    {
      name: 'Date',
      selector: (row) => formatDate(row.created),
      sortable: true,
      width: '170px',
      sortFunction: dateSort
    },
    {
      name: 'Webmaster',
      selector: (row) => row.webmaster.name,
      sortable: true,
      width: '120px'
    },
    {
      name: 'Website',
      selector: (row) => row.website.name,
      sortable: true,
      width: '170px'
    },
    {
      name: 'Project',
      selector: (row) => row.project.name,
      sortable: true,
      width: '120px'
    },
    {
      name: 'Payment',
      selector: (row) => row.payment.type + ' - ' + row.payment.detail,
      width: '200px'
    },
    {
      name: 'Value',
      selector: (row) => row.price + '$',
      sortable: true
    },
    {
      name: 'Action',
      cell: (row) => (
        <PaymentHistoryActionButtons
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
      title='Payment history'
      columns={columns}
      data={data}
      totalRows={response?.data?.count || 0}
      perPageCount={perPage}
      handlerChange={handlerChange}
      sortAsc={false}
    />
  )
}

export default PaymentHistoryTable
