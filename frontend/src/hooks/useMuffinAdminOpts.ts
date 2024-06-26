import { useContext } from "react"
import { MuffinAdminContext } from "../context"

export function useMuffinAdminOpts() {
  return useContext(MuffinAdminContext)
}
