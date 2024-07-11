import {
  Button,
  Form,
  useListContext,
  useRecordContext,
  useResourceContext,
  useTranslate,
} from "react-admin"

import { useState } from "react"
import { buildRA } from "../buildRA"
import { AdminModal, PayloadButtons, useConfirmation } from "../common"
import { useAction } from "../hooks/useAction"
import { AdminAction } from "../types"
import { buildIcon, findBuilder } from "../utils"

export type ActionPayloadProps = {
  active: boolean
  onClose: () => void
  onHandle: (payload: any) => void
}

export function ActionButton({ action, confirm, ...props }: AdminAction) {
  const translate = useTranslate()
  const record = useRecordContext()
  const confirmation = useConfirmation()
  const { mutate, isPending } = useAction(action)

  const confirmMessage =
    typeof confirm === "string" ? translate(confirm) : "Do you confirm this action?"

  const onHandle = async (payload?) => {
    const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
    if (process) await mutate({ record, payload })
  }

  return <ActionButtonBase {...props} isPending={isPending} onHandle={onHandle} />
}

export function BulkActionButton({ action, confirm, ...props }: AdminAction) {
  const translate = useTranslate()
  const { selectedIds } = useListContext()
  const { mutate, isPending } = useAction(action)
  const confirmation = useConfirmation()

  const confirmMessage =
    typeof confirm === "string" ? translate(confirm) : "Do you confirm this action?"

  const onHandle = async (payload?) => {
    const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
    if (process) await mutate({ ids: selectedIds, payload })
  }

  return <ActionButtonBase {...props} onHandle={onHandle} isPending={isPending} />
}

export function CommonPayload({ active, onClose, onHandle, schema, title }) {
  const inputs = buildRA(schema)
  const translate = useTranslate()
  return (
    <AdminModal
      maxWidth="sm"
      open={active}
      onClose={onClose}
      title={translate(title, { _: title })}
    >
      <Form
        onSubmit={(data) => {
          onClose()
          onHandle(data)
        }}
      >
        {inputs}
        <PayloadButtons onClose={onClose} />
      </Form>
    </AdminModal>
  )
}

function ActionButtonBase({
  label,
  title,
  onHandle,
  isPending,
  icon,
  schema,
  id,
}: Omit<AdminAction, "action"> & {
  isPending?: boolean
  onHandle: (payload?: any) => void
}) {
  const resource = useResourceContext()
  const [payloadActive, setPayloadActive] = useState(false)

  const PayloadBuilder =
    findBuilder(["action", "payload", id, resource]) || (schema && CommonPayload)

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={() => {
          if (PayloadBuilder) setPayloadActive(true)
          else onHandle()
        }}
        disabled={isPending}
      >
        {buildIcon(icon)}
      </Button>
      {PayloadBuilder && (
        <PayloadBuilder
          active={payloadActive}
          onHandle={onHandle}
          onClose={() => setPayloadActive(false)}
          title={title || label}
          schema={schema}
        />
      )}
    </>
  )
}
