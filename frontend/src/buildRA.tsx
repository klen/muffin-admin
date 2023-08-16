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

import { AvatarField, EditableBooleanField, FKField, JsonField } from "./fields"
import { JsonInput, FKInput } from "./inputs"

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
