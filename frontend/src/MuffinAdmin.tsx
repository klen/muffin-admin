import IconButton from "@mui/material/IconButton"
import SvgIcon from "@mui/material/SvgIcon"
import Tooltip from "@mui/material/Tooltip"
import Typography from "@mui/material/Typography"
import createTheme from "@mui/material/styles/createTheme"
import {
  Admin,
  AppBar,
  DataProvider,
  Layout,
  Login,
  ToggleThemeButton,
  defaultTheme,
} from "react-admin"
import { AdminOpts } from "./types"
import { AdminPropsContext, buildAdmin, findBuilder, findIcon, setupAdmin } from "./utils"

const darkTheme = createTheme({
  palette: { mode: "dark" },
})

export function MuffinAdmin(props: AdminOpts) {
  const { resources, auth, appBarLinks, dashboard } = props
  const children = resources.map((resource) =>
    buildAdmin(["resource", resource.name], {
      ...resource,
      key: resource.name,
    })
  )
  const appBar = (props) => (
    <AppBar {...props}>
      <Typography
        variant="h6"
        color="inherit"
        id="react-admin-title"
        style={{
          flex: 1,
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
          overflow: "hidden",
        }}
      />
      <ToggleThemeButton lightTheme={defaultTheme} darkTheme={darkTheme} />
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
    <AdminPropsContext.Provider value={props}>
      <Admin
        authProvider={buildAdmin(["authprovider"], auth)}
        dashboard={buildAdmin(["dashboard"], dashboard)}
        dataProvider={buildAdmin(["dataprovider"], props) as unknown as DataProvider}
        layout={(props) => <Layout {...props} appBar={appBar} />}
        loginPage={findBuilder(["loginpage"])}
        requireAuth={auth.required}
      >
        {children}
      </Admin>
    </AdminPropsContext.Provider>
  )
}

setupAdmin(["admin"], MuffinAdmin)

// Initialize login page
setupAdmin(["loginpage"], Login)
