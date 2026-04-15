import { Box, Typography } from "@mui/material"
import { PropsWithChildren } from "react"
import {
  EditButton,
  ListButton,
  Show,
  SimpleShowLayout,
  TopToolbar,
  useRecordContext,
  useTranslate,
} from "react-admin"
import { useLocation, useNavigate } from "react-router-dom"
import { LinkAction } from "./actions"
import { buildRA } from "./buildRA"
import { ActionButton } from "./buttons"
import { AdminModal } from "./common"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinShow({ children }: PropsWithChildren) {
  const { show, name, key } = useMuffinResourceOpts()
  const location = useLocation()
  const navigate = useNavigate()
  const ShowToolbar = findBuilder(["show-toolbar", name])
  const returnTo = new URLSearchParams(location.search).get("returnTo")

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

  return (
    <Show
      actions={false}
      title={false}
      component="div"
      queryOptions={{ meta: { key } }}
      sx={{
        "& .RaShow-main": {
          padding: 0,
        },
      }}
    >
      <AdminModal
        open={true}
        onClose={handleClose}
        title={<ShowToolbar />}
        maxWidth="xl"
        hideBackdrop
        disableScrollLock
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
        <SimpleShowLayout
          sx={{
            padding: 0,
            "& .RaSimpleShowLayout-stack": {
              rowGap: 1,
            },
          }}
        >
          {buildAdmin(["show-fields", name], show)}
        </SimpleShowLayout>
        {children}
      </AdminModal>
    </Show>
  )
}

setupAdmin(["show"], MuffinShow)
setupAdmin(["show-fields"], ({ fields }) => buildRA(fields))

export function MuffinShowToolbar() {
  const { show, name } = useMuffinResourceOpts()
  const record = useRecordContext()
  const translate = useTranslate()
  const { edit } = show

  const Links = findBuilder(["show-links", name])
  const Actions = findBuilder(["show-actions", name])

  return (
    <Box sx={{ display: "flex", flexDirection: "column", width: "100%" }}>
      <TopToolbar sx={{ pl: 0, pr: 0, width: "100%", justifyContent: "space-between" }}>
        <Typography variant="h6" sx={{ mr: 2 }}>
          {translate(`resources.${name}.name`, { smart_count: 1, _: name })}
          {record?.id ? ` #${record.id}` : ""}
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <Actions />
          {edit && <EditButton />}
          <ListButton />
        </Box>
      </TopToolbar>
      <Box sx={{ mt: 0.5 }}>
        <Links />
      </Box>
    </Box>
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
    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
      {links.map(([key, props]) => (
        <LinkAction key={key} resource={key} {...props} />
      ))}
      {children}
    </Box>
  )
}

setupAdmin(["show-links"], MuffinShowLinks)
