import React from "react";

import { Create, SimpleForm, TopToolbar, ListButton } from "react-admin";

import initRAItems from '../ui.jsx'
import { checkParams, processAdmin, setupAdmin } from '../utils'


// Initialize a create component
setupAdmin('create', checkParams((inputs, res) => props => {

  const Actions = ({basePath}) => (
      <TopToolbar>
        <ListButton basePath={ basePath } />
      </TopToolbar>
  )

  return (
    <Create actions={ <Actions /> } {...props}>
      <SimpleForm children={ processAdmin('create-inputs', inputs, res) } />
    </Create>
  )
}
));
setupAdmin('create-inputs', initRAItems);

