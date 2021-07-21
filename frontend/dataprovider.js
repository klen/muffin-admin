import { makeRequest } from './utils';


export default (apiUrl) => {

  const methods = {

    getList: async (resource, {filter, pagination, sort}) => {
      const query = {};
      if (filter) query.where = JSON.stringify(filter);
      if (pagination) {
        const {page, perPage: limit} = pagination;
        query.limit = limit;
        query.offset = limit * (page - 1);
      }
      if (sort) {
        const {field, order} = sort;
        query.sort = order == 'ASC' ? field : `-${field}`;
      };

      const {headers, json} = await makeRequest(`${apiUrl}/${resource}`, {query});
      return {
        data: json,
        total: parseInt(headers.get('x-total'), 10),
      };

    },

    getOne: async (resource, {id}) => {
      const {json} = await makeRequest(`${apiUrl}/${resource}/${id}`);
      return {data: json};
    },

    create: async (resource, {data}) => {
      const {json} = await makeRequest(`${apiUrl}/${resource}`, {data, method: 'POST'});
      return {data: json};
    },

    update: async (resource, {id, data}) => {
      const {json} = await makeRequest(`${apiUrl}/${resource}/${id}`, {data, method: 'PUT'});
      return {data: json};
    },

    updateMany: async (resource, {ids, data}) => {
      await Promise.all(ids.map(id => methods.update(resource, {id, data})));
      return {data: ids};
    },

    delete: async (resource, {id}) => {
      const {json} = await makeRequest(`${apiUrl}/${resource}/${id}`, {method: 'DELETE'});
      return {data: {id}};
    },

    deleteMany: async (resource, {ids}) => {
      const {json} = await makeRequest(`${apiUrl}/${resource}`, {data: ids, method: 'DELETE'});
      return {data: ids};
    },

    getMany: (resource, {ids}) => {
      return methods.getList(resource, {filter: {id: {"$in": ids}}});
    },

    getManyReference: async (resource, {target, id, filter, ...opts}) => {
      filter = filter || {};
      filter[target] = id;
      return await methods.getList(resource, {filter, ...opts});
    },

    runAction: async (resource, props) => {
      let {action, payload, ids, record} = props;
      if (record) { action = action.replace(/\{([^}]+)\}/, (_, field) => record[field]).replace(/^\/+/, '') }
      const {json} = await makeRequest(`${apiUrl}/${action}`, {query: {ids}, method: 'POST', data: payload});
      return {data: json};
    },

  };

  return methods;

}
