import { ReferenceField, TextField, useFieldValue, UseFieldValueOptions } from "react-admin"

export function FKField({ reference, refSource, refKey, link, source, ...props }) {
  refKey = refKey || "id"
  return (
    <ReferenceField
      source={source}
      link={link || "show"}
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
