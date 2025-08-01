import * as icons from "@mui/icons-material"
import { stringify } from "query-string"
import { fetchUtils } from "ra-core"
import { TAdminPath } from "./types"

const builders = new Map<string, (props: any) => any>()

export function setupAdmin<T>(adminType: TAdminPath, fc: (props: any) => T) {
  const key = adminType.join("/")
  builders.set(key, fc)
}

export function buildAdmin(adminType: TAdminPath, props = {}) {
  const builder = findBuilder(adminType)
  if (process.env.NODE_ENV == "development") console.log(props)
  if (builder) return builder(props)

  console.warn(`No admin renderer found for ${adminType.join("/")}`)
  return null
}

export function findBuilder(adminType: TAdminPath): (props: any) => any {
  if (process.env.NODE_ENV == "development") console.log(adminType)
  const key = [...adminType]
  while (key.length) {
    const builder = builders.get(key.join("/"))
    if (builder) return builder
    key.pop()
  }
}

export type APIParams = {
  method?: string
  query?: {
    where?: string
    limit?: number
    offset?: number
    sort?: string
    ids?: string[]
  }
  data?: any
  headers?: any
  body?: string
}

export const requestHeaders: Record<string, string> = {}

export function makeRequest(url: string, params: APIParams = {}) {
  const { data, query, ...opts } = params || {}

  if (data) opts.body = JSON.stringify(data)
  if (query) url = `${url}?${stringify(query)}`

  return fetchUtils.fetchJson(url, {
    ...opts,
    headers: new Headers({ ...requestHeaders, ...opts.headers }),
  })
}

export function findIcon(icon?: string) {
  return icon ? icons[icon] : undefined
}

export function buildIcon(icon?: string) {
  const Icon = findIcon(icon)
  if (Icon) return <Icon />
}

function isObject(item: any) {
  return item && typeof item === "object" && !Array.isArray(item)
}

export function deepMerge(target: any, ...sources: any[]): any {
  if (!sources.length) return target
  const source = sources.shift()

  if (isObject(target) && isObject(source)) {
    for (const key in source) {
      if (isObject(source[key])) {
        if (!target[key]) Object.assign(target, { [key]: {} })
        deepMerge(target[key], source[key])
      } else {
        Object.assign(target, { [key]: source[key] })
      }
    }
  }
  return deepMerge(target, ...sources)
}

export function prepareFilters(filter: any) {
  return JSON.stringify(
    Object.entries(filter).reduce((acc, [key, value]) => {
      acc[key] = Array.isArray(value) ? { $in: value } : value
      return acc
    }, {})
  )
}
