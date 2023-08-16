import React from "react"
import {
  Edit,
  ListButton,
  ShowButton,
  SimpleForm,
  TopToolbar,
  useResourceContext,
} from "react-admin"
import { AdminPropsContext, buildAdmin, setupAdmin } from "./utils"
import { AdminAction, AdminOpts, AdminResourceProps } from "./types"
import { useContext } from "react"
import { ActionButton } from "./buttons"
import { buildRA } from "./buildRA"

export function MuffinResourceEdit({
  actions,
  inputs,
  ...props
}: AdminResourceProps["edit"]) {
  const resourceName = useResourceContext()
  const {
    adminProps: { mutationMode },
  } = useContext(AdminPropsContext) as AdminOpts

  return (
    <Edit
      actions={buildAdmin(["edit-actions", resourceName], actions)}
      mutationMode={mutationMode || "optimistic"}
      {...props}
    >
      <SimpleForm>
        {buildAdmin(["edit-inputs", resourceName], inputs)}
      </SimpleForm>
    </Edit>
  )
}

setupAdmin(["edit"], (props) => <MuffinResourceEdit {...props} />)
setupAdmin(["edit-actions"], (actions: AdminAction[]) => (
  <TopToolbar>
    {actions.map((props, idx) => (
      <ActionButton key={idx} {...props} />
    ))}
    <ListButton />
    <ShowButton />
  </TopToolbar>
))
setupAdmin(["edit-inputs"], buildRA)
