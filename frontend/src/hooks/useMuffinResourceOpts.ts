import { useResourceContext } from "react-admin"
import { useMuffinAdminOpts } from "./useMuffinAdminOpts"

export function useMuffinResourceOpts(resource?) {
  resource = useResourceContext({ resource })
  const { resources } = useMuffinAdminOpts()
  return resources.find((r) => r.name === resource)
}
