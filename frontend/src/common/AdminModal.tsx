import { Dialog, DialogActions, DialogContent, DialogProps, DialogTitle } from "@mui/material"
import { PropsWithChildren } from "react"

interface IProps {
  open: boolean
  onClose: () => void
  title?: string
  actions?: React.ReactNode
}

export function AdminModal({
  open,
  onClose,
  children,
  title,
  actions,
  ...props
}: PropsWithChildren<IProps & DialogProps>) {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md" {...props}>
      {title && <DialogTitle>{title}</DialogTitle>}
      <DialogContent>{children}</DialogContent>
      {actions && <DialogActions>{actions}</DialogActions>}
    </Dialog>
  )
}
