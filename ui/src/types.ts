import { ReactNode } from 'react'
import { TableColumn } from 'react-data-table-component'
import { SWRResponse } from 'swr'

interface ActionButtonsProps<T> {
  object: T
  endpointName: string
  refresh: () => void
}

interface FormProps<T> {
  page_obj?: T
  endpointName: string
  useModal?: boolean
  showModal: boolean
  onClose: () => void
}

interface FormContentProps<T> {
  form: T
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void
  updateFormValue: (field: string, value: string | object) => void
  buttons?: React.ReactNode
}

interface ServerResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

interface TableProps<T> {
  data: T[]
  endpointName: string
  response: SWRResponse<ServerResponse<T>, Error>
  perPage: number
  handlerChange: (offset: number, perPage: number) => void
}

interface TableBaseProps<T> {
  title: string
  columns: TableColumn<T>[]
  data: T[]
  totalRows: number
  perPageCount: number
  handlerChange: (offset: number, perPage: number) => void
  sortColumnNumber?: number
  sortAsc?: boolean
}

interface GeneratorValues {
  id: string
  name?: string
}

interface CustomTooltipProps {
  placement: string
  delay: { show: number; hide: number }
  tooltipText: string
  children: React.ReactNode
}

interface UserData {
  id: string
  username: string
  email: string
  created: string
  updated: string
  is_active: boolean
  mail_settings: MailSettings
}

interface ReactComponent {
  children: ReactNode
}

interface UserLoginData {
  username: string
  password: string
}

interface UserRegisterData {
  username: string
  email: string
  password: string
}

interface UserLocalData {
  access: string
  refresh: string
  user: object
}

interface Url {
  id: string
  url: string
  seo_status: string | null
}

interface SeoData {
  yandex_x?: { [key: string]: string | number }
  similarweb?: { [key: string]: string | number }
  moz?: { [key: string]: string | number }
  web_archive?: { [key: string]: string | number }
  created?: string
}

// Form field interfaces
interface FormFieldProps {
  label?: string

  type?: string
  placeholder: string
  rowsCount?: number
  value: string | number
  onChange: (value: string) => void
  disabled?: boolean
}

interface SingleSelectFieldProps {
  label?: string
  placeholder?: string
  values: [
    {
      id?: string | null
      name?: string | null
    }
  ]
  selectedValues: {
    id?: string | null
    name?: string | null
  }
  onChange: (value: string) => void
}

// Dashboard page interfaces
interface DashboardDataRow {
  id: string
  site: Url
  publish_cost: number
  publish_efficiency: number
  efficiency: number
  information: string
  seo_data: SeoData | null
  webmasters?: WebmasterDataRow[]
  projects: ProjectDataRow[]
}

interface DashboardActionButtonsProps
  extends ActionButtonsProps<DashboardDataRow> {}

interface DashboardFormProps extends FormProps<DashboardDataRow> {}

interface DashboardFormContentProps
  extends FormContentProps<DashboardDataRow> {}

interface DashboardTableProps extends TableProps<DashboardDataRow> {}

// Mail settings interfaces
interface MailSettingsFormProps {
  mail_settings?: MailSettings | null
  onUpdateMailSettings: (updatedMailSettings: MailSettings) => void
}

interface MailSettings {
  mail_folders: string
  smtp_server: string
  smtp_port: number
  smtp_username: string
  smtp_password: string
  imap_ssl: boolean
  imap_server: string
  imap_port: number
  imap_username: string
  imap_password: string
}

// Project page interfaces
interface ProjectPublishPage {
  id: string
  url: string
  publish_date: string
  check_status: string
}

interface ProjectDataRow {
  id: string
  name: string
  url?: Url
  mail_settings?: MailSettings | null
  created?: string
  last_published_date?: string
  published_count?: number
  total_spend?: number
  publish_pages?: ProjectPublishPage[]
  last_publish_check?: string
}

interface ProjectActionButtonsProps
  extends ActionButtonsProps<ProjectDataRow> {}

interface ProjectFormProps extends FormProps<ProjectDataRow> {}

interface ProjectFormContentProps {
  form?: ProjectDataRow
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void
  updateFormValue: (field: string, value: string) => void
  showMailSettingsForm: boolean
  handleToggleMailSettingsForm: () => void
  handleUpdateMailSettings: (updatedMailSettings: MailSettings) => void
  buttons?: React.ReactNode
}

interface ProjectTableProps extends TableProps<ProjectDataRow> {}

// Webmaster page interfaces
interface WebmasterPaymentDataRow {
  id: string
  type: string
  details: string
  total_spend: number
}

interface WebmasterWebsiteDataRow {
  id: string
  name?: string
  site?: Url
}

interface WebmasterContactDataRow {
  id: string
  type: string
  contact: string
  latest_contact: string
}

