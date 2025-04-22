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
  required,
  RichTextField,
  SearchInput,
  SelectArrayInput,
  SelectField,
  SelectInput,
  TextField,
  TextInput,
  UrlField,
} from "react-admin"

import { AvatarField, CopyField, EditableBooleanField, FKField, JsonField } from "./fields"
import { DateRangeFilter, Filter, SearchFilter } from "./filters"
import { FKInput, JsonInput, TimestampInput } from "./inputs"

const UI: Record<string, JSX.ElementType> = {
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
  CopyField,

  // Inputs
  ArrayInput,
  AutocompleteArrayInput,
  AutocompleteInput,
  BooleanInput,
  CheckboxGroupInput,
  DateInput,
  DateTimeInput,
  FKInput,
  FileInput,
  ImageInput,
  JsonInput,
  NullableBooleanInput,
  NumberInput,
  PasswordInput,
  RadioButtonGroupInput,
  ReferenceArrayInput,
  ReferenceInput,
  SelectArrayInput,
  SelectInput,
  TextInput,
  TimestampInput,
  SearchInput,

  // Filters
  Filter,
  DateRangeFilter,
  SearchFilter,
}

export function buildRAComponent(name: string, props: any) {
  const Item = UI[name]
  if (!Item) return null

  if (props.required) {
    props.validate = required()
    delete props.required
  }

  if (props.children) props.children = buildRA(props.children)[0]

  return <Item key={props.source} {...props} />
}

export function buildRA(items: [string, Record<string, any>][]) {
  return items.map((item) => buildRAComponent(item[0], item[1]))
}

export function registerUI(name: string, component: JSX.ElementType) {
  UI[name] = component
}
