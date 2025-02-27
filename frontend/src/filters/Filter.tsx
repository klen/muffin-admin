import Button from "@mui/material/Button"
import FormGroup from "@mui/material/FormGroup"
import Menu from "@mui/material/Menu"
import MenuItem from "@mui/material/MenuItem"
import TextField from "@mui/material/TextField"
import { useState } from "react"
import { FieldTitle, InputProps, useInput } from "react-admin"

const OPERATORS = {
  $eq: "=",
  $ne: "≠",
  $gt: ">",
  $ge: "≥",
  $lt: "<",
  $le: "≤",
}

export function Filter({ type = "text", ...props }: InputProps) {
  const { field } = useInput({
    format: (value: any) => (value ? value[Object.keys(value)[0]] : ""),
    ...props,
  })
  const [op, setOp] = useState((field.value && Object.keys(field.value)[0]) || "$eq")

  const onChange = function(e: any) {
    field.onChange({ [op]: e.target.value })
  }

  const [menuEl, setMenuEl] = useState(null)
  const open = Boolean(menuEl)
  const { label, source, resource, isRequired } = props

  return (
    <>
      <FormGroup row sx={{ flexWrap: "nowrap" }}>
        <Button
          size="small"
          disableElevation
          sx={{ minWidth: 30 }}
          onClick={(e) => setMenuEl(e.currentTarget)}
        >
          <span style={{ fontSize: "1.5em" }}>{OPERATORS[op]}</span>
        </Button>
        <TextField
          {...field}
          onChange={onChange}
          value={field.value}
          variant="outlined"
          type={type}
          label={
            <FieldTitle label={label} source={source} resource={resource} isRequired={isRequired} />
          }
        />
      </FormGroup>
      <Menu open={open} onClose={() => setMenuEl(null)} anchorEl={menuEl}>
        {Object.entries(OPERATORS).map(([key, value]) => (
          <MenuItem
            key={key}
            selected={op === value}
            onClick={() => {
              setOp(key)
              setMenuEl(null)
              field.onChange({ [key]: field.value })
            }}
          >
            {value}
          </MenuItem>
        ))}
      </Menu>
    </>
  )
}
