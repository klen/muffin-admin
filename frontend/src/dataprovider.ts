import { AdminOpts } from "./types"
import { APIParams, makeRequest, setupAdmin } from "./utils"

export function MuffinDataprovider({ apiUrl }: AdminOpts) {
  const methods = {
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
      const { headers, json } = await makeRequest(`${apiUrl}/${resource}`, {
        query,
      })
      return {
        data: json,
        total: parseInt(headers.get("x-total"), 10),
      }
    },

    getOne: async (resource, { id }) => {
      const { json } = await makeRequest(`${apiUrl}/${resource}/${id}`)
      return { data: json }
    },

    create: async (resource, { data }) => {
      const { json } = await makeRequest(`${apiUrl}/${resource}`, {
        data,
        method: "POST",
      })
      return { data: json }
    },

    update: async (resource, { id, data }) => {
      const { json } = await makeRequest(`${apiUrl}/${resource}/${id}`, {
        data,
        method: "PUT",
      })
      return { data: json }
    },

    updateMany: async (resource, { ids, data }) => {
      await Promise.all(ids.map((id) => methods.update(resource, { id, data })))
      return { data: ids }
    },

    delete: async (resource, { id }) => {
      await makeRequest(`${apiUrl}/${resource}/${id}`, {
        method: "DELETE",
      })
      return { data: { id } }
    },

    deleteMany: async (resource, { ids }) => {
      await makeRequest(`${apiUrl}/${resource}`, {
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

    runAction: async (resource, action, props) => {
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

setupAdmin(["dataprovider"], MuffinDataprovider)
