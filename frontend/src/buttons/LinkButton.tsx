import { Button } from "react-admin"
import { Link } from "react-router-dom"
import { AdminShowLink } from "../types"
import { buildIcon } from "../utils"

const LinkButton = ({
  filters,
  icon,
  label,
  resource,
  title,
}: AdminShowLink & { resource: string; filters: any }) => {
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
