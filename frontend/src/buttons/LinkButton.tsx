import React from "react"
import { Button } from "react-admin"
import { Link } from "react-router-dom"
import { buildIcon } from "../utils"

const LinkButton = ({ label, icon, title, resource, filters }) => {
  const linkParams = {
    pathname: `/${resource}`,
    search: filters ? `filter=${JSON.stringify(filters)}` : undefined,
  }

  return (
    <Button label={label} title={title} component={Link} to={linkParams}>
      {buildIcon(icon)}
    </Button>
  )
}

export default LinkButton
