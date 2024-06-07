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
      key={name}
      name={name}
      icon={findIcon(icon)}
      create={createProps ? buildAdmin(["create", name], createProps) : undefined}
      edit={editProps ? buildAdmin(["edit", name], editProps) : undefined}
      list={buildAdmin(["list", name], listProps)}
      show={buildAdmin(["show", name], showProps)}
      {...props}
    />
  )
}

setupAdmin(["resource"], MuffinResource)
