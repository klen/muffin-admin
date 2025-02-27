import TextField from "@mui/material/TextField"
import { enGB, ru } from "date-fns/locale"
import { FieldTitle, InputProps, useLocale } from "react-admin"
import DatePicker, { registerLocale } from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css"

registerLocale("ru", ru)
registerLocale("en", enGB)

type TProps = InputProps & {
  value: [Date, Date]
  onChange: (value: [Date, Date]) => void
}

export function DateRangeInput({ value, onChange, ...props }: TProps) {
  const [startDate, endDate] = value
  const locale = useLocale()
  const { label, source, resource, isRequired } = props

  return (
    <DatePicker
      withPortal
      locale={locale}
      selectsRange
      endDate={endDate}
      onChange={onChange}
      startDate={startDate}
      customInput={
        <TextField
          variant="outlined"
          label={
            <FieldTitle label={label} source={source} resource={resource} isRequired={isRequired} />
          }
        />
      }
    />
  )
}
