import { Button, useListContext, useRecordContext } from "react-admin"

import { useState } from "react"
import { useAction } from "../hooks/useAction"
import { AdminAction } from "../types"
import { buildIcon, findBuilder } from "../utils"

export function ActionButton({ icon, label, title, action, id }: AdminAction) {
  const [payloadActive, setPayloadActive] = useState(false)
  const record = useRecordContext()
  const { mutate, isLoading } = useAction(action, {})

  const PayloadBuilder = findBuilder(["action", "payload", id])

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={() => (PayloadBuilder ? setPayloadActive(true) : mutate({ record }))}
        disabled={isLoading}
      >
        {buildIcon(icon)}
      </Button>
      {PayloadBuilder && (
        <PayloadBuilder
          active={payloadActive}
          onHandle={(payload) => mutate({ record, payload })}
          onClose={() => setPayloadActive(false)}
        />
      )}
    </>
  )
}

export function BulkActionButton({ label, icon, title, action, id }: AdminAction) {
  const { selectedIds } = useListContext()
  const { mutate, isLoading } = useAction(action)
  const [payloadActive, setPayloadActive] = useState(false)

  const PayloadBuilder = findBuilder(["action", "payload", id])

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={() => (PayloadBuilder ? setPayloadActive(true) : mutate({ ids: selectedIds }))}
        disabled={isLoading}
      >
        {buildIcon(icon)}
      </Button>
      {PayloadBuilder && (
        <PayloadBuilder
          active={payloadActive}
          onHandle={(payload) => mutate({ ids: selectedIds, payload })}
          onClose={() => setPayloadActive(false)}
        />
      )}
    </>
  )
}
