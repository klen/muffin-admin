import { Dialog, DialogActions, DialogContent, DialogProps, DialogTitle } from "@mui/material"
import { PropsWithChildren } from "react"
import { SxProps, Theme } from "@mui/material/styles"

interface IProps extends Omit<DialogProps, "title" | "open" | "onClose"> {
  open: boolean
  onClose: () => void
  title?: React.ReactNode
  actions?: React.ReactNode
  contentSx?: SxProps<Theme>
}

export function AdminModal({
  open,
  onClose,
  children,
  title,
  actions,
  contentSx,
  ...props
}: PropsWithChildren<IProps>) {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md" {...props}>
      {title && <DialogTitle>{title}</DialogTitle>}
      <DialogContent sx={contentSx}>{children}</DialogContent>
      {actions && <DialogActions>{actions}</DialogActions>}
    </Dialog>
  )
}
