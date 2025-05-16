import IconButton from "@mui/material/IconButton"
import SvgIcon from "@mui/material/SvgIcon"
import Tooltip from "@mui/material/Tooltip"

import Typography from "@mui/material/Typography"
import {
  AdminContext,
  AdminProps,
  AdminUI,
  AppBar,
  AppBarProps,
  Layout,
  LayoutProps,
  localStorageStore,
  Login,
  LoginProps,
} from "react-admin"

import { useEffect } from "react"
import { ConfirmationProvider } from "./common"
import { useMuffinAdminOpts } from "./hooks"
import { buildProvider, muffinTranslations } from "./i18n"
import { buildAdmin, deepMerge, findBuilder, findIcon, setupAdmin } from "./utils"

export function MuffinAdmin(props: AdminProps) {
  const opts = useMuffinAdminOpts()
  const { resources = [], auth, adminProps, apiUrl, locales: backendLocales } = opts

  document.title = adminProps?.title || "Muffin Admin"
  const muffinI18nProvider = buildProvider(
    backendLocales
      ? Object.fromEntries(
          Object.entries(muffinTranslations).map(([locale, messages]) => [
            locale,
            deepMerge({}, messages, backendLocales[locale], buildAdmin(["locale", locale]) || {}),
          ])
        )
      : muffinTranslations
  )

  const {
    basename,
    authProvider = findBuilder(["auth-provider"])(auth),
    dataProvider = findBuilder(["data-provider"])(apiUrl),
    catchAll,
    dashboard = findBuilder(["dashboard"]),
    disableTelemetry,
    error,
    i18nProvider = muffinI18nProvider,
    layout = findBuilder(["layout"]),
    loading,
    loginPage = findBuilder(["loginpage"]),
    authCallbackPage,
    notification,
    queryClient,
    requireAuth = auth.required,
    store = localStorageStore(),
    ready,
    theme,
    lightTheme,
    darkTheme,
    defaultTheme,
    title = "React Admin",
  } = props

  return (
    <AdminContext
      authProvider={authProvider}
      basename={basename}
      dataProvider={dataProvider}
      i18nProvider={i18nProvider}
      store={store}
      queryClient={queryClient}
      theme={theme}
      lightTheme={lightTheme}
      darkTheme={darkTheme}
      defaultTheme={defaultTheme}
    >
      <ConfirmationProvider>
        <AdminUI
          layout={layout}
          dashboard={dashboard}
          disableTelemetry={disableTelemetry}
          catchAll={catchAll}
          error={error}
          title={title}
          loading={loading}
          loginPage={loginPage}
          authCallbackPage={authCallbackPage}
          notification={notification}
          requireAuth={requireAuth}
          ready={ready}
        >
          {resources?.map(({ name }) => buildAdmin(["resource", name], { name }))}
        </AdminUI>
      </ConfirmationProvider>
    </AdminContext>
  )
}

setupAdmin(["admin"], MuffinAdmin)

export function MuffinAdminLayout(props: LayoutProps) {
  return <Layout {...props} appBar={findBuilder(["appbar"])} menu={findBuilder(["menu"])} />
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

export function MuffinLogin(props: LoginProps) {
  const {
    auth: { loginURL },
  } = useMuffinAdminOpts()
  useEffect(() => {
    if (loginURL) window.location.replace(loginURL)
  }, [loginURL])
  return <Login {...props} />
}

// Initialize login page
setupAdmin(["loginpage"], MuffinLogin)
