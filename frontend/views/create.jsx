import React from 'react'

import { Create, SimpleForm, TopToolbar, ListButton } from 'react-admin'

import initRAItems from '../ui.jsx'
import { checkParams, processAdmin, setupAdmin } from '../utils'

// Initialize a create component
setupAdmin(
  'create',
  checkParams(
    (inputs, res) =>
      function MACreate(props) {
        const Actions = (
          <TopToolbar>
            <ListButton />
          </TopToolbar>
        )

        return (
          <Create actions={Actions} {...props}>
            <SimpleForm>
              {processAdmin('create-inputs', inputs, res)}
            </SimpleForm>
          </Create>
        )
      }
  )
)
setupAdmin('create-inputs', initRAItems)
