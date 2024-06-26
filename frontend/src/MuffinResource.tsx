import { Resource, ResourceProps } from "react-admin"
import { useMuffinAdminOpts } from "./hooks"
import { findBuilder, findIcon, setupAdmin } from "./utils"

export function MuffinResource({ name, ...props }: ResourceProps) {
  const adminOpts = useMuffinAdminOpts()
  const opts = adminOpts?.resources.find((r) => r.name == name)
  if (!opts) return null

  return (
    <Resource
      key={name}
      name={name}
      icon={findIcon(opts.icon)}
      create={findBuilder(["create", name])}
      edit={findBuilder(["edit", name])}
      list={findBuilder(["list", name])}
      show={findBuilder(["show", name])}
      {...props}
    />
  )
}

setupAdmin(["resource"], MuffinResource)
