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

export function MuffinResourceEdit() {
  const {
    adminProps: { mutationMode = "optimistic" },
  } = useMuffinAdminOpts()
  const { edit, name } = useMuffinResourceOpts()
  if (!edit) return null

  const { inputs, remove } = edit
  const Actions = findBuilder(["edit-actions", name]) as unknown as any

  return (
    <Edit actions={<Actions />} mutationMode={mutationMode}>
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

setupAdmin(["edit"], MuffinResourceEdit)

function MuffinResourceEditActions() {
  const { edit } = useMuffinResourceOpts()
  if (!edit) return null
  const { actions = [] } = edit
  return (
    <TopToolbar>
      {actions.map((props, idx) => (
        <ActionButton key={idx} {...props} />
      ))}
      <ListButton />
      <ShowButton />
    </TopToolbar>
  )
}

setupAdmin(["edit-actions"], MuffinResourceEditActions)

setupAdmin(["edit-inputs"], buildRA)
