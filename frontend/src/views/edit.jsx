import React from "react"

import {
  Edit,
  ListButton,
  ShowButton,
  SimpleForm,
  TopToolbar,
} from "react-admin"

import initRAItems from "../ui"
import { checkParams, processAdmin, setupAdmin } from "../utils"
import { ActionButton } from "../buttons/ActionButton"

// Initialize an edit component
setupAdmin(
  "edit",
  checkParams((props, name) => {
    let { edit, adminProps } = props
    let { actions, inputs } = edit

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
        <Edit
          actions={<Actions />}
          mutationMode={adminProps.mutationMode || "optimistic"}
          {...props}
        >
          <SimpleForm>{processAdmin("edit-inputs", inputs, name)}</SimpleForm>
        </Edit>
      )
    }

    return MAEdit
  })
)

setupAdmin("edit-inputs", initRAItems)
