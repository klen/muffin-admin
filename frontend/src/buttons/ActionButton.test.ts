import { describe, expect, it } from "vitest"
import { buildFileUrl } from "./ActionButton"

describe("buildFileUrl", () => {
  it("encodes ids and filters without adding the token", () => {
    const url = buildFileUrl("/admin/api", "/message/{id}/data.csv", "a/b", { name: "A & B" })

    expect(url).toBe(
      `/admin/api/message/a%2Fb/data.csv?f&where=${encodeURIComponent('{"name":"A & B"}')}`
    )
    expect(url).not.toContain("t=")
  })

  it("works for list downloads without filters", () => {
    expect(buildFileUrl("/admin/api", "/user/export")).toBe("/admin/api/user/export?f")
  })
})
