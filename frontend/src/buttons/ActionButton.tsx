import { Button, useListContext, useRecordContext, useResourceContext } from "react-admin"

import { useState } from "react"
import { useAction } from "../hooks/useAction"
import { AdminAction } from "../types"
import { buildIcon, findBuilder } from "../utils"

export function ActionButton({ icon, label, title, action, id }: AdminAction) {
  const [payloadActive, setPayloadActive] = useState(false)
  const record = useRecordContext()
  const resource = useResourceContext()
  const { mutate, isPending } = useAction(action, {})

  const PayloadBuilder = findBuilder(["action", "payload", id, resource])

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={() => (PayloadBuilder ? setPayloadActive(true) : mutate({ record }))}
        disabled={isPending}
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
  const { mutate, isPending } = useAction(action)
  const resource = useResourceContext()
  const [payloadActive, setPayloadActive] = useState(false)

  const PayloadBuilder = findBuilder(["action", "payload", id, resource])

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={() => (PayloadBuilder ? setPayloadActive(true) : mutate({ ids: selectedIds }))}
        disabled={isPending}
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
