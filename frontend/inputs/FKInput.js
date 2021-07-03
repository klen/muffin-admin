import React from "react";

import { ReferenceInput, AutocompleteInput } from 'react-admin'


const FKInput = ({refProp, refSource, ...props}) => {

  let filterToQuery = search => {
    let filters = {};
    filters[refProp] = search;
    return filters;
  }

  refSource = refSource || 'id';

  let renderText = record => {
      let pk = record[refSource];
      return pk && `${record[refProp]} (#${pk})` || "";
  }

  return (
    <ReferenceInput { ...props } filterToQuery={ filterToQuery }>
      <AutocompleteInput source={ refSource } optionText={ renderText } />
    </ReferenceInput>
  )


}

export default FKInput;
