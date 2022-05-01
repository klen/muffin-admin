import React from 'react'
import {
  ListButton,
  EditButton,
  Show,
  SimpleShowLayout,
  TopToolbar,
} from 'react-admin'

import initRAItems from '../ui'
import { checkParams, processAdmin, setupAdmin } from '../utils'
import { ActionButton } from '../buttons/ActionButton'

// Initiliaze a show component
setupAdmin(
  'show',
  checkParams(
    ({ actions, fields }, resource) =>
      function MAShow(props) {
        const Actions = () => (
          <TopToolbar>
            {actions.map((props, idx) => {
              return <ActionButton key={idx} resource={resource} {...props} />
            })}
            <ListButton />
            <EditButton />
          </TopToolbar>
        )

        return (
          <Show actions={<Actions />} {...props}>
            <SimpleShowLayout>
              {processAdmin('show-fields', fields, resource)}
            </SimpleShowLayout>
          </Show>
        )
      }
  )
)

setupAdmin('show-fields', initRAItems)
