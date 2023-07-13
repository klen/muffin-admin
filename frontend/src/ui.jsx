import React from "react"

import { required } from "react-admin"
import {
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
} from "react-admin"
import {
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
} from "react-admin"

import AvatarField from "./fields/AvatarField"
import FKField from "./fields/FKField"
import FKInput from "./inputs/FKInput"
import JsonField from "./fields/JsonField"
import JsonInput from "./inputs/JsonInput"

const UI = {
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
  JsonField,
  FKField,

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

  if (props.required) {
    props.validate = required()
    delete props.required
  }

  props.fullWidth = props.fullWidth ?? true

  if (props.children) props.children = initRAItems(props.children)[0]

  return <Item key={props.source} {...props} />
}

export default function initRAItems(items) {
  return items.map((item) => buildRAComponent(...item))
}
