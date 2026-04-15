import { ReferenceField, TextField, useFieldValue, UseFieldValueOptions } from "react-admin"
import { useLocation } from "react-router-dom"

export function FKField({ reference, refSource, refKey, link, source, ...props }) {
  const location = useLocation()
  refKey = refKey || "id"
  const returnTo = `${location.pathname}${location.search}`

  const resolveLink =
    link ||
    ((record) => {
      const id = record?.[refKey]
      if (id === undefined || id === null) return false
      return `/${reference}/${id}/show?returnTo=${encodeURIComponent(returnTo)}`
    })

  return (
    <ReferenceField
      source={source}
      link={resolveLink}
      reference={reference}
      queryOptions={{ meta: { key: refKey } }}
      {...props}
    >
      <TextField source={refSource} />
      {refSource !== refKey && <FKFieldValue source={refKey} />}
    </ReferenceField>
  )
}

function FKFieldValue(props: UseFieldValueOptions) {
  const value = useFieldValue(props)
  if (value === undefined) return null
  return (
    <>
      {" (#"}
      <TextField {...props} />
      {")"}
    </>
  )
}

FKField.displayName = "FKField"
