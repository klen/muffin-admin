import IconButton from "@mui/material/IconButton"
import SvgIcon from "@mui/material/SvgIcon"
import Tooltip from "@mui/material/Tooltip"
import Typography from "@mui/material/Typography"
import {
  Admin,
  AdminProps,
  AppBar,
  AppBarProps,
  AuthProvider,
  DataProvider,
  Layout,
  LayoutProps,
  Login,
} from "react-admin"

import { useMuffinAdminOpts } from "./hooks"
import { buildAdmin, findBuilder, findIcon, setupAdmin } from "./utils"

export function MuffinAdmin(props: AdminProps) {
  const opts = useMuffinAdminOpts()
  const { resources = [], auth, adminProps, apiUrl } = opts

  document.title = adminProps?.title || "Muffin Admin"
  const authProvider = findBuilder(["authprovider"])(auth) as AuthProvider
  const dataProvider = findBuilder(["dataprovider"])(apiUrl) as DataProvider

  return (
    <Admin
      requireAuth={auth.required}
      authProvider={authProvider}
      dataProvider={dataProvider}
      layout={findBuilder(["layout"])}
      loginPage={findBuilder(["loginpage"])}
      dashboard={findBuilder(["dashboard"])}
      darkTheme={{ palette: { mode: "dark" } }}
      {...props}
    >
      {resources?.map(({ name }) => buildAdmin(["resource", name], { name }))}
    </Admin>
  )
}

setupAdmin(["admin"], MuffinAdmin)

export function MuffinAdminLayout(props: LayoutProps) {
  return <Layout {...props} appBar={findBuilder(["appbar"])} />
}

setupAdmin(["layout"], MuffinAdminLayout)

export function MuffinAppBar(props: AppBarProps) {
  const { appBarLinks } = useMuffinAdminOpts()
  return (
    <AppBar {...props}>
      <Typography
        variant="h6"
        color="inherit"
        id="react-admin-title"
        style={{
          flex: 1,
          overflow: "hidden",
          whiteSpace: "nowrap",
          textOverflow: "ellipsis",
        }}
      />
      {appBarLinks.map((info) => (
        <Tooltip key={info.url} title={info.title}>
          <IconButton color="inherit" href={info.url}>
            <SvgIcon component={findIcon(info.icon)} />
          </IconButton>
        </Tooltip>
      ))}
    </AppBar>
  )
}

setupAdmin(["appbar"], MuffinAppBar)

// Initialize login page
setupAdmin(["loginpage"], Login)
