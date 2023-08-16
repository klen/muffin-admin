import React from "react"
import { Layout } from "react-admin"
import { setupAdmin } from "./utils"

export function MuffinLayout(props) {
  return <Layout {...props} />
}

setupAdmin(["layout"], MuffinLayout)
