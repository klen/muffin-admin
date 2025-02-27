import { useInput } from "react-admin"
import { DateRangeInput } from "../inputs/DateRangeInput"

export function DateRangeFilter(props) {
  const { field } = useInput(props)

  const onChange = (dates: [Date, Date]) => {
    field.onChange({
      $between: dates.map((d) => d?.toISOString() || null),
    })
  }
  let filterValue = field.value.$between ?? [null, null]
  if (!Array.isArray(filterValue)) filterValue = [null, null]
  const value = filterValue.map((d: string) => (d ? new Date(d) : d))

  return <DateRangeInput value={value} onChange={onChange} {...props} />
}
