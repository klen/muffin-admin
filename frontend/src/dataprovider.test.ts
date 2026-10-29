import { afterEach, describe, expect, it, vi } from "vitest"
import { MuffinDataprovider } from "./dataprovider"

const jsonResponse = (body: any, headers: Record<string, string> = {}) =>
  new Response(JSON.stringify(body), {
    headers: { "content-type": "application/json", ...headers },
    status: 200,
  })

afterEach(() => {
  vi.unstubAllGlobals()
})

describe("MuffinDataprovider", () => {
  it("encodes resource ids in the URL", async () => {
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse({ id: "a/b" }))
    vi.stubGlobal("fetch", fetchMock)

    const dataProvider = MuffinDataprovider("/admin/api")
    await dataProvider.getOne("user", { id: "a/b" })

    expect(fetchMock.mock.calls[0][0]).toBe("/admin/api/user/a%2Fb")
  })

  it("uses the resource meta key as the react-admin id", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(jsonResponse([{ key: "web::42" }], { "x-total": "1" }))
    vi.stubGlobal("fetch", fetchMock)

    const dataProvider = MuffinDataprovider("/admin/api")
    const result = await dataProvider.getList("order", {
      meta: { key: "key" },
      pagination: { page: 1, perPage: 25 },
    })

    expect(result.data).toEqual([{ id: "web::42", key: "web::42" }])
    expect(result.total).toBe(1)
  })
})
