import { useRecordContext, useResourceContext } from "react-admin"
import LinkButton from "../buttons/LinkButton"
import { AdminShowLink } from "../types"

export function LinkAction(props: AdminShowLink & { resource: string }) {
  const record = useRecordContext()
  const currentResource = useResourceContext()
  if (!record) return null
  return <LinkButton {...props} filters={{ [currentResource]: record.id }} />
}
