import { renderToStaticMarkup } from "react-dom/server"
import { expect, it, vi } from "vitest"

vi.mock("react-admin", async (importOriginal) => {
  const actual = await importOriginal<typeof import("react-admin")>()
  return {
    ...actual,
    useTranslate: () => (key: string, options?: { _?: string }) => options?._ ?? key,
  }
})

import { MuffinAdminContext } from "./context"
import { MuffinDashboard } from "./MuffinDashboard"

it("renders no card without dashboard data", () => {
  const html = renderToStaticMarkup(
    <MuffinAdminContext.Provider value={{ dashboard: undefined, help: undefined } as any}>
      <MuffinDashboard />
    </MuffinAdminContext.Provider>
  )

  expect(html).not.toContain("undefined")
  expect(html).not.toContain("MuiCard")
})
