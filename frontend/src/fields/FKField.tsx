import { ReferenceField, TextField } from "react-admin"

export function FKField({ refSource, refID, link, reference, source, ...props }) {
  return (
    <ReferenceField link={link || "show"} reference={reference} source={source} {...props}>
      <>
        <TextField source={refSource} />
        {" (#"}
        <TextField source={refID || "id"} />
        {")"}
      </>
    </ReferenceField>
  )
}

FKField.displayName = "FKField"
FKField.defaultProps = {
  addLabel: true,
}