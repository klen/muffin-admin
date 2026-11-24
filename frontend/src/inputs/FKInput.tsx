import { AutocompleteInput, ReferenceInput } from "react-admin"
import { useMuffinResourceOpts } from "../hooks"

export function FKInput({ refKey, refSource, fullWidth, reference, source, ...props }) {
  // List the options with the related resource's default sorting instead of react-admin's `-id`
  const { list } = useMuffinResourceOpts(reference) || {}
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
      sort={list?.sort}
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
