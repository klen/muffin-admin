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
  const [payloadActive, setPayloadActive] = useState(false)

  const PayloadBuilder = findBuilder(["action", "payload", action])

  const refresh = useRefresh(),
    unselectAll = useUnselectAll(resource),
    notify = useNotify()

  const { mutate, isLoading } = useAction(action)

  const process = (payload?) =>
    mutate(
      { ids: selectedIds, payload },
      {
        onSuccess: ({ data }) => {
          if (data && data.message) notify(data.message, { type: "success" })
          if (data && data.redirectTo) window.location = data.redirectTo
          else {
            unselectAll()
            refresh()
          }
        },
        onError: (err) => {
          notify(typeof err === "string" ? err : err.message, { type: "error" })
        },
      }
    )

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={() => (PayloadBuilder ? setPayloadActive(true) : process())}
        disabled={isLoading}
      >
        {buildIcon(icon)}
      </Button>
      {PayloadBuilder && (
        <PayloadBuilder
          active={payloadActive}
          onHandle={(payload) => process(payload)}
          onClose={() => setPayloadActive(false)}
        />
      )}
    </>
  )
}

export function ActionButton({ icon, label, title, action }) {
  const [payloadActive, setPayloadActive] = useState(false)

  const record = useRecordContext()
  const { mutate, isLoading } = useAction(action)

  const PayloadBuilder = findBuilder(["action", "payload", action])

  const refresh = useRefresh(),
    notify = useNotify()

  const process = (payload?) =>
    mutate(
      { record, payload },
      {
        onSuccess: ({ data }) => {
          if (data && data.message) notify(data.message, { type: "success" })
          if (data && data.redirectTo) window.location = data.redirectTo
          else refresh()
        },
        onError: (err) => {
          notify(typeof err === "string" ? err : err.message, { type: "error" })
        },
      }
    )

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={() => (PayloadBuilder ? setPayloadActive(true) : process())}
        disabled={isLoading}
      >
        {buildIcon(icon)}
      </Button>
      {PayloadBuilder && (
        <PayloadBuilder
          active={payloadActive}
          onHandle={(payload) => process(payload)}
          onClose={() => setPayloadActive(false)}
        />
      )}
    </>
  )
}
