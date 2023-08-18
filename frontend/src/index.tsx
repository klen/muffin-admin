import { createRoot } from "react-dom/client"
import { buildAdmin } from "./utils"

export * from "./MuffinAdmin"
export * from "./MuffinDashboard"
export * from "./MuffinResource"
export * from "./MuffinResourceCreate"
export * from "./MuffinResourceEdit"
export * from "./MuffinResourceList"
export * from "./MuffinResourceShow"
export * from "./authprovider"
export * from "./buildRA"
export * from "./buttons"
export * from "./dataprovider"
export * from "./fields"
export * from "./types"
export * from "./utils"

export async function initAdmin(prefix = "", containerId: string = "root") {
  const response = await fetch(`${prefix}/ra.json`)
  const props = await response.json()
  const container = document.getElementById(containerId)
  if (!container) throw new Error(`Container #${containerId} not found`)
  const root = createRoot(container)
  root.render(buildAdmin(["admin"], props))
}
