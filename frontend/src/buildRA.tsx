import {
  ArrayField,
  ArrayInput,
  AutocompleteArrayInput,
  AutocompleteInput,
  BooleanField,
  BooleanInput,
  CheckboxGroupInput,
  ChipField,
  DateField,
  DateInput,
  DateTimeInput,
  EmailField,
  FileField,
  FileInput,
  ImageField,
  ImageInput,
  NullableBooleanInput,
  NumberField,
  NumberInput,
  PasswordInput,
  RadioButtonGroupInput,
  ReferenceArrayField,
  ReferenceArrayInput,
  ReferenceField,
  ReferenceInput,
  ReferenceManyField,
  RichTextField,
  SelectField,
  SelectInput,
  TextField,
  TextInput,
  UrlField,
  required,
} from "react-admin"

import { AvatarField, EditableBooleanField, FKField, JsonField } from "./fields"
import { FKInput, JsonInput } from "./inputs"

export const UI: Record<string, JSX.ElementType> = {
  // Fields
  BooleanField,
  ChipField,
  DateField,
  EmailField,
  ImageField,
  FileField,
  NumberField,
  RichTextField,
  TextField,
  UrlField,
  SelectField,
  ArrayField,
  ReferenceField,
  ReferenceManyField,
  ReferenceArrayField,
  AvatarField,
  EditableBooleanField,
  FKField,
  JsonField,

  // Inputs
  BooleanInput,
  NullableBooleanInput,
  DateInput,
  DateTimeInput,
  ImageInput,
  FileInput,
  NumberInput,
  PasswordInput,
  TextInput,
  AutocompleteInput,
  RadioButtonGroupInput,
  SelectInput,
  ArrayInput,
  AutocompleteArrayInput,
  CheckboxGroupInput,
  ReferenceArrayInput,
  ReferenceInput,
  JsonInput,
  FKInput,
}

export function buildRAComponent(name, props) {
  const Item = UI[name]
  if (!Item) return null

  if (props.required) {
    props.validate = required()
    delete props.required
  }

  props.fullWidth = props.fullWidth ?? true

  if (props.children) props.children = buildRA(props.children)[0]

  return <Item key={props.source} {...props} />
}

export function buildRA(items) {
  return items.map((item) => buildRAComponent(item[0], item[1]))
}
