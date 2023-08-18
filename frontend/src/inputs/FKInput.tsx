import { AutocompleteInput, ReferenceInput } from "react-admin"

export function FKInput({ refProp, refSource, fullWidth, reference, source, ...props }) {
  const filterToQuery = (search) => {
    const filters = {}
    filters[refProp] = search
    return filters
  }

  refSource = refSource || "id"

  const renderText = (record) => {
    const pk = record[refSource]
    return (pk && `${record[refProp]} (#${pk})`) || ""
  }

  return (
    <ReferenceInput reference={reference} source={source} filterToQuery={filterToQuery} {...props}>
      <AutocompleteInput
        source={refSource}
        optionText={renderText}
        fullWidth={fullWidth}
        {...props}
      />
    </ReferenceInput>
  )
}
