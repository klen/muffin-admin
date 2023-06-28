import React from "react"

import { Resource } from "react-admin"
import * as icons from "@mui/icons-material"

import { checkParams, processAdmin, setupAdmin } from "./utils"
import "./views/list"
import "./views/show"
import "./views/edit"
import "./views/create"

// Initialize Resources Components
setupAdmin("resources", ({ resources, adminProps }) =>
  resources.map((resource) =>
    processAdmin("resource", { resource, adminProps }, resource.name)
  )
)

// Initialize a resource's component
setupAdmin(
  "resource",
  checkParams((props, name) => {
    let { resource, adminProps } = props
    let { create, edit, icon, list, show, ...resProps } = resource

    return (
      <Resource
        key={name}
        name={name}
        icon={icons[icon]}
        create={processAdmin("create", create, name)}
        edit={processAdmin("edit", { edit, adminProps }, name)}
        list={processAdmin("list", list, name)}
        show={processAdmin("show", show, name)}
        {...resProps}
      />
    )
  })
)
