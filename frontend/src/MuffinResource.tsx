import React from "react"
import { Resource } from "react-admin"
import { AdminResourceProps } from "./types"
import { buildAdmin, findIcon, setupAdmin } from "./utils"

export function MuffinResource({
  name,
  create: createProps,
  edit: editProps,
  list: listProps,
  show: showProps,
  icon,
  ...props
}: AdminResourceProps) {
  return (
    <Resource
      name={name}
      icon={findIcon(icon)}
      create={buildAdmin(["create", name], createProps)}
      edit={buildAdmin(["edit", name], editProps)}
      list={buildAdmin(["list", name], listProps)}
      show={buildAdmin(["show", name], showProps)}
      {...props}
    />
  )
}

setupAdmin(["resource"], MuffinResource)
