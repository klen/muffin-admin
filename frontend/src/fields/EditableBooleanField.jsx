import React from "react"
import { useRecordContext } from "ra-core"
import { BooleanInput } from "ra-ui-materialui"

const EditableBooleanField = ({ source, alt, style, nameProp, ...props }) => {
  const record = useRecordContext(props)

  return <BooleanInput source={source} />
}

export default EditableBooleanField
