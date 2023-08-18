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
import { AdminShowProps } from "./types"
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
setupAdmin(["show-actions"], ({ actions, links }) => (
  <TopToolbar>
    <div style={{ marginRight: "auto" }}>
      {Object.keys(links).map((key) => (
        <LinkAction key={key} resource={key} {...links[key]} />
      ))}
    </div>
    {actions.map((props, idx) => (
      <ActionButton key={idx} {...props} />
    ))}
    <ListButton />
    <EditButton />
  </TopToolbar>
))
