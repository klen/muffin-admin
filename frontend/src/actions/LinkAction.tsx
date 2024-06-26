import { useRecordContext, useResourceContext } from "react-admin"
import LinkButton from "../buttons/LinkButton"
import { useMuffinAdminOpts } from "../hooks"
import { AdminShowLink } from "../types"

export function LinkAction({ field, icon, ...props }: AdminShowLink & { resource: string }) {
  const { resources } = useMuffinAdminOpts()
  const record = useRecordContext()
  const currentResource = useResourceContext()
  if (!record) return null

  const resource = resources.find((r) => r.name === props.resource)

  return (
    <LinkButton
      {...props}
      icon={icon || resource?.icon}
      filters={{ [currentResource]: encodeURIComponent(record[field || "id"]) }}
    />
  )
}
