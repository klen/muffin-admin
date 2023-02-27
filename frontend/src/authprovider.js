import Cookies from "js-cookie"

import { makeRequest, processAdmin, requestHeaders, setupAdmin } from "./utils"

setupAdmin(
  "auth-get",
  ({ storage }) =>
    (name) =>
      storage == "localstorage" ? localStorage.getItem(name) : Cookies.get(name)
)

setupAdmin("auth-set", ({ storage }) => (name, value) => {
  if (storage == "localstorage") {
    localStorage.setItem(name, value)
    requestHeaders["Authorization"] = value
  } else Cookies.set(name, value)
})

export default (props) => {
  const { identityURL, authorizeURL, logoutURL, required, storage_name } = props

  const authGet = processAdmin("auth-get", props)
  const authSet = processAdmin("auth-set", props)

  // Initialize request headers
  authSet(storage_name, authGet(storage_name))

  let getIdentity = async () => {
    if (identityURL) {
      let { json } = await makeRequest(identityURL)
      return json
    }
  }

  if (required)
    return {
      login: async (data) => {
        if (!authorizeURL) throw { message: "Authorization is not supported" }

        let { json } = await makeRequest(authorizeURL, { data, method: "POST" })
        authSet(storage_name, json)
      },

      checkError: async (error) => {
        const { status } = error

        if (status == 401 || status == 403) {
          // Clean storage
          authSet(storage_name, "")

          throw {
            message: "Invalid authorization",
            redirectTo: logoutURL,
            logoutUser: !logoutURL,
          }
        }
      },

      checkAuth: async () => {
        const auth = authGet(storage_name)
        if (!auth) throw { message: "Authorization required" }

        if (!identityURL) return auth

        let user = await getIdentity()
        if (!user) throw { message: "Authorization required" }

        return user
      },

      logout: async () => {
        // Clean storage
        authSet(storage_name, "")

        if (logoutURL) window.location = logoutURL
      },

      getIdentity,

      getPermissions: () => {
        const role = authGet(storage_name + "_role")
        return role ? Promise.resolve(role) : Promise.reject()
      },
    }
}
