import { PropsWithChildren } from "react"
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
import { useMuffinAdminOpts, useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinEdit({ children }: PropsWithChildren) {
  const {
    adminProps: { mutationMode = "optimistic" },
  } = useMuffinAdminOpts()
  const { edit, name } = useMuffinResourceOpts()
  if (!edit) return null

  const { inputs, remove } = edit
  const ActionsToolbar = findBuilder(["edit-toolbar", name])

  return (
    <Edit actions={<ActionsToolbar />} mutationMode={mutationMode}>
      {children}
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

export function MuffinEditToolbar({ children }: PropsWithChildren) {
  const resource = useResourceContext()
  const Actions = findBuilder(["edit-actions", resource])
  return (
    <TopToolbar>
      <Actions />
      {children}
      <ListButton />
      <ShowButton />
    </TopToolbar>
  )
}

setupAdmin(["edit-toolbar"], MuffinEditToolbar)

export function MuffinEditActions({ children }: PropsWithChildren) {
  const { edit, actions: baseActions = [] } = useMuffinResourceOpts()
  if (!edit) return null
  const actions = baseActions.filter((a) => a.view?.includes("edit"))
  return (
    <>
      {children}
      {actions.map((props, idx) => (
        <ActionButton key={idx} {...props} />
      ))}
    </>
  )
}

setupAdmin(["edit-actions"], MuffinEditActions)
