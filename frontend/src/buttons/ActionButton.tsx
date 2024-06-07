import * as icons from "@mui/icons-material"
import {
  Button,
  useListContext,
  useNotify,
  useRecordContext,
  useRefresh,
  useResourceContext,
  useUnselectAll,
} from "react-admin"

import { useState } from "react"
import { useAction } from "../hooks/useAction"
import { buildIcon, findBuilder } from "../utils"

export function BulkActionButton({ label, icon, title, action }) {
  const resource = useResourceContext()
  const { selectedIds } = useListContext()
  const refresh = useRefresh(),
    unselectAll = useUnselectAll(resource),
    notify = useNotify()

  const { mutate, isLoading } = useAction(action)

  const onClick = () => {
    mutate(
      {
        action,
        ids: selectedIds,
      },
      {
        onSuccess: ({ data }) => {
          if (data && data.message) notify(data.message, { type: "success" })
          refresh()
          unselectAll()
        },
        onError: (err) => {
          notify(typeof err === "string" ? err : err.message, { type: "error" })
        },
      }
    )
  }

  return (
    <Button label={label} title={title} onClick={onClick} disabled={isLoading}>
      {buildIcon(icon)}
    </Button>
  )
}

export function ActionButton(props) {
  const { icon, label, title, action } = props

  const [payload, setPayload] = useState(null)
  const [payloadActive, setPayloadActive] = useState(false)

  const record = useRecordContext()
  const actionData = { record, payload }
  const { mutate, isLoading } = useAction(action)

  const PayloadBuilder = findBuilder(["action", "payload", action])

  const refresh = useRefresh(),
    notify = useNotify(),
    Icon = icons[icon]

  const process = () =>
    mutate(actionData, {
      onSuccess: ({ data }) => {
        if (data && data.message) notify(data.message, { type: "success" })
        if (data && data.redirectTo) window.location = data.redirectTo
        else refresh()
      },
      onError: (err) => {
        notify(typeof err === "string" ? err : err.message, { type: "error" })
      },
    })

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={PayloadBuilder ? () => setPayloadActive(true) : process}
        disabled={isLoading}
      >
        {Icon && <Icon />}
      </Button>
      {PayloadBuilder && (
        <PayloadBuilder
          active={payloadActive}
          onChange={(payload) => {
            setPayloadActive(false)
            setPayload(payload)
            process()
          }}
          onClose={() => setPayloadActive(false)}
        />
      )}
    </>
  )
}
