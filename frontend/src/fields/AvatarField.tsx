import Avatar from "@mui/material/Avatar"
import get from "lodash/get"
import { useRecordContext } from "ra-core"

export function AvatarField({ source, alt, style, nameProp, ...props }) {
  const record = useRecordContext(props)
  const value = get(record, source),
    name = record[nameProp]

  const letters = name
    ? name
        .trim(" ")
        .split(/\s+/)
        .slice(0, 2)
        .map((n: string) => n[0].toUpperCase())
        .join("")
    : ""

  return (
    <Avatar src={value} alt={alt} style={style}>
      {letters}
    </Avatar>
  )
}

AvatarField.displayName = "AvatarField"
