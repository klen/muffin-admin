import { createContext } from "react"
import type { AdminOpts } from "./types"

export const MuffinAdminContext = createContext<AdminOpts>(null)
