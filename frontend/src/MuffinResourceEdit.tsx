import { useContext } from "react"
import {
  DeleteButton,
  Edit,
  ListButton,
  SaveButton,
  ShowButton,
  SimpleForm,
  Toolbar,
  TopToolbar,
  useResourceContext,
} from "react-admin"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"
import { AdminAction, AdminOpts, AdminResourceProps } from "./types"
import { AdminPropsContext, buildAdmin, setupAdmin } from "./utils"

export function MuffinResourceEdit(props: AdminResourceProps["edit"]) {
  const resourceName = useResourceContext()
  const {
    adminProps: { mutationMode },
  } = useContext(AdminPropsContext) as AdminOpts

  if (!props) return null
  const { actions, inputs, remove, ...opts } = props

  return (
    <Edit
      actions={buildAdmin(["edit-actions", resourceName], actions)}
      mutationMode={mutationMode || "optimistic"}
      {...opts}
    >
      <SimpleForm
        toolbar={
          <Toolbar>
            <SaveButton />
            {remove && (
              <DeleteButton
                sx={{
                  marginLeft: "auto",
                }}
              />
            )}
          </Toolbar>
        }
      >
        {buildAdmin(["edit-inputs", resourceName], inputs)}
      </SimpleForm>
    </Edit>
  )
}

setupAdmin(["edit"], (props) => <MuffinResourceEdit {...props} />)
setupAdmin(["edit-actions"], (actions: AdminAction[]) => (
  <TopToolbar>
    {actions.map((props, idx) => (
      <ActionButton key={idx} {...props} />
    ))}
    <ListButton />
    <ShowButton />
  </TopToolbar>
))
setupAdmin(["edit-inputs"], buildRA)
