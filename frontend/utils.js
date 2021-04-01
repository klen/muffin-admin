import { stringify } from 'query-string';
import { fetchUtils } from 'ra-core';


export const requestHeaders = {};

export const makeRequest = (url, params) => {
  let {data, query, ...opts} = params || {};

  if (data) opts.body = JSON.stringify(data);
  if (query) url = `${url}?${stringify(query)}`;

  opts = {...opts, headers: new Headers({...requestHeaders, ...opts.headers})}

  return fetchUtils.fetchJson(url, opts);
}
