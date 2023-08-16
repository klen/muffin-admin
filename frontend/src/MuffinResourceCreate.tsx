import React from "react"
import {
  Create,
  ListButton,
  SimpleForm,
  TopToolbar,
  useResourceContext,
} from "react-admin"
import { AdminResourceProps } from "./types"
import { buildAdmin, setupAdmin } from "./utils"
import { buildRA } from "./buildRA"

export function MuffinResourceCreate({
  inputs,
}: {
  inputs: AdminResourceProps["create"]
}) {
  const resourceName = useResourceContext()

  return (
    <Create actions={buildAdmin(["create-actions", resourceName])}>
      <SimpleForm>
        {buildAdmin(["create-inputs", resourceName], inputs)}
      </SimpleForm>
    </Create>
  )
}

setupAdmin(["create"], (inputs) => <MuffinResourceCreate inputs={inputs} />)

setupAdmin(["create-actions"], () => (
  <TopToolbar>
    <ListButton />
  </TopToolbar>
))

setupAdmin(["create-inputs"], buildRA)