interface WebmasterDataRow {
  id: string
  name: string
  contacts?: WebmasterContactDataRow[]
  payments?: WebmasterPaymentDataRow[]
  websites?: WebmasterWebsiteDataRow[]
}

interface WebmasterActionButtonsProps
  extends ActionButtonsProps<WebmasterDataRow> {}

interface WebmasterFormProps extends FormProps<WebmasterDataRow> {}

interface WebmasterFormContentProps
  extends FormContentProps<WebmasterDataRow> {}

interface WebmasterTableProps extends TableProps<WebmasterDataRow> {}

// Contact page interfaces
interface ContactDataRow {
  id: string
  contact: string
  type: string
  last_contact_date?: string
  updated?: string
  webmaster?: WebmasterDataRow
}

interface ContactActionButtonsProps
  extends ActionButtonsProps<ContactDataRow> {}

interface ContactFormProps extends FormProps<ContactDataRow> {}

interface ContactFormContentProps extends FormContentProps<ContactDataRow> {}

interface ContactTableProps extends TableProps<ContactDataRow> {}

// Contact history page interfaces
interface ContactHistoryDataRow {
  id: string
  subject: string
  body: string
  created: string
  webmaster: WebmasterDataRow
  contact: ContactDataRow
  project: ProjectDataRow
  website: WebmasterWebsiteDataRow
}

interface ContactHistoryActionButtonsProps
  extends ActionButtonsProps<ContactHistoryDataRow> {}

interface ContactHistoryFormProps extends FormProps<ContactHistoryDataRow> {}

interface ContactHistoryFormContentProps
  extends FormContentProps<ContactHistoryDataRow> {}

interface ContactHistoryTableProps extends TableProps<ContactHistoryDataRow> {}

// Mail page interfaces
interface MailDataRow {
  id: string
  account_name: string
  created: string
  receive_date: string
  mail_box: string
  mail_id: string
  replay_to: string
  author_name: string
  author_mail: string
  subject: string
  body: string
}

interface MailActionButtonsProps extends ActionButtonsProps<MailDataRow> {}

interface MailFormProps extends FormProps<MailDataRow> {}

interface MailFormContentProps extends FormContentProps<MailDataRow> {}

interface MailTableProps extends TableProps<MailDataRow> {}

// Payment page interfaces
interface PaymentDataRow {
  id: string
  detail: string
  type: string
}

interface PaymentActionButtonsProps
  extends ActionButtonsProps<PaymentDataRow> {}

interface PaymentFormProps extends FormProps<PaymentDataRow> {}

interface PaymentFormContentProps extends FormContentProps<PaymentDataRow> {}

interface PaymentTableProps extends TableProps<PaymentDataRow> {}

// Payment history page interfaces
interface PaymentHistoryDataRow {
  id: string
  created: string
  price: number
  payment: PaymentDataRow
  project: ProjectDataRow
  webmaster: WebmasterDataRow
  website: WebmasterWebsiteDataRow
}

interface PaymentHistoryActionButtonsProps
  extends ActionButtonsProps<PaymentHistoryDataRow> {}

interface PaymentHistoryFormProps extends FormProps<PaymentHistoryDataRow> {}

interface PaymentHistoryFormContentProps
  extends FormContentProps<PaymentHistoryDataRow> {}

interface PaymentHistoryTableProps extends TableProps<PaymentHistoryDataRow> {}

export type {
  ContactActionButtonsProps,
  ContactDataRow,
  ContactFormContentProps,
  ContactFormProps,
  ContactHistoryActionButtonsProps,
  ContactHistoryDataRow,
  ContactHistoryFormContentProps,
  ContactHistoryFormProps,
  ContactHistoryTableProps,
  ContactTableProps,
  CustomTooltipProps,
  DashboardActionButtonsProps,
  DashboardDataRow,
  DashboardFormContentProps,
  DashboardFormProps,
  DashboardTableProps,
  FormFieldProps,
  GeneratorValues,
  MailActionButtonsProps,
  MailDataRow,
  MailFormContentProps,
  MailFormProps,
  MailSettings,
  MailSettingsFormProps,
  MailTableProps,
  PaymentActionButtonsProps,
  PaymentDataRow,
  PaymentFormContentProps,
  PaymentFormProps,
  PaymentHistoryActionButtonsProps,
  PaymentHistoryDataRow,
  PaymentHistoryFormContentProps,
  PaymentHistoryFormProps,
  PaymentHistoryTableProps,
  PaymentTableProps,
  ProjectActionButtonsProps,
  ProjectDataRow,
  ProjectFormContentProps,
  ProjectFormProps,
  ProjectTableProps,
  ReactComponent,
  ServerResponse,
  SingleSelectFieldProps,
  TableBaseProps,
  Url,
  UserData,
  UserLocalData,
  UserLoginData,
  UserRegisterData,
  WebmasterActionButtonsProps,
  WebmasterDataRow,
  WebmasterFormContentProps,
  WebmasterFormProps,
  WebmasterTableProps
}
