import {
  Button,
  useListContext,
  useRecordContext,
  useResourceContext,
  useTranslate,
} from "react-admin"

import { useState } from "react"
import { useConfirmation } from "../common"
import { useAction } from "../hooks/useAction"
import { AdminAction } from "../types"
import { buildIcon, findBuilder } from "../utils"

export type ActionPayloadProps = {
  active: boolean
  onClose: () => void
  onHandle: (payload: any) => void
}

export function ActionButton({ icon, label, title, action, id, confirm }: AdminAction) {
  const translate = useTranslate()
  const record = useRecordContext()
  const resource = useResourceContext()
  const confirmation = useConfirmation()
  const { mutate, isPending } = useAction(action, {})

  const [payloadActive, setPayloadActive] = useState(false)
  const [payloadResolver, setPayloadResolver] = useState<(data: any) => void>()

  const PayloadBuilder = findBuilder(["action", "payload", id, resource])
  const buildPayload = PayloadBuilder
    ? new Promise((resolve) => setPayloadResolver(() => resolve))
    : Promise.resolve()
  const confirmMessage =
    typeof confirm === "string" ? translate(confirm) : "Do you confirm this action?"

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={async () => {
          if (PayloadBuilder) setPayloadActive(true)
          const payload = await buildPayload
          const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
          if (process) await mutate({ record, payload })
        }}
        disabled={isPending}
      >
        {buildIcon(icon)}
      </Button>
      {PayloadBuilder && (
        <PayloadBuilder
          active={payloadActive}
          onHandle={payloadResolver}
          onClose={() => setPayloadActive(false)}
        />
      )}
    </>
  )
}

export function BulkActionButton({ label, icon, title, action, id, confirm }: AdminAction) {
  const translate = useTranslate()
  const { selectedIds } = useListContext()
  const { mutate, isPending } = useAction(action)
  const confirmation = useConfirmation()
  const resource = useResourceContext()
  const [payloadActive, setPayloadActive] = useState(false)
  const [payloadResolver, setPayloadResolver] = useState<(data: any) => void>()

  const PayloadBuilder = findBuilder(["action", "payload", id, resource])
  const buildPayload = PayloadBuilder
    ? new Promise((resolve) => setPayloadResolver(() => resolve))
    : Promise.resolve()
  const confirmMessage =
    typeof confirm === "string" ? translate(confirm) : "Do you confirm this action?"

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={async () => {
          if (PayloadBuilder) setPayloadActive(true)
          const payload = await buildPayload
          const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
          if (process) await mutate({ ids: selectedIds, payload })
        }}
        disabled={isPending}
      >
        {buildIcon(icon)}
      </Button>
      {PayloadBuilder && (
        <PayloadBuilder
          active={payloadActive}
          onHandle={payloadResolver}
          onClose={() => setPayloadActive(false)}
        />
      )}
    </>
  )
}
