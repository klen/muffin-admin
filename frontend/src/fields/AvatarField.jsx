import React from "react"
import get from "lodash/get"
import { useRecordContext } from "ra-core"
import Avatar from "@mui/material/Avatar"

const AvatarField = ({ source, alt, style, nameProp, ...props }) => {
  const record = useRecordContext(props)

  let value = get(record, source),
    name = record[nameProp]

  const letters = name
    ? name
        .trim(" ")
        .split(/\s+/)
        .slice(0, 2)
        .map((n) => n[0].toUpperCase())
        .join("")
    : ""

  return (
    <Avatar src={value} alt={alt} style={style}>
      {letters}
    </Avatar>
  )
}

AvatarField.displayName = "AvatarField"
AvatarField.defaultProps = {
  addLabel: true,
}

export default AvatarField
