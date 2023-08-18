import { useContext } from "react"
import { useRecordContext, useResourceContext } from "react-admin"
import LinkButton from "../buttons/LinkButton"
import { AdminShowLink } from "../types"
import { AdminPropsContext } from "../utils"

export function LinkAction({ field, icon, ...props }: AdminShowLink & { resource: string }) {
  const adminProps = useContext(AdminPropsContext)
  const record = useRecordContext()
  const currentResource = useResourceContext()
  if (!record) return null

  const resource = adminProps?.resources.find((r) => r.name === props.resource)

  return (
    <LinkButton
      {...props}
      icon={icon || resource?.icon}
      filters={{ [currentResource]: encodeURIComponent(record[field || "id"]) }}
    />
  )
}
