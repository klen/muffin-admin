import React from "react";

import { Edit, ShowButton, SimpleForm, TopToolbar } from "react-admin";
import { checkParams, processAdmin, initRAItems, setupAdmin } from '../utils'

import { ActionButton } from '../buttons/ActionButton'


// Initialize an edit component
setupAdmin('edit', checkParams(({actions, inputs}, res) => props => {

    const Actions = ({basePath, data, resource, ...baseProps}) => (
      <TopToolbar>
        {
          actions.map((props, idx) => {
            let aProps = {resource, basePath, ...baseProps, ...props};
            return <ActionButton key={ idx } {...aProps} />
          })
        }
        <ShowButton basePath={basePath} record={data} />
      </TopToolbar>
    )

    return (
      <Edit actions={ <Actions /> } { ...props }>
        <SimpleForm children={ processAdmin('edit-inputs', inputs, res) } />
      </Edit>
    )
}));

setupAdmin('edit-inputs', initRAItems);
