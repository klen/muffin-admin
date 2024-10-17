import { PropsWithChildren } from "react"
import { EditButton, ListButton, Show, SimpleShowLayout, TopToolbar } from "react-admin"
import { LinkAction } from "./actions"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinShow({ children }: PropsWithChildren) {
  const { show, name } = useMuffinResourceOpts()
  const ActionsToolbar = findBuilder(["show-toolbar", name])

  return (
    <Show actions={<ActionsToolbar />}>
      {children}
      <SimpleShowLayout>{buildAdmin(["show-fields", name], show)}</SimpleShowLayout>
    </Show>
  )
}

setupAdmin(["show"], (props) => <MuffinShow {...props} />)
setupAdmin(["show-fields"], ({ fields }) => buildRA(fields))

export function MuffinShowToolbar({ children }: PropsWithChildren) {
  const { show, name } = useMuffinResourceOpts()
  const { edit } = show

  const Links = findBuilder(["show-links", name])
  const Actions = findBuilder(["show-actions", name])

  return (
    <TopToolbar>
      <Links />
      <Actions />
      {children}
      <ListButton />
      {edit && <EditButton />}
    </TopToolbar>
  )
}

setupAdmin(["show-toolbar"], MuffinShowToolbar)

export function MuffinShowActions({ children }: PropsWithChildren) {
  const { actions: baseActions = [] } = useMuffinResourceOpts()
  const actions = baseActions.filter((a) => a.view?.includes("show"))
  return (
    <>
      {children}
      {actions.map((props) => (
        <ActionButton key={props.id} {...props} />
      ))}
    </>
  )
}

setupAdmin(["show-actions"], MuffinShowActions)

export function MuffinShowLinks({ children }: PropsWithChildren) {
  const { show } = useMuffinResourceOpts()
  const { links } = show
  return (
    <div style={{ marginRight: "auto" }}>
      {links.map(([key, props]) => (
        <LinkAction key={key} resource={key} {...props} />
      ))}
      {children}
    </div>
  )
}

setupAdmin(["show-links"], MuffinShowLinks)
