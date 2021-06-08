import React from "react";

import { fetchUtils } from 'ra-core';
import { stringify } from 'query-string';
import { required } from 'react-admin';

import ui from "./ui";


export const admin = {}
export const setupAdmin = globalThis.setupAdmin = (type, fn) => admin[type] = fn
export const checkParams = (fn) => (props, res) => {
  if (!props || React.isValidElement(props)) return props;
  return fn(props, res);
}
export const processAdmin = (type, props, res) => {
  let callbacks = [], result = props;

  if (admin[`${type}-${res}`]) result = admin[`${type}-${res}`](props, res);
  if (admin[type]) result = admin[type](props, res);
  if (process.env.NODE_ENV == 'development') console.log(`${type}${ res ? '-' + res : ''}`, props);

  return result;
}
export const initRAItems = itemsProps => itemsProps.map((item) => {
    const Item = ui[item[0]],
          props = {...item[1]};

    if (props.required) {
        props.validate = required();
        delete props.required
    }

    props.fullWidth = props.fullWidth ?? true

    if (props.children) props.children = initRAItems(props.children)[0];
  
    return <Item key={ props.source } { ...props } />
})

export const requestHeaders = {};

export const makeRequest = (url, params) => {
  let {data, query, ...opts} = params || {};

  if (data) opts.body = JSON.stringify(data);
  if (query) url = `${url}?${stringify(query)}`;

  opts = {...opts, headers: new Headers({...requestHeaders, ...opts.headers})}

  return fetchUtils.fetchJson(url, opts);
}
