import HelpIcon from "@mui/icons-material/Help"
import Link from "@mui/material/Link"
import { Button, useTranslate } from "react-admin"

export function HelpLink({ label, ...props }: Parameters<typeof Button>[0]) {
  const translate = useTranslate()
  label = label || translate("muffin.instructions")
  return (
    <Button component={Link} label={label} target="_blank" {...props}>
      <HelpIcon />
    </Button>
  )
}
