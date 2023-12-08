import { useState } from 'react'
import DataTable from 'react-data-table-component'

import { TableBaseProps } from '../types'

function TableBase<T>({
  title,
  columns,
  data,
  totalRows,
  perPageCount,
  handlerChange,
  sortColumnNumber=1,
  sortAsc=true
}: TableBaseProps<T>) {
  const [perPage, setPerPage] = useState(perPageCount)

  const fetchSites = async (page: number) => {
    handlerChange(page - 1, perPage)
  }

  const handlePageChange = (page: number) => {
    fetchSites(page)
  }

  const handlePerRowsChange = async (newPerPage: number, page: number) => {
    setPerPage(newPerPage)
    handlerChange(page - 1, newPerPage)
  }

  return (
    <DataTable
      title={title}
      columns={columns}
      data={data}
      pagination
      paginationServer
      paginationRowsPerPageOptions={[1, 3, 5, 10, 20, 30]}
      paginationPerPage={perPage}
      paginationTotalRows={totalRows}
      onChangeRowsPerPage={handlePerRowsChange}
      onChangePage={handlePageChange}
      defaultSortFieldId={sortColumnNumber}
      defaultSortAsc={sortAsc}
    />
  )
}

export default TableBase
