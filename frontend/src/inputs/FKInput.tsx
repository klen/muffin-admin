import { AutocompleteInput, ReferenceInput } from "react-admin"

export function FKInput({ refKey, refSource, fullWidth, reference, source, ...props }) {
  // Bind to AutoCompleteInput if we want to customize the search
  // const filterToQuery = (search) => {
  //   const filters = {}
  //   filters[refKey] = search
  //   return filters
  // }

  refKey = refKey || "id"
  const renderText = (record) => {
    const pk = record[refKey]
    if (refKey == refSource) return `#${pk}`
    return (pk && `${record[refSource]} (#${pk})`) || ""
  }

  return (
    <ReferenceInput reference={reference} source={source}>
      <AutocompleteInput source={refKey} optionText={renderText} fullWidth={fullWidth} {...props} />
    </ReferenceInput>
  )
}
