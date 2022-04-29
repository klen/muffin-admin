import React from 'react'

import {
  Edit,
  ListButton,
  ShowButton,
  SimpleForm,
  TopToolbar,
} from 'react-admin'

import initRAItems from '../ui.jsx'
import { checkParams, processAdmin, setupAdmin } from '../utils'

import { ActionButton } from '../buttons/ActionButton.jsx'

// Initialize an edit component
setupAdmin(
  'edit',
  checkParams(
    ({ actions, inputs }, res) =>
      function MAEdit(props) {
        const Actions = ({ basePath, resource, ...baseProps }) => (
          <TopToolbar>
            {actions.map((props, idx) => {
              let aProps = { resource, basePath, ...baseProps, ...props }
              return <ActionButton key={idx} {...aProps} />
            })}
            <ListButton />
            <ShowButton />
          </TopToolbar>
        )

        return (
          <Edit actions={<Actions />} {...props}>
            <SimpleForm>{processAdmin('edit-inputs', inputs, res)}</SimpleForm>
          </Edit>
        )
      }
  )
)

setupAdmin('edit-inputs', initRAItems)
