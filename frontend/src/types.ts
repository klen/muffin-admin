export type TProps = {
  [key: string]: any
}

export type AdminAction = {
  view: string
  id: string
  label: string
  title: string
  icon: string
  action: string
}

export type AdminField = [string, { source: string }]
export type AdminInput = [string, { required: boolean; source: string }]

export type AdminShowLink = {
  label: string
  title?: string
  icon?: string
  field?: string
}
export type AdminShowProps = {
  actions: AdminAction[]
  fields: AdminField[]
  links: [string, AdminShowLink][]
  edit?: boolean
}

export type AdminResourceProps = {
  name: string
  icon?: string
  label: string
  create: AdminInput[] | false
  edit:
    | {
        actions: AdminAction[]
        inputs: AdminInput[]
        remove?: boolean
      }
    | false
  list: {
    limit: number
    limitMax: number
    actions: AdminAction[]
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
  version: string
}
