import React from "react";

import { ReferenceInput, AutocompleteInput } from 'react-admin'


const FKInput = ({refProp, refSource, ...props}) => {

  let filterToQuery = search => {
    let filters = {};
    filters[refProp] = search;
    return filters;
  }

  return (
    <ReferenceInput { ...props } filterToQuery={ filterToQuery }>
      <AutocompleteInput source={ refSource || 'id' } optionText={ refProp } />
    </ReferenceInput>
  )


}

export default FKInput;
