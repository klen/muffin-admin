import React from "react"

import {
  ListButton,
  EditButton,
  Show,
  SimpleShowLayout,
  TopToolbar,
} from "react-admin"

import initRAItems from "../ui"
import { checkParams, processAdmin, setupAdmin } from "../utils"
import { ActionButton } from "../buttons/ActionButton"

// Initiliaze a show component
setupAdmin(
  "show",
  checkParams(
    ({ actions, fields }, resource) =>
      function MAShow(props) {
        return (
          <Show
            actions={processAdmin(
              "show-actions",
              { actions, resource },
              resource
            )}
            {...props}
          >
            <SimpleShowLayout>
              {processAdmin("show-fields", fields, resource)}
            </SimpleShowLayout>
          </Show>
        )
      }
  )
)

/* Actions */
setupAdmin("show-actions", ({ actions, resource }) => (
  <TopToolbar>
    {actions.map((props, idx) => (
      <ActionButton key={idx} resource={resource} {...props} />
    ))}
    <ListButton />
    <EditButton />
  </TopToolbar>
))

/* Fields */
setupAdmin("show-fields", initRAItems)
