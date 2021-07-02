import React from "react";

import { ListButton, EditButton, Show, SimpleShowLayout, TopToolbar } from "react-admin";
import { checkParams, processAdmin, initRAItems, setupAdmin } from '../utils'

import { ActionButton } from '../buttons/ActionButton'


// Initiliaze a show component
setupAdmin('show', checkParams(({actions, fields}, res) => props => {

    const Actions = ({basePath, data, resource, ...baseProps}) => (
      <TopToolbar>
        {
          actions.map((props, idx) => {
            let aProps = {resource, basePath, record: data, ...baseProps, ...props};
            return <ActionButton key={ idx } {...aProps} />
          })
        }
        <ListButton basePath={ basePath } />
        <EditButton basePath={basePath} record={data} />
      </TopToolbar>
    )

    return (
      <Show actions={ <Actions /> } {...props}>
        <SimpleShowLayout children={ processAdmin('show-fields', fields, res) } />
      </Show>
    )
}));

setupAdmin('show-fields', initRAItems);
