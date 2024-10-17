import { PropsWithChildren } from "react"
import { Create, ListButton, SimpleForm, TopToolbar } from "react-admin"
import { buildRA } from "./buildRA"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinResourceCreate({ children }: PropsWithChildren) {
  const { name, create } = useMuffinResourceOpts()
  if (!create) return null

  const ActionsToolbar = findBuilder(["create-toolbar", name])

  return (
    <Create actions={<ActionsToolbar />}>
      {children}
      <SimpleForm>{buildAdmin(["create-inputs", name], create)}</SimpleForm>
    </Create>
  )
}

setupAdmin(["create"], MuffinResourceCreate)
setupAdmin(["create-inputs"], buildRA)

export function MuffinCreateToolbar({ children }: PropsWithChildren) {
  return (
    <TopToolbar>
      {children}
      <ListButton />
    </TopToolbar>
  )
}

setupAdmin(["create-toolbar"], MuffinCreateToolbar)
