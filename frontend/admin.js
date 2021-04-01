import React from "react";

import * as ra from "react-admin";
import * as icons from "@material-ui/icons"

import authProvider from "./authprovider";
import dataProvider from "./dataprovider";


const defaultPagination = <ra.Pagination rowsPerPageOptions={[10, 25, 50, 100]} />;

const checkParams = (fn) => (props, res) => {
  if (!props || React.isValidElement(props)) return props;
  return fn(props, res);
}

const initItems = itemsProps => itemsProps.map((item) => {
    const Item = ra[item[0]],
          props = {...item[1]};

    if (props.required) {
        props.validate = ra.required();
        delete props.required
    }

    props.fullWidth = props.fullWidth ?? true

    if (props.children) props.children = initItems(props.children)[0];
  
    return <Item key={ props.source } { ...props } />
  })

const admin = {

  // Process Admin
  "admin": (props) => {
    const { apiUrl, auth, adminProps, resources } = props;

    return <ra.Admin  authProvider={ processAdmin('auth', auth) }
                      children={ processAdmin('resources', resources) }
                      dataProvider={ processAdmin('data', apiUrl) }
                      loginPage={ processAdmin('login', auth) }
                      { ...adminProps } />
  },

  // Process Auth
  "auth": auth => authProvider(auth),

  // Process Data
  "data": apiUrl => dataProvider(apiUrl),

  // Process Login Page
  "login": checkParams((params, res) => (props) => <ra.Login {...props}  />),

  // Process Resources
  "resources": resources => resources.map(res => processAdmin('resource', res, res.name)),

  // Process Resource
  "resource": checkParams((props, res) => {
    let {name, list, create, edit, show, icon, ...resProps } = props;

    return <ra.Resource key={ name } name={ name } icon={ icons[icon] }
                        create={ processAdmin('create', create, res) }
                        edit={ processAdmin('edit', edit, res) }
                        list={ processAdmin('list', list, res) }
                        show={ processAdmin('show', show, res) }
                        { ...resProps } />;
  }),

  // Process list view
  "list": checkParams((props, res) => {
    let {children, filters, pagination, ...listProps } = props;

    return (props) => {
      let Filters = (props) => <ra.Filter { ...props } children={ processAdmin('list-filters', filters, res) } />

      props = { ...props, ...listProps };
      return (
        <ra.List filters={ <Filters /> } pagination={ pagination || defaultPagination } { ...props }>
          <ra.Datagrid rowClick="show" children={ [...processAdmin('list-fields', children, res), <ra.EditButton />] } />
        </ra.List>
      )
    };

  }),

  "list-filters": checkParams((inputs, res) => initItems(inputs)),

  "list-fields": checkParams((fields, res) => initItems(fields)),

  // Process show view
  "show": checkParams((fields, res) => (props) =>
      <ra.Show {...props}>
        <ra.SimpleShowLayout children={ processAdmin('show-fields', fields, res) } />
      </ra.Show>
  ),

  "show-fields": checkParams((fields, res) => initItems(fields)),

  // Process create view
  "create": checkParams((inputs, res) => (props) =>
    <ra.Create {...props}>
      <ra.SimpleForm children={ processAdmin('create-inputs', inputs, res) } />
    </ra.Create>
  ),

  "create-inputs": checkParams((inputs, res) => initItems(inputs)),

  // Process edit view
  "edit": checkParams((inputs, res) => (props) =>
    <ra.Edit { ...props }>
      <ra.SimpleForm children={ processAdmin('edit-inputs', inputs, res) } />
    </ra.Edit>
  ),

  "edit-inputs": checkParams((inputs, res) => initItems(inputs)),

}

const setupAdmin = globalThis.setupAdmin = (type, fn) => {
  admin[type] = fn;
}

const processAdmin = (type, props, res) => {
  let callbacks = [], result = props;

  if (admin[`${type}-${res}`]) result = admin[`${type}-${res}`](props, res);
  if (admin[type]) result = admin[type](props, res);
  if (process.env.NODE_ENV == 'development') console.log(`${type}${ res ? '-' + res : ''}`, props);

  return result;
}

export default (props) => processAdmin('admin', props);
