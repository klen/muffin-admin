import { createContext } from "react"
import { AdminOpts } from "./types"

export const MuffinAdminContext = createContext<AdminOpts>(null)
