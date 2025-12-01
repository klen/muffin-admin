import { startCase } from "lodash"
import { ImageField, ImageInput, RecordContext, useInput, useRecordContext } from "react-admin"

export function ImgInput({ source, label, ...props }) {
  const { field } = useInput({ source })
  label = label || field.name

  return (
    <ImageInput source={source} label={startCase(label || field.name)} {...props}>
      <PreviewImage />
    </ImageInput>
  )
}

function PreviewImage() {
  const value = useRecordContext()
  const source = value?.src || value

  return (
    <RecordContext.Provider value={{ source }}>
      <ImageField source="source" title="source" />
    </RecordContext.Provider>
  )
}
