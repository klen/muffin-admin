import { EditButton, ListButton, Show, SimpleShowLayout, TopToolbar } from "react-admin"
import { LinkAction } from "./actions"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinShow() {
  const { show, name } = useMuffinResourceOpts()
  const Toolbar = findBuilder(["show-toolbar", name])

  return (
    <Show actions={<Toolbar />}>
      <SimpleShowLayout>{buildAdmin(["show-fields", name], show)}</SimpleShowLayout>
    </Show>
  )
}

setupAdmin(["show"], (props) => <MuffinShow {...props} />)
setupAdmin(["show-fields"], ({ fields }) => buildRA(fields))

export function MuffinShowToolbar() {
  const { show, name } = useMuffinResourceOpts()
  const { edit } = show

  const Links = findBuilder(["show-links", name])
  const Actions = findBuilder(["show-actions", name])

  return (
    <TopToolbar>
      <Links />
      <Actions />
      <ListButton />
      {edit && <EditButton />}
    </TopToolbar>
  )
}

setupAdmin(["show-toolbar"], MuffinShowToolbar)

export function MuffinShowActions() {
  const { show } = useMuffinResourceOpts()
  const { actions } = show
  return actions.map((props) => <ActionButton key={props.id} {...props} />)
}

setupAdmin(["show-actions"], MuffinShowActions)

export function MuffinShowLinks() {
  const { show } = useMuffinResourceOpts()
  const { links } = show
  return (
    <div style={{ marginRight: "auto" }}>
      {links.map(([key, props]) => (
        <LinkAction key={key} resource={key} {...props} />
      ))}
    </div>
  )
}

setupAdmin(["show-links"], MuffinShowLinks)
