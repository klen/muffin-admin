import React from "react"
import { Admin, DataProvider, Layout } from "react-admin"
import { AdminOpts } from "./types"
import { AdminPropsContext, buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinAdmin(props: AdminOpts) {
  const { resources, auth } = props
  const children = resources.map((resource) =>
    buildAdmin(["resource", resource.name], {
      ...resource,
      key: resource.name,
    })
  )
  return (
    <AdminPropsContext.Provider value={props}>
      <Admin
        authProvider={buildAdmin(["authprovider"], auth)}
        dataProvider={
          buildAdmin(["dataprovider"], props) as unknown as DataProvider
        }
        loginPage={findBuilder(["loginpage"])}
        layout={findBuilder(["layout"])}
        dashboard={buildAdmin(["dashboard"])}
        requireAuth={auth.required}
      >
        {children}
      </Admin>
    </AdminPropsContext.Provider>
  )
}

setupAdmin(["admin"], MuffinAdmin)
setupAdmin(["layout"], Layout)
