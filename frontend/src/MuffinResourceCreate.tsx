import { Create, ListButton, SimpleForm, TopToolbar } from "react-admin"
import { buildRA } from "./buildRA"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinResourceCreate() {
  const { name, create } = useMuffinResourceOpts()
  if (!create) return null

  const Actions = findBuilder(["create-actions", name])

  return (
    <Create actions={<Actions />}>
      <SimpleForm>{buildAdmin(["create-inputs", name], create)}</SimpleForm>
    </Create>
  )
}

setupAdmin(["create"], MuffinResourceCreate)

setupAdmin(["create-actions"], () => (
  <TopToolbar>
    <ListButton />
  </TopToolbar>
))

setupAdmin(["create-inputs"], buildRA)
