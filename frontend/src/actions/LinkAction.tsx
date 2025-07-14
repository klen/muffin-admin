import { useRecordContext, useResourceContext } from "react-admin"
import LinkButton from "../buttons/LinkButton"
import { useMuffinAdminOpts } from "../hooks"
import { AdminShowLink } from "../types"

export function LinkAction({
  field,
  filter,
  icon,
  label,
  ...props
}: AdminShowLink & { resource: string }) {
  const record = useRecordContext()
  const { resources } = useMuffinAdminOpts()
  const currentResource = useResourceContext()

  if (!record) return null

  const resource = resources.find((r) => r.name === props.resource)

  return (
    <LinkButton
      {...props}
      icon={icon || resource?.icon}
      label={label || `resources.${props.resource}.name`}
      filters={{ [filter || currentResource]: encodeURIComponent(record[field || "id"]) }}
    />
  )
}
