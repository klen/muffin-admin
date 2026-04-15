import { Box, Typography } from "@mui/material"
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
  useRecordContext,
  useResourceContext,
  useTranslate,
} from "react-admin"
import { useLocation, useNavigate } from "react-router-dom"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"
import { AdminModal } from "./common"
import { useMuffinAdminOpts, useMuffinResourceOpts } from "./hooks"
import { findBuilder, setupAdmin } from "./utils"

export function MuffinEdit({ children }: PropsWithChildren) {
  const {
    adminProps: { mutationMode = "optimistic" },
  } = useMuffinAdminOpts()

  const { edit, name, key } = useMuffinResourceOpts()
  const location = useLocation()
  const navigate = useNavigate()
  const returnTo = new URLSearchParams(location.search).get("returnTo")
  if (!edit) return null

  const handleClose = () => {
    if (returnTo) {
      navigate(returnTo)
      return
    }

    if (window.history.length > 1) {
      navigate(-1)
      return
    }

    navigate(`/${name}`)
  }

  const Actions = findBuilder(["edit-toolbar", name])
  const Inputs = findBuilder(["edit-inputs", name])
  const FormToolbar = findBuilder(["edit-form-toolbar", name])

  return (
    <Edit
      actions={false}
      title={false}
      component="div"
      mutationMode={mutationMode}
      queryOptions={{ meta: { key } }}
      sx={{
        "& .RaEdit-main": {
          padding: 0,
        },
      }}
    >
      <AdminModal
        open={true}
        onClose={handleClose}
        title={<Actions />}
        maxWidth="xl"
        contentSx={{
          paddingTop: "8px !important",
          paddingBottom: "12px !important",
          paddingLeft: "16px !important",
          paddingRight: "16px !important",
        }}
        sx={{
          "& .MuiDialog-paper": {
            width: "min(1400px, 96vw)",
          },
        }}
      >
        {children}
        <SimpleForm toolbar={<FormToolbar />}>
          <Inputs />
        </SimpleForm>
      </AdminModal>
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
  const record = useRecordContext()
  const translate = useTranslate()
  const Actions = findBuilder(["edit-actions", resource])
  return (
    <Box sx={{ display: "flex", flexDirection: "column", width: "100%" }}>
      <TopToolbar sx={{ pl: 0, pr: 0, width: "100%", justifyContent: "space-between" }}>
        <Typography variant="h6" sx={{ mr: 2 }}>
          {translate(`resources.${resource}.name`, { smart_count: 1, _: resource })}
          {record?.id ? ` #${record.id}` : ""}
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <Actions />
          {children}
          <ShowButton />
          <ListButton />
        </Box>
      </TopToolbar>
    </Box>
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
