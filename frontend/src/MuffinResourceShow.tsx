import {
  EditButton,
  ListButton,
  Show,
  SimpleShowLayout,
  TopToolbar,
  useResourceContext,
} from "react-admin"
import { LinkAction } from "./actions"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"
import { AdminAction, AdminShowProps } from "./types"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinResourceShow(props: AdminShowProps) {
  const resourceName = useResourceContext()
  const ShowActions = findBuilder(["show-actions", resourceName])

  return (
    <Show actions={<ShowActions {...props} />}>
      <SimpleShowLayout>{buildAdmin(["show-fields", resourceName], props)}</SimpleShowLayout>
    </Show>
  )
}

setupAdmin(["show"], (props) => <MuffinResourceShow {...props} />)
setupAdmin(["show-fields"], ({ fields }) => buildRA(fields))
setupAdmin(["record-actions"], ({ actions }: { actions: AdminAction[] }) =>
  actions.map((props, idx) => <ActionButton key={idx} {...props} />)
)
setupAdmin(["record-links"], ({ links }: { links: AdminShowProps["links"] }) =>
  links.map(([key, props]) => <LinkAction key={key} resource={key} {...props} />)
)
setupAdmin(["show-actions"], ({ actions, links, edit }: AdminShowProps) => {
  const resourceName = useResourceContext()
  const Actions = findBuilder(["record-actions", resourceName])
  const Links = findBuilder(["record-links", resourceName])
  return (
    <TopToolbar>
      <div style={{ marginRight: "auto" }}>
        <Links links={links} />
      </div>
      <Actions actions={actions} />
      <ListButton />
      {edit && <EditButton />}
    </TopToolbar>
  )
})
