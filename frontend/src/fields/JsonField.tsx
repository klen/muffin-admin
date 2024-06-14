import get from "lodash/get"
import { useState } from "react"
import { Button, FunctionField, useRecordContext } from "react-admin"

export function JsonField({ label, source }) {
  const [expand, setExpand] = useState(false)
  const record = useRecordContext()
  const value = get(record, source)
  if (!value || Object.keys(value).length == 0) return null

  const src = JSON.stringify(value, null, 2)
  const retval = (
    <div>
      <p></p>
      {label}
      <Button
        variant="contained"
        color="primary"
        size="small"
        label={expand ? "colapse" : "expand"}
        onClick={(e) => {
          setExpand(!expand)
          e.stopPropagation()
        }}
      />
      <p>{expand && <pre>{src}</pre>}</p>
    </div>
  )

  return <FunctionField render={() => retval} />
}
