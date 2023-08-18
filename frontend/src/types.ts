export type TProps = {
  [key: string]: any
}

export type AdminAction = {
  view: string
  icon: string
  action: string
  title: string
  label: string
}

export type AdminField = [string, { source: string }]
export type AdminInput = [string, { required: boolean; source: string }]

export type AdminShowLink = {
  label: string
  title?: string
  icon?: string
  fk?: string
}
export type AdminShowProps = {
  actions: AdminAction[]
  fields: AdminField[]
  links: Record<string, AdminShowLink>
}

export type AdminResourceProps = {
  name: string
  icon?: string
  label: string
  create: AdminInput[]
  edit: {
    actions: AdminAction[]
    inputs: AdminInput[]
  }
  list: {
    limit: number
    limitMax: number
    actions: AdminAction[]
    fields: AdminField[]
    filters: AdminInput[]
    show: boolean
    edit?: boolean
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
