import { Stack } from "@mui/material"
import { Button } from "react-admin"
import { useFormContext } from "react-hook-form"

export function PayloadButtons({ onClose, onSubmit }) {
  const { formState } = useFormContext()
  return (
    <Stack direction="row" alignItems="center" justifyContent="flex-end" spacing={1}>
      <Button
        label="ra.action.confirm"
        variant="contained"
        disabled={!formState.isValid}
        size="medium"
        onClick={onSubmit}
      />
      <Button label="ra.action.cancel" variant="outlined" size="medium" onClick={onClose} />
    </Stack>
  )
}
