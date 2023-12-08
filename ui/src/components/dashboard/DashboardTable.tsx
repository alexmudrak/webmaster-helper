import { TableColumn } from 'react-data-table-component'

import { formatDate } from '../../helper/dateUtils'
import { DashboardDataRow, DashboardTableProps } from '../../types'
import TableBase from '../TableBase'
import DashboardActionButtons from './DashboardActionButtons'

function DashboardTable({
  data,
  endpointName,
  response,
  perPage,
  handlerChange
}: DashboardTableProps) {
  const serviceMapping = {
    yandex_x: 'Yandex X',
    similarweb: 'SimilarWeb',
    moz: 'Moz',
    web_archive: 'Web Archive'
  }
  const columns: TableColumn<DashboardDataRow>[] = [
    {
      name: 'Website',
      selector: (row) => row.site.url,
      sortable: true,
      width: '170px'
    },
    {
      name: 'Webmaster',
      cell: (row) => (
        <ul>
          {row.webmasters?.map((item, index) => (
            <li key={index}>{item.name}</li>
          ))}
        </ul>
      ),
      sortable: false,
      width: '120px'
    },
    {
      name: 'Published',
      cell: (row) => (
        <ul>
          {row.projects
            ?.sort((a, b) => a.name.localeCompare(b.name))
            .map((item, index) => (
              <li key={index}>
                {item.name} - ({item.publish_pages?.length})
              </li>
            ))}
        </ul>
      ),
      sortable: false,
      width: '170px'
    },
    {
      name: 'Publish cost',
      selector: (row) => row.publish_cost + '$',
      sortable: true
    },
    {
      name: 'Seo data',
      cell: (row) => {
        const seoData = row.seo_data

        if (!seoData) {
          return null
        }

        const listItems = Object.entries(seoData)
          .filter(([key]) => key !== 'created')
          .map(([key, value]) => (
            <li key={key}>
              {serviceMapping[key]}:{' '}
              {typeof value === 'object' ? value.data?.value || 0 : value}
            </li>
          ))

        return <ul>{listItems}</ul>
      },
      width: '250px'
    },
    {
      name: 'Efficiency',
      sortable: true,
      selector: (row) => Number(parseFloat(row.publish_efficiency).toFixed(2))
    },
    {
      name: 'Last check',
      cell: (row) => {
        const newestLastPublishCheck = row.projects?.reduce((acc, project) => {
          if (!acc || project?.last_publish_check > acc) {
            return project.last_publish_check
          } else {
            return acc
          }
        }, null)
        const listItem = (
          <>
            <li>Seo: {formatDate(row.seo_data?.created)}</li>
            <li>Publishing: {formatDate(newestLastPublishCheck)}</li>
          </>
        )
        return <ul>{listItem}</ul>
      },
      width: '250px'
    },
    {
      name: 'Action',
      cell: (row) => (
        <DashboardActionButtons
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
      title='Dashboard'
      columns={columns}
      data={data}
      totalRows={response?.data?.count || 0}
      perPageCount={perPage}
      handlerChange={handlerChange}
    />
  )
}

export default DashboardTable
