import { faCircleCheck } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { TableColumn } from 'react-data-table-component'

import { formatDate } from '../../helper/dateUtils'
import { ProjectDataRow, ProjectTableProps } from '../../types'
import TableBase from '../TableBase'
import ProjectActionButtons from './ProjectActionButtons'

function ProjectTable({
  data,
  endpointName,
  response,
  perPage,
  handlerChange
}: ProjectTableProps) {
  const columns: TableColumn<ProjectDataRow>[] = [
    {
      name: 'Project name',
      selector: (row) => row.name,
      sortable: true,
      maxWidth: '150px'
    },
    {
      name: 'Url',
      cell: (row) => row.url?.url,
      width: '150px'
    },
    {
      name: 'Published count',
      cell: (row) => row.published_count,
      maxWidth: '100px'
    },
    {
      name: 'Spend value',
      selector: (row) => row.total_spend + '$',
      sortable: true,
      maxWidth: '100px'
    },
    {
      name: 'Create date',
      selector: (row) => formatDate(row.created),
      sortable: true,
      maxWidth: '170px'
    },
    {
      name: 'Last published date',
      selector: (row) => formatDate(row.last_published_date),
      sortable: true,
      maxWidth: '170px'
    },
    {
      name: 'Use mail',
      cell: (row) => (
        <div>
          {row.mail_settings ? (
            <FontAwesomeIcon icon={faCircleCheck} />
          ) : (
            <span>-</span>
          )}
        </div>
      )
    },
    {
      name: 'Actions',
      cell: (row) => (
        <ProjectActionButtons
          endpointName={endpointName}
          object={row}
          refresh={response.mutate}
        />
      ),
      width: '200px',
      ignoreRowClick: true,
      allowOverflow: true,
      button: true
    }
  ]

  return (
    <TableBase
      title='Project'
      columns={columns}
      data={data}
      totalRows={response?.data?.count || 0}
      perPageCount={perPage}
      handlerChange={handlerChange}
    />
  )
}

export default ProjectTable
