import { useResourceContext } from "react-admin"
import { useMuffinAdminOpts } from "./useMuffinAdminOpts"

export function useMuffinResourceOpts() {
  const resource = useResourceContext()
  const { resources } = useMuffinAdminOpts()
  return resources.find((r) => r.name === resource)
}
