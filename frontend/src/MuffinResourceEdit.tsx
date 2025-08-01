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
import { findBuilder, setupAdmin } from "./utils"

export function MuffinEdit({ children }: PropsWithChildren) {
  const {
    adminProps: { mutationMode = "optimistic" },
  } = useMuffinAdminOpts()

  const { edit, name, key } = useMuffinResourceOpts()
  if (!edit) return null

  const Actions = findBuilder(["edit-toolbar", name])
  const Inputs = findBuilder(["edit-inputs", name])
  const FormToolbar = findBuilder(["edit-form-toolbar", name])

  return (
    <Edit actions={<Actions />} mutationMode={mutationMode} queryOptions={{ meta: { key } }}>
      {children}
      <SimpleForm toolbar={<FormToolbar />}>
        <Inputs />
      </SimpleForm>
    </Edit>
  )
}

setupAdmin(["edit"], MuffinEdit)

export function MuffinEditFormToolbar() {
  const { edit } = useMuffinResourceOpts()
  if (!edit) return null

  const { remove } = edit
  return (
    <Toolbar>
      <SaveButton />
      {remove && <DeleteButton sx={{ marginLeft: "auto" }} />}
    </Toolbar>
  )
}

setupAdmin(["edit-form-toolbar"], MuffinEditFormToolbar)

export function MuffinEditInputs() {
  const { edit } = useMuffinResourceOpts()
  if (!edit) return null

  const { inputs } = edit

  return <>{buildRA(inputs)}</>
}
setupAdmin(["edit-inputs"], MuffinEditInputs)

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
