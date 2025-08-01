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
    const key = record[refKey]
    if (refKey == refSource) return `#${key}`
    return (key && `${record[refSource]} (#${key})`) || ""
  }

  return (
    <ReferenceInput
      reference={reference}
      source={source}
      queryOptions={{
        meta: { key: refKey },
      }}
    >
      <AutocompleteInput
        source={refKey}
        optionText={renderText}
        fullWidth={fullWidth}
        sx={{ minWidth: 300 }}
        {...props}
      />
    </ReferenceInput>
  )
}
