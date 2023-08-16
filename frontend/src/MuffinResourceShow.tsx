import React from "react"
import {
  EditButton,
  ListButton,
  Show,
  SimpleShowLayout,
  TopToolbar,
  useResourceContext,
} from "react-admin"
import { buildAdmin, setupAdmin } from "./utils"
import { AdminResourceProps } from "./types"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"

export function MuffinResourceShow(props: AdminResourceProps["show"]) {
  const resourceName = useResourceContext()
  const { fields, actions } = props
  return (
    <Show actions={buildAdmin(["show-actions", resourceName], actions)}>
      <SimpleShowLayout>
        {buildAdmin(["show-fields", resourceName], fields)}
      </SimpleShowLayout>
    </Show>
  )
}

setupAdmin(["show"], (props) => <MuffinResourceShow {...props} />)
setupAdmin(["show-fields"], (props) => buildRA(props))
setupAdmin(["show-actions"], (actions) => (
  <TopToolbar>
    {actions.map((props, idx) => (
      <ActionButton key={idx} {...props} />
    ))}
    <ListButton />
    <EditButton />
  </TopToolbar>
))
