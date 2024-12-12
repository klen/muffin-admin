import CopyIcon from "@mui/icons-material/FileCopy"

import { Snackbar } from "@mui/material"
import { useState } from "react"

export function CopyButton({ value }) {
  const [open, setOpen] = useState(false)
  const handleClick = (e: any) => {
    setOpen(true)
    navigator.clipboard.writeText(value)
    e.stopPropagation()
  }
  return (
    <span title="Copy to clipboard">
      <CopyIcon color="info" fontSize="small" onClick={handleClick} style={{ cursor: "pointer" }} />
      <Snackbar
        open={open}
        autoHideDuration={2000}
        onClose={() => setOpen(false)}
        message={`Copied to clipboard: ${value}`}
      />
    </span>
  )
}
