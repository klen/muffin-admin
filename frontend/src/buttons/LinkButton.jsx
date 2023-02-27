import React from "react"
import { Button } from "react-admin"
import { Link } from "react-router-dom"
import * as icons from "@mui/icons-material"

const LinkButton = ({ label, icon, title, resource, filters }) => {
  const Icon = icons[icon] || icon
  let linkParams = {
    pathname: `/${resource}`,
    search: filters ? `filter=${JSON.stringify(filters)}` : undefined,
  }

  return (
    <Button label={label} title={title} component={Link} to={linkParams}>
      {Icon && <Icon />}
    </Button>
  )
}

export default LinkButton
