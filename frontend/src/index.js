import { createRoot } from "react-dom/client"

import "./admin"
import { processAdmin } from "./utils"

export * from "./utils"

export async function initAdmin(prefix = "") {
  const response = await fetch(`${prefix}/ra.json`)
  const props = await response.json()
  const container = document.getElementById("root")
  const root = createRoot(container)
  root.render(processAdmin("admin", props))
}
