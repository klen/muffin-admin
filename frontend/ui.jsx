import React from "react";

import { required } from 'react-admin';
import { BooleanField, ChipField, DateField, EmailField, ImageField, FileField, NumberField, RichTextField, TextField, UrlField, SelectField, ArrayField, ReferenceField, ReferenceManyField, ReferenceArrayField } from "react-admin";
import { BooleanInput, NullableBooleanInput, DateInput, DateTimeInput, ImageInput, FileInput, NumberInput, PasswordInput, TextInput, AutocompleteInput, RadioButtonGroupInput, SelectInput, ArrayInput, AutocompleteArrayInput, CheckboxGroupInput, ReferenceArrayInput, ReferenceInput } from "react-admin";
import { JsonField, JsonInput } from "react-admin-json-view";

import AvatarField from "./fields/AvatarField.jsx"
import FKField from "./fields/FKField.jsx"
import FKInput from "./inputs/FKInput.jsx"


// Fix JsonField
JsonField.displayName = 'JsonField';
JsonField.defaultProps = {
    addLabel: true,
};

const ui = {

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

const initRAItems = itemsProps => itemsProps.map((item) => {
    const Item = ui[item[0]],
          props = {...item[1]};

    if (props.required) {
        props.validate = required();
        delete props.required
    }

    props.fullWidth = props.fullWidth ?? true

    if (props.children) props.children = initRAItems(props.children)[0];
  
    return <Item key={ props.source } { ...props } />
})

export default initRAItems
