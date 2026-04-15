import { Button } from "react-admin"
import { Link, useLocation } from "react-router-dom"
import { AdminShowLink } from "../types"
import { buildIcon } from "../utils"

const LinkButton = ({
  filters,
  icon,
  label,
  resource,
  id,
  title,
}: AdminShowLink & { resource: string; filters?: any; id?: string }) => {
  const location = useLocation()
  const searchParams = new URLSearchParams()
  searchParams.set("returnTo", `${location.pathname}${location.search}`)

  if (filters) {
    searchParams.set("filter", JSON.stringify(filters))
  }

  const linkParams = {
    pathname: `/${resource}`,
    search: `?${searchParams.toString()}`,
  }

  if (id) linkParams.pathname += `/${id}/show`

  return (
    <Button
      label={label}
      title={title}
      component={Link}
      to={linkParams}
      onClick={(e) => e.stopPropagation()}
    >
      {buildIcon(icon)}
    </Button>
  )
}

export default LinkButton
