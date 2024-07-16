import { Button } from "react-admin"
import { Link } from "react-router-dom"
import { AdminShowLink } from "../types"
import { buildIcon } from "../utils"

const LinkButton = ({
  filters,
  icon,
  label,
  resource,
  id,
  title,
}: AdminShowLink & { resource: string; filters: any; id?: string }) => {
  const linkParams = {
    pathname: `/${resource}`,
    search: filters ? `filter=${JSON.stringify(filters)}` : undefined,
  }

  if (id) linkParams.pathname += `/${id}/show`

  return (
    <Button label={label} title={title} component={Link} to={linkParams}>
      {buildIcon(icon)}
    </Button>
  )
}

export default LinkButton
