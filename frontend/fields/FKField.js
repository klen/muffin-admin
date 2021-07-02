import React from "react";

import { ReferenceField, TextField } from 'react-admin'

const FKField = ({refSource, ...props}) => (
  <ReferenceField { ...props }>
    <TextField source={ refSource } />
  </ReferenceField>
)

export default FKField;

