import { Button, Typography } from "@mui/material"
import { createContext, PropsWithChildren, useContext, useState } from "react"
import { useTranslate } from "react-admin"
import { AdminModal } from "./AdminModal"

type TConfirmProps = {
  title?: string
  message: string
  actions?: React.ReactNode
}

type TConfirmContext = {
  confirm: (props: TConfirmProps) => Promise<boolean>
}

export const ConfirmContext = createContext<TConfirmContext>({} as TConfirmContext)

export function ConfirmationProvider({ children }: PropsWithChildren) {
  const translate = useTranslate()
  const [open, setOpen] = useState(false)
  const [title, setTitle] = useState(translate("ra.message.are_you_sure"))
  const [message, setMessage] = useState(null)
  const [resolver, setResolve] = useState<null | ((value: boolean) => void)>(null)

  function handleConfirm({ title, message }: TConfirmProps) {
    setOpen(true)
    if (title) setTitle(title)
    if (message) setMessage(message)
    return new Promise<boolean>((resolve) => {
      setResolve(() => resolve)
    })
  }
  const confirmContext = {
    confirm: handleConfirm,
  }
  return (
    <ConfirmContext.Provider value={confirmContext}>
      {children}
      <AdminModal
        open={open}
        onClose={() => setOpen(false)}
        title={title}
        maxWidth="xs"
        actions={
          <>
            <Button
              variant="contained"
              onClick={() => {
                setOpen(false)
                resolver(true)
              }}
            >
              {translate("ra.action.confirm")}
            </Button>
            <Button
              variant="outlined"
              onClick={() => {
                setOpen(false)
                resolver(false)
              }}
            >
              {translate("ra.action.cancel")}
            </Button>
          </>
        }
      >
        <Typography>{message}</Typography>
      </AdminModal>
    </ConfirmContext.Provider>
  )
}

export const useConfirmation = () => {
  return useContext(ConfirmContext)
}
