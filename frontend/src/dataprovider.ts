import { AdminOpts } from "./types"
import { APIParams, makeRequest, setupAdmin } from "./utils"

export function MuffinDataprovider({ apiUrl }: AdminOpts) {
  async function request(url: string, options?: APIParams) {
    if (!url.startsWith("/")) url = `${apiUrl}/${url}`
    const { json, headers } = await makeRequest(url, options)
    return { data: json, headers }
  }

  const methods = {
    request,
    getList: async (resource: string, params: any) => {
      const { filter, pagination, sort } = params
      const query: APIParams["query"] = {}
      if (filter) query.where = JSON.stringify(filter)
      if (pagination) {
        const { page, perPage: limit } = pagination
        query.limit = limit
        query.offset = limit * (page - 1)
      }
      if (sort) {
        const { field, order } = sort
        query.sort = order == "ASC" ? field : `-${field}`
      }
      const { headers, data } = await request(resource, { query })
      return { data, total: parseInt(headers.get("x-total"), 10) }
    },

    getOne: async (resource, { id }) => {
      return await request(`${resource}/${id}`)
    },

    create: async (resource, { data }) => {
      return await request(resource, {
        data,
        method: "POST",
      })
    },

    update: async (resource, { id, data }) => {
      return await makeRequest(`${apiUrl}/${resource}/${id}`, {
        data,
        method: "PUT",
      })
    },

    updateMany: async (resource, { ids, data }) => {
      await Promise.all(ids.map((id) => methods.update(resource, { id, data })))
      return { data: ids }
    },

    delete: async (resource, { id }) => {
      await request(`${resource}/${id}`, { method: "DELETE" })
      return { data: { id } }
    },

    deleteMany: async (resource, { ids }) => {
      await request(resource, {
        data: ids,
        method: "DELETE",
      })
      return { data: ids }
    },

    getMany: (resource, props) => {
      const { ids, meta } = props
      const key = meta?.key || "id"
      return methods.getList(resource, { filter: { [key]: { $in: ids } } })
    },

    getManyReference: async (resource, { target, id, filter, ...opts }) => {
      filter = filter || {}
      filter[target] = id
      return await methods.getList(resource, { filter, ...opts })
    },

    runAction: async (resource: string, action: string, props: TActionProps) => {
      const { payload, ids, record } = props
      action = action.replace(/^\/+/, "")
      if (record) {
        action = action.replace(/\{([^}]+)\}/, (_, field) => record[field])
      }
      const { json } = await makeRequest(`${apiUrl}/${action}`, {
        query: { ids },
        method: "POST",
        data: payload,
      })
      return { data: json }
    },
  }
  return methods
}

export type TActionProps = {
  payload?: any
  ids?: string[]
  record: any
}
setupAdmin(["dataprovider"], MuffinDataprovider)
