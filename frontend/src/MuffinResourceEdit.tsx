import {
  DeleteButton,
  Edit,
  ListButton,
  SaveButton,
  ShowButton,
  SimpleForm,
  Toolbar,
  TopToolbar,
} from "react-admin"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"
import { useMuffinAdminOpts, useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinEdit() {
  const {
    adminProps: { mutationMode = "optimistic" },
  } = useMuffinAdminOpts()
  const { edit, name } = useMuffinResourceOpts()
  if (!edit) return null

  const { inputs, remove } = edit
  const ActionsToolbar = findBuilder(["edit-toolbar", name])

  return (
    <Edit actions={<ActionsToolbar />} mutationMode={mutationMode}>
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
        {buildAdmin(["edit-inputs", name], inputs)}
      </SimpleForm>
    </Edit>
  )
}

setupAdmin(["edit"], MuffinEdit)
setupAdmin(["edit-inputs"], buildRA)

export function MuffinEditToolbar() {
  const { name } = useMuffinResourceOpts()
  const Actions = findBuilder(["edit-actions", name])
  return (
    <TopToolbar>
      <Actions />
      <ListButton />
      <ShowButton />
    </TopToolbar>
  )
}

setupAdmin(["edit-toolbar"], MuffinEditToolbar)

export function MuffinEditActions() {
  const { edit, actions: baseActions = [] } = useMuffinResourceOpts()
  if (!edit) return null
  const actions = baseActions.filter((a => a.view.includes("edit")))
  return (
    <>
      {actions.map((props, idx) => (
        <ActionButton key={idx} {...props} />
      ))}
    </>
  )
}

setupAdmin(["edit-actions"], MuffinEditActions)
