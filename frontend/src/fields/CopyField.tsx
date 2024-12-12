import get from "lodash/get"

import { useRecordContext } from "react-admin"
import { CopyButton } from "../buttons"

export function CopyField({ source, ...props }) {
  const record = useRecordContext(props)
  const value = get(record, source)

  if (!value) return null
  return (
    <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
      <span>{value}</span>
      <CopyButton value={value} />
    </div>
  )
}
