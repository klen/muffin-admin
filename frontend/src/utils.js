/* eslint-disable no-console */

import { isValidElement } from "react"
import { fetchUtils } from "ra-core"
import { stringify } from "query-string"

const parts = {}

export const setupAdmin = (part, gen) => (parts[part] = gen)

export const checkParams = (fn) => (props, res) => {
  if (!props || isValidElement(props)) return props
  return fn(props, res)
}

export const processAdmin = (type, props, res) => {
  if (process.env.NODE_ENV == "development")
    console.log(`${type}${res ? "-" + res : ""}`, props)

  if (parts[`${type}-${res}`]) return parts[`${type}-${res}`](props, res)
  if (parts[type]) return parts[type](props, res)
}

export const requestHeaders = {}

export const makeRequest = (url, params) => {
  let { data, query, ...opts } = params || {}

  if (data) opts.body = JSON.stringify(data)
  if (query) url = `${url}?${stringify(query)}`

  opts = {
    ...opts,
    headers: new Headers({ ...requestHeaders, ...opts.headers }),
  }

  return fetchUtils.fetchJson(url, opts)
}
