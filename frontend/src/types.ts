export type TID = string | number

export type TProps = {
  [key: string]: any
}

export type TAdminType =
  | "action-form"
  | "admin"
  | "appbar"
  | "auth-provider"
  | "auth-storage-get"
  | "auth-storage-set"
  | "create"
  | "create-toolbar"
  | "create-inputs"
  | "dashboard"
  | "dashboard-actions"
  | "dashboard-content"
  | "data-provider"
  | "edit"
  | "edit-actions"
  | "edit-toolbar"
  | "edit-form-toolbar"
  | "edit-inputs"
  | "layout"
  | "list"
  | "list-actions"
  | "list-toolbar"
  | "list-grid"
  | "list-grid-buttons"
  | "list-filters"
  | "list-fields"
  | "locale"
  | "loginpage"
  | "menu"
  | "resource"
  | "show"
  | "show-actions"
  | "show-toolbar"
  | "show-fields"
  | "show-links"
export type TAdminPath = [type: TAdminType, ...ids: string[]]

export type AdminAction = {
  view?: ("show" | "edit" | "list" | "bulk")[]
  help?: string
  id: string
  label: string
  title: string
  icon: string
  paths: string[]
  confirm?: string | false
  schema?: AdminInput[]
  file?: boolean
}

export type AdminField = [string, { source: string }]
export type AdminInput = [string, { required: boolean; source: string;[key: string]: any }]

export type AdminShowLink = {
  label: string
  title?: string
  icon?: string
  field?: string
}
export type AdminShowProps = {
  fields: AdminField[]
  links: [string, AdminShowLink][]
  edit?: boolean
}

export type AdminPayloadProps = {
  active: boolean
  onClose: () => void
  onHandle: (payload?: any) => void
  title?: string
  schema?: AdminInput[]
  help?: string
}

export type AdminResourceProps = {
  name: string
  group?: string
  icon?: string
  label: string
  help?: string
  actions: AdminAction[]
  create: AdminInput[] | false
  edit:
  | {
    inputs: AdminInput[]
    remove?: boolean
  }
  | false
  list: {
    limit: number
    limitMax: number
    limitTotal: boolean
    create: boolean
    filters: AdminInput[]
    fields: AdminField[]
    // Enable show button
    show: boolean
    // Permissions
    edit?: boolean
    remove?: boolean
    // Default sorting
    sort?: {
      field: string
      order: "ASC" | "DESC"
    }
  }
  show: AdminShowProps
}

export type AdminDashboardBlock = {
  title: string
  value: any
}

export type AdminOpts = {
  adminProps: {
    title: string
    disableTelemetry?: boolean
    mutationMode?: "optimistic" | "pessimistic" | "undoable"
  }
  apiUrl: string
  appBarLinks: [{ url: string; title: string; icon?: string }]
  auth: {
    identityURL: string
    authorizeURL: string
    loginURL?: string
    logoutURL?: string
    required: boolean
    storage: "localstorage" | "cookie"
    storageName: string
  }
  dashboard: AdminDashboardBlock[] | AdminDashboardBlock
  resources: AdminResourceProps[]
  help?: string
  locales: Record<string, Record<string, any>>
  version: string
}
