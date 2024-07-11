import { Stack } from "@mui/material"
import { Button } from "react-admin"

export function PayloadButtons({
  onClose,
  onSubmit,
  isValid = true,
}: {
  onClose: () => void
  onSubmit?: (e: any) => void
  isValid: boolean
}) {
  return (
    <Stack direction="row" alignItems="center" justifyContent="flex-end" spacing={1}>
      <Button
        label="ra.action.confirm"
        variant="contained"
        disabled={!isValid}
        size="medium"
        onClick={onSubmit}
      />
      <Button label="ra.action.cancel" variant="outlined" size="medium" onClick={onClose} />
    </Stack>
  )
}
