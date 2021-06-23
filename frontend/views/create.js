import React from "react";

import { Create, SimpleForm } from "react-admin";
import { checkParams, processAdmin, initRAItems, setupAdmin } from '../utils'

// Initialize a create component
setupAdmin('create', checkParams((inputs, res) => props =>
  <Create {...props}>
    <SimpleForm children={ processAdmin('create-inputs', inputs, res) } />
  </Create>
));
setupAdmin('create-inputs', initRAItems);

