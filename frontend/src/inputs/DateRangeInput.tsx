import TextField from "@mui/material/TextField"
import { enGB, ru } from "date-fns/locale"
import { useLocale } from "react-admin"
import DatePicker, { registerLocale } from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css"

registerLocale("ru", ru)
registerLocale("en", enGB)

type TProps = {
  value: [Date, Date]
  onChange: (value: [Date, Date]) => void
}

export function DateRangeInput({ value, onChange }: TProps) {
  const [startDate, endDate] = value
  const locale = useLocale()
  return (
    <DatePicker
      withPortal
      locale={locale}
      selectsRange
      endDate={endDate}
      onChange={onChange}
      startDate={startDate}
      customInput={<TextField variant="outlined" />}
    />
  )
}
