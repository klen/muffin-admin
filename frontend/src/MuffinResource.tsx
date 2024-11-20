import { Resource, ResourceProps } from "react-admin"
import { useMuffinAdminOpts } from "./hooks"
import { findBuilder, findIcon, setupAdmin } from "./utils"

export function MuffinResource({ name, ...props }: ResourceProps) {
  const adminOpts = useMuffinAdminOpts()
  const opts = adminOpts?.resources.find((r) => r.name == name)
  if (!opts) return null

  const Create = findBuilder(["create", name])
  const Edit = findBuilder(["edit", name])
  const List = findBuilder(["list", name])
  const Show = findBuilder(["show", name])

  return (
    <Resource
      key={name}
      name={name}
      icon={findIcon(opts.icon)}
      create={Create}
      edit={Edit}
      list={List}
      show={Show}
      {...props}
    />
  )
}

setupAdmin(["resource"], MuffinResource)
