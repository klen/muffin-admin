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
import { buildAdmin, setupAdmin } from "./utils"

export function MuffinResourceShow(props: AdminShowProps) {
  const resourceName = useResourceContext()
  return (
    <Show actions={buildAdmin(["show-actions", resourceName], props)}>
      <SimpleShowLayout>{buildAdmin(["show-fields", resourceName], props)}</SimpleShowLayout>
    </Show>
  )
}

setupAdmin(["show"], (props) => <MuffinResourceShow {...props} />)
setupAdmin(["show-fields"], ({ fields }) => buildRA(fields))
setupAdmin(["record-actions"], (actions: AdminAction[]) =>
  actions.map((props, idx) => <ActionButton key={idx} {...props} />)
)
setupAdmin(["show-actions"], ({ actions, links, edit }: AdminShowProps) => {
  const resourceName = useResourceContext()
  return (
    <TopToolbar>
      <div style={{ marginRight: "auto" }}>
        {links.map(([key, props]) => (
          <LinkAction key={key} resource={key} {...props} />
        ))}
      </div>
      {buildAdmin(["record-actions", resourceName], actions)}
      <ListButton />
      {edit && <EditButton />}
    </TopToolbar>
  )
})
