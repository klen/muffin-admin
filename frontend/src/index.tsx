import { createRoot } from "react-dom/client"
import { MuffinAdminContext } from "./context"
import { MuffinAdmin } from "./MuffinAdmin"

export * from "./actions"
export * from "./authprovider"
export * from "./buildRA"
export * from "./buttons"
export * from "./common"
export * from "./context"
export * from "./dataprovider"
export * from "./fields"
export * from "./hooks"
export * from "./MuffinAdmin"
export * from "./MuffinDashboard"
export * from "./MuffinMenu"
export * from "./MuffinRecordList"
export * from "./MuffinResource"
export * from "./MuffinResourceCreate"
export * from "./MuffinResourceEdit"
export * from "./MuffinResourceList"
export * from "./MuffinResourceShow"
export * from "./types"
export * from "./utils"

export async function initAdmin(prefix = "", containerId: string = "root") {
  const response = await fetch(`${prefix}/ra.json`)
  const adminOpts = await response.json()
  const container = document.getElementById(containerId)
  if (!container) throw new Error(`Container #${containerId} not found`)
  const root = createRoot(container)
  root.render(
    <MuffinAdminContext.Provider value={adminOpts}>
      <MuffinAdmin />
    </MuffinAdminContext.Provider>
  )
}

export { VERSION } from "./version"
