import { createRoot } from "react-dom/client"
import { buildAdmin } from "./utils"

export async function initAdmin(prefix = "") {
  const response = await fetch(`${prefix}/ra.json`)
  const props = await response.json()
  const container = document.getElementById("root")
  if (!container) throw new Error("No root element found")
  const root = createRoot(container)
  root.render(buildAdmin(["admin"], props))
}

// @ts-ignore
globalThis.initAdmin = initAdmin

export * from "./MuffinAdmin"
export * from "./MuffinLayout"
export * from "./MuffinResource"
export * from "./MuffinResourceCreate"
export * from "./MuffinResourceEdit"
export * from "./MuffinResourceList"
export * from "./MuffinResourceShow"
export * from "./authprovider"
export * from "./buildRA"
export * from "./buttons"
export * from "./dataprovider"
export * from "./types"
export * from "./fields"
export * from "./utils"
