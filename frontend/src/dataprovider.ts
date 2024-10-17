import { TID } from "./types"
import { APIParams, makeRequest, setupAdmin } from "./utils"

export function MuffinDataprovider(apiUrl: string) {
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
      return {
        data,
        total: parseInt(headers.get("x-total"), 10),
        pageInfo: {
          hasPreviousPage: pagination.page > 1,
          hasNextPage: data.length === pagination.perPage,
        },
      }
    },

    getOne: async (resource: string, { id }: { id: TID }) => {
      return await request(`${resource}/${id}`)
    },

    create: async (resource: string, { data }) => {
      return await request(resource, {
        data,
        method: "POST",
      })
    },

    update: async (resource: string, { id, data }: { id: TID; data: any }) => {
      return await makeRequest(`${apiUrl}/${resource}/${id}`, {
        data,
        method: "PUT",
      }).then(({ json }) => ({ data: json }))
    },

    updateMany: async (resource: string, { ids, data }: { ids: TID[]; data: any }) => {
      await Promise.all(ids.map((id) => methods.update(resource, { id, data })))
      return { data: ids }
    },

    delete: async (resource: string, { id }: { id: TID }) => {
      await request(`${resource}/${id}`, { method: "DELETE" })
      return { data: { id } }
    },

    deleteMany: async (resource: string, { ids }: { ids: TID[][] }) => {
      await request(resource, {
        data: ids,
        method: "DELETE",
      })
      return { data: ids }
    },

    getMany: (resource: string, props: { ids: TID[]; meta: any }) => {
      const { ids, meta } = props
      const key = meta?.key || "id"
      return methods.getList(resource, { filter: { [key]: { $in: ids } } })
    },

    getManyReference: async (resource: string, { target, id, filter, ...opts }) => {
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

export type TActionProps<T = any> = {
  payload?: any
  ids?: string[]
  record?: T
}
setupAdmin(["data-provider"], MuffinDataprovider)
