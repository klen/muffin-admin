import Cookies from "js-cookie"
import { findBuilder, makeRequest, requestHeaders, setupAdmin } from "."
import { AdminOpts } from "./types"

setupAdmin(
  ["auth-storage-get"],
  ({ storage, storageName }: AdminOpts["auth"]) =>
    () =>
      storage == "localstorage" ? localStorage.getItem(storageName) : Cookies.get(storageName)
)

setupAdmin(["auth-storage-set"], ({ storage }) => (name, value) => {
  if (storage == "localstorage") {
    localStorage.setItem(name, value)
    requestHeaders["Authorization"] = value
  } else Cookies.set(name, value)
})

export function MuffinAuthProvider(props: AdminOpts["auth"]) {
  const { identityURL, authorizeURL, logoutURL, required, storageName } = props

  const authGet = findBuilder(["auth-storage-get"])(props)
  const authSet = findBuilder(["auth-storage-set"])(props)

  // Initialize request headers
  authSet(storageName, authGet(storageName))

  const getIdentity = async () => {
    if (identityURL) {
      const { json } = await makeRequest(identityURL)
      return json
    }
  }

  if (required)
    return {
      login: async (data) => {
        if (!authorizeURL) throw { message: "Authorization is not supported" }

        const { json } = await makeRequest(authorizeURL, {
          data,
          method: "POST",
        })
        authSet(storageName, json)
      },

      checkError: async (error) => {
        const { status } = error || {}

        if (status == 401 || status == 403) {
          // Clean storage
          authSet(storageName, "")

          throw {
            message: "Invalid authorization",
            redirectTo: logoutURL,
            logoutUser: !logoutURL,
          }
        }
      },

      checkAuth: async () => {
        const auth = authGet(storageName)
        if (!auth) throw { message: "Authorization required" }

        if (!identityURL) return auth

        const user = await getIdentity()
        if (!user) throw { message: "Authorization required" }

        return user
      },

      getAuthorization: () => authGet(storageName),

      logout: async () => {
        // Clean storage
        authSet(storageName, "")

        if (logoutURL) window.location.href = logoutURL
      },

      getIdentity,

      getPermissions: async () => {
        const role = authGet(storageName + "_role")
        return role || ""
      },
    }
}

setupAdmin(["authprovider"], MuffinAuthProvider)
