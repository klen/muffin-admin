import { BooleanField, ChipField, DateField, EmailField, ImageField, FileField, NumberField, RichTextField, TextField, UrlField, SelectField, ArrayField, ReferenceField, ReferenceManyField, ReferenceArrayField } from "react-admin";
import { BooleanInput, NullableBooleanInput, DateInput, DateTimeInput, ImageInput, FileInput, NumberInput, PasswordInput, TextInput, AutocompleteInput, RadioButtonGroupInput, SelectInput, ArrayInput, AutocompleteArrayInput, CheckboxGroupInput, ReferenceArrayInput, ReferenceInput } from "react-admin";
import { JsonField, JsonInput } from "react-admin-json-view";

import AvatarField from "./fields/AvatarField"
import FKField from "./fields/FKField"
import FKInput from "./inputs/FKInput"


// Fix JsonField
JsonField.displayName = 'JsonField';
JsonField.defaultProps = {
    addLabel: true,
};


export default {

  // Fields
  BooleanField, ChipField, DateField, EmailField, ImageField, FileField,
  NumberField, RichTextField, TextField, UrlField, SelectField, ArrayField,
  ReferenceField, ReferenceManyField, ReferenceArrayField, AvatarField,
  JsonField, FKField,

  // Inputs
  BooleanInput, NullableBooleanInput, DateInput, DateTimeInput, ImageInput,
  FileInput, NumberInput, PasswordInput, TextInput, AutocompleteInput,
  RadioButtonGroupInput, SelectInput, ArrayInput, AutocompleteArrayInput,
  CheckboxGroupInput, ReferenceArrayInput, ReferenceInput, JsonInput, FKInput,

}
