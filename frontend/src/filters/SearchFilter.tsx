import SearchIcon from "@mui/icons-material/Search"
import { InputAdornment } from "@mui/material"
import clsx from "clsx"
import debounce from "lodash/debounce"
import { useTranslate } from "ra-core"
import { useState } from "react"
import { ResettableTextField, SearchInputProps, useInput, useResourceContext } from "react-admin"

export function SearchFilter({ source, className, ...props }: SearchInputProps) {
  const translate = useTranslate()
  const { field } = useInput({ source, ...props })
  const [searchValue, setSearchValue] = useState(field.value || "")
  const resource = useResourceContext()

  const onBlur = () => field.onChange(searchValue)
  const label = translate(`resources.${resource}.fields.${source}`)

  return (
    <ResettableTextField
      resettable
      ref={field.ref}
      value={searchValue}
      onBlur={debounce(onBlur, 500)}
      onChange={(e) => setSearchValue(e.target?.value || e)}
      onKeyUp={(e) => {
        if (e.key === "Enter") field.onChange(searchValue)
      }}
      placeholder={label}
      {...props}
      className={clsx("ra-input", `ra-input-${source}`, className)}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <SearchIcon color="disabled" />
          </InputAdornment>
        ),
      }}
    />
  )
}
