import { Create, ListButton, SimpleForm, TopToolbar } from "react-admin"
import { buildRA } from "./buildRA"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinResourceCreate() {
  const { name, create } = useMuffinResourceOpts()
  if (!create) return null

  const ActionsToolbar = findBuilder(["create-toolbar", name])

  return (
    <Create actions={<ActionsToolbar />}>
      <SimpleForm>{buildAdmin(["create-inputs", name], create)}</SimpleForm>
    </Create>
  )
}

setupAdmin(["create"], MuffinResourceCreate)
setupAdmin(["create-inputs"], buildRA)

setupAdmin(["create-toolbar"], () => (
  <TopToolbar>
    <ListButton />
  </TopToolbar>
))
