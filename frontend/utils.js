import React from "react";

import { fetchUtils } from 'ra-core';
import { stringify } from 'query-string';
import { required } from 'react-admin';


const admin = globalThis.admin = globalThis.admin || {};

export const setupAdmin = globalThis.setupAdmin = (type, fn) => admin[type] = fn
export const checkParams = (fn) => (props, res) => {
  if (!props || React.isValidElement(props)) return props;
  return fn(props, res);
}
export const processAdmin = (type, props, res) => {
  let callbacks = [], result = props;

  if (process.env.NODE_ENV == 'development') console.log(`${type}${ res ? '-' + res : ''}`, props);

  if (admin[`${type}-${res}`]) return admin[`${type}-${res}`](props, res);
  if (admin[type]) return admin[type](props, res);
}

export const requestHeaders = {};

export const makeRequest = (url, params) => {
  let {data, query, ...opts} = params || {};

  if (data) opts.body = JSON.stringify(data);
  if (query) url = `${url}?${stringify(query)}`;

  opts = {...opts, headers: new Headers({...requestHeaders, ...opts.headers})}

  return fetchUtils.fetchJson(url, opts);
}
