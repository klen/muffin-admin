import { AutocompleteInput, ReferenceInput } from "react-admin"

export function FKInput({ refKey, refSource, fullWidth, reference, source, ...props }) {
  refKey = refKey || "id"
  const renderText = (record) => {
    const pk = record[refKey]
    if (refKey == refSource) return `#${pk}`
    return (pk && `${record[refSource]} (#${pk})`) || ""
  }

  return (
    <ReferenceInput reference={reference} source={source} {...props}>
      <AutocompleteInput source={refKey} optionText={renderText} fullWidth={fullWidth} {...props} />
    </ReferenceInput>
  )
}
