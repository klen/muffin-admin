import { ReferenceField, TextField } from "react-admin"

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
      <>
        <TextField source={refSource} />
        {refSource !== refKey && (
          <>
            {" (#"}
            <TextField source={refKey} />
            {")"}
          </>
        )}
      </>
    </ReferenceField>
  )
}

FKField.displayName = "FKField"
