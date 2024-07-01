import { EditButton, ListButton, Show, SimpleShowLayout, TopToolbar } from "react-admin"
import { LinkAction } from "./actions"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinResourceShow() {
  const { show, name } = useMuffinResourceOpts()
  const ShowActions = findBuilder(["show-actions", name])

  return (
    <Show actions={<ShowActions />}>
      <SimpleShowLayout>{buildAdmin(["show-fields", name], show)}</SimpleShowLayout>
    </Show>
  )
}

setupAdmin(["record-actions"], () => {
  const { show } = useMuffinResourceOpts()
  const { actions } = show
  return actions.map((props) => <ActionButton key={props.id} {...props} />)
})

setupAdmin(["record-links"], () => {
  const { show } = useMuffinResourceOpts()
  const { links } = show
  return (
    <div style={{ marginRight: "auto" }}>
      {links.map(([key, props]) => (
        <LinkAction key={key} resource={key} {...props} />
      ))}
    </div>
  )
})

setupAdmin(["show"], (props) => <MuffinResourceShow {...props} />)

setupAdmin(["show-fields"], ({ fields }) => buildRA(fields))

setupAdmin(["show-actions"], () => {
  const { show, name } = useMuffinResourceOpts()
  const { edit } = show

  const Links = findBuilder(["record-links", name])
  const Actions = findBuilder(["record-actions", name])

  return (
    <TopToolbar>
      <Links />
      <Actions />
      <ListButton />
      {edit && <EditButton />}
    </TopToolbar>
  )
})
