import { ReferenceField, TextField } from "react-admin"

export function FKField({ reference, refSource, refKey, link, source, ...props }) {
  return (
    <ReferenceField
      link={link || "show"}
      reference={reference}
      source={source}
      queryOptions={{ meta: { key: refKey } }}
      {...props}
    >
      <>
        <TextField source={refSource} />
        {" (#"}
        <TextField source={refKey || "id"} />
        {")"}
      </>
    </ReferenceField>
  )
}

FKField.displayName = "FKField"
