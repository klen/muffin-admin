import IconButton from "@mui/material/IconButton"
import SvgIcon from "@mui/material/SvgIcon"
import Tooltip from "@mui/material/Tooltip"
import Typography from "@mui/material/Typography"
import { Admin, AdminProps, AppBar, DataProvider, Layout, Login } from "react-admin"
import { AdminOpts } from "./types"
import { AdminPropsContext, buildAdmin, findBuilder, findIcon, setupAdmin } from "./utils"

export function MuffinAdmin(opts: AdminOpts, props: AdminProps) {
  const { resources, auth, appBarLinks, adminProps, dashboard } = opts
  const children = resources?.map((resource) =>
    buildAdmin(["resource", resource.name], { ...resource })
  )

  document.title = adminProps?.title || "Muffin Admin"

  const appBar = (props) => (
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

  return (
    <AdminPropsContext.Provider value={opts}>
      <Admin
        authProvider={buildAdmin(["authprovider"], auth)}
        dataProvider={buildAdmin(["dataprovider"], opts) as unknown as DataProvider}
        layout={(props) => <Layout {...props} appBar={appBar} />}
        loginPage={findBuilder(["loginpage"])}
        dashboard={dashboard ? buildAdmin(["dashboard"], dashboard) : null}
        requireAuth={auth.required}
        darkTheme={{ palette: { mode: "dark" } }}
        {...props}
      >
        {children}
      </Admin>
    </AdminPropsContext.Provider>
  )
}

setupAdmin(["admin"], MuffinAdmin)

// Initialize login page
setupAdmin(["loginpage"], Login)
