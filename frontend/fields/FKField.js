import React from "react";

import { ReferenceField, TextField } from 'react-admin'

const FKField = ({refSource, refID, ...props}) => {
  return (
    <ReferenceField { ...props }>
      <>
        { "#" }
        <TextField source={ refID || 'id' } />
        { " " }
        <TextField source={ refSource } />
      </>
    </ReferenceField>
  )
}

FKField.displayName = 'FKField';
FKField.defaultProps = {
    addLabel: true,
};

export default FKField;

