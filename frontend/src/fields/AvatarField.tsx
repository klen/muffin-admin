import Avatar from "@mui/material/Avatar"
import CircularProgress from "@mui/material/CircularProgress"
import get from "lodash/get"
import { useRecordContext } from "ra-core"

export function AvatarField({ source, alt, style, nameProp, ...props }) {
  const record = useRecordContext(props)
  let value = get(record, source),
    name = record[nameProp]

  // Check value is a valid URL
  if (value) {
    try {
      new URL(value);
    } catch {
      // Not a valid URL, return loader
      return (
        <CircularProgress size={24} />
      )
    }
  }

  const letters = name
    ? name
      .trim(" ")
      .split(/\s+/)
      .slice(0, 2)
      .map((n: string) => n[0]?.toUpperCase())
      .join("")
    : ""

  return (
    <Avatar src={value} alt={alt} style={style}>
      {letters}
    </Avatar>
  )
}

AvatarField.displayName = "AvatarField"
