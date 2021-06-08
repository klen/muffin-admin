import React from "react";

import { 
  Create,
  Datagrid,
  Edit,
  EditButton,
  Filter,
  List,
  Pagination,
  Resource,
  Show,
  SimpleForm,
  SimpleShowLayout,
} from "react-admin";
import * as icons from "@material-ui/icons"

import { checkParams, processAdmin, initRAItems, setupAdmin } from './utils'


const defaultPagination = <Pagination rowsPerPageOptions={[10, 25, 50, 100]} />;

// Initialize Resources Components
setupAdmin('resources', resources => resources.map(res => processAdmin('resource', res, res.name)));

// Initialize a resource's component
setupAdmin('resource', checkParams((props, res) => {
    let { create, edit, icon, list, name, show, ...resProps } = props;

    return <Resource key={ name } name={ name } icon={ icons[icon] }
                        create={ processAdmin('create', create, res) }
                        edit={ processAdmin('edit', edit, res) }
                        list={ processAdmin('list', list, res) }
                        show={ processAdmin('show', show, res) }
                        { ...resProps } />;
}));

// Initiliaze a list component
setupAdmin('list', checkParams((props, res) => {
    let {children, filters, edit, pagination, show, ...listProps } = props;

    children = processAdmin('list-fields', children, res);
    if (edit) children.push(<EditButton key="edit-button" />);

    return (props) => {
      let Filters = (props) => <Filter { ...props } children={ processAdmin('list-filters', filters, res) } />

      props = { ...props, ...listProps };
      return (
        <List filters={ <Filters /> } pagination={ pagination || defaultPagination } { ...props }>
          <Datagrid rowClick={ show && "show" } children={ children } />
        </List>
      )
    };
}));

setupAdmin('list-filters', initRAItems);
setupAdmin('list-fields', initRAItems);

// Initiliaze a show component
setupAdmin('show', checkParams((fields, res) => props =>
    <Show {...props}>
      <SimpleShowLayout children={ processAdmin('show-fields', fields, res) } />
    </Show>
));
setupAdmin('show-fields', initRAItems);

// Initialize a create component
setupAdmin('create', checkParams((inputs, res) => props =>
  <Create {...props}>
    <SimpleForm children={ processAdmin('create-inputs', inputs, res) } />
  </Create>
));
setupAdmin('create-inputs', initRAItems);

// Initialize an edit component
setupAdmin('edit', checkParams((inputs, res) => props =>
  <Edit { ...props }>
    <SimpleForm children={ processAdmin('edit-inputs', inputs, res) } />
  </Edit>
));
setupAdmin('edit-inputs', initRAItems);
