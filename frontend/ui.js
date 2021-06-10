import { BooleanField, ChipField, DateField, EmailField, ImageField, FileField, NumberField, RichTextField, TextField, UrlField, SelectField, ArrayField, ReferenceField, ReferenceManyField, ReferenceArrayField } from "react-admin";
import { BooleanInput, NullableBooleanInput, DateInput, DateTimeInput, ImageInput, FileInput, NumberInput, PasswordInput, TextInput, AutocompleteInput, RadioButtonGroupInput, SelectInput, ArrayInput, AutocompleteArrayInput, CheckboxGroupInput, ReferenceArrayInput, ReferenceInput } from "react-admin";
import { JsonField, JsonInput } from "react-admin-json-view";
import AvatarField from "./fields/avatar"


// Fix JsonField
JsonField.displayName = 'JsonField';
JsonField.defaultProps = {
    addLabel: true,
};


export default {
  BooleanField, ChipField, DateField, EmailField, ImageField, FileField, NumberField, RichTextField, TextField, UrlField, SelectField, ArrayField, ReferenceField, ReferenceManyField, ReferenceArrayField,
  BooleanInput, NullableBooleanInput, DateInput, DateTimeInput, ImageInput, FileInput, NumberInput, PasswordInput, TextInput, AutocompleteInput, RadioButtonGroupInput, SelectInput, ArrayInput, AutocompleteArrayInput, CheckboxGroupInput, ReferenceArrayInput, ReferenceInput,
  JsonField, JsonInput, AvatarField,
}
