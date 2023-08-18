import { useContext } from "react"
import { useRecordContext, useResourceContext } from "react-admin"
import LinkButton from "../buttons/LinkButton"
import { AdminShowLink } from "../types"
import { AdminPropsContext } from "../utils"

export function LinkAction({ fk, icon, ...props }: AdminShowLink & { resource: string }) {
  const adminProps = useContext(AdminPropsContext)
  const record = useRecordContext()
  const currentResource = useResourceContext()
  if (!record) return null

  icon = icon || adminProps?.resources[props.resource]?.icon

  return <LinkButton {...props} icon={icon} filters={{ [currentResource]: record[fk || "id"] }} />
}
