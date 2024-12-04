import { format } from "date-fns"
import { DateTimeInput } from "react-admin"

export function TimestampInput({ source, ms, ...props }) {
  return (
    <DateTimeInput
      source={source}
      {...props}
      format={(v) => {
        if (!v) return ""
        const value = new Date(ms ? v : v * 1000)
        return format(value, "yyyy-MM-dd'T'HH:mm:ss")
      }}
      parse={(v) => {
        if (!v) return null
        return new Date(v).valueOf() / (ms ? 1 : 1000)
      }}
    />
  )
}
