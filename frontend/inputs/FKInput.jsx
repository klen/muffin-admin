import React from 'react'

import { ReferenceInput, AutocompleteInput } from 'react-admin'

const FKInput = ({
  refProp,
  refSource,
  fullWidth,
  reference,
  source,
  ...props
}) => {
  let filterToQuery = (search) => {
    let filters = {}
    filters[refProp] = search
    return filters
  }

  refSource = refSource || 'id'

  let renderText = (record) => {
    let pk = record[refSource]
    return (pk && `${record[refProp]} (#${pk})`) || ''
  }

  return (
    <ReferenceInput
      reference={reference}
      source={source}
      filterToQuery={filterToQuery}
      {...props}
    >
      <AutocompleteInput
        source={refSource}
        optionText={renderText}
        fullWidth={fullWidth}
      />
    </ReferenceInput>
  )
}

export default FKInput
