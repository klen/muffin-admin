import {
  Button,
  FormGroupsProvider,
  useAugmentedForm,
  useListContext,
  useRecordContext,
  useResourceContext,
  useTranslate,
} from "react-admin"
import { FormProvider } from "react-hook-form"

import { useState } from "react"
import { buildRA } from "../buildRA"
import { AdminModal, PayloadButtons, useConfirmation } from "../common"
import { useAction } from "../hooks/useAction"
import { AdminAction, AdminPayloadProps } from "../types"
import { buildIcon, findBuilder } from "../utils"

export type ActionPayloadProps = {
  active: boolean
  onClose: () => void
  onHandle: (payload: any) => void
}

export function ActionButton({ paths, confirm, ...props }: AdminAction) {
  const translate = useTranslate()
  const record = useRecordContext()
  const confirmation = useConfirmation()
  const path = paths.find((p) => p.includes("{id}")) || paths[paths.length - 1]
  const { mutate, isPending } = useAction(path)

  const confirmMessage =
    typeof confirm === "string" ? translate(confirm) : "Do you confirm this action?"

  const onHandle = async (payload?) => {
    const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
    if (process) await mutate({ record, payload })
  }

  return <ActionButtonBase {...props} isPending={isPending} onHandle={onHandle} />
}

export function BulkActionButton({ paths, confirm, ...props }: AdminAction) {
  const translate = useTranslate()
  const { selectedIds } = useListContext()
  const path = paths.find((p) => !p.includes("{id}")) || paths[0]
  const { mutate, isPending } = useAction(path)
  const confirmation = useConfirmation()

  const confirmMessage =
    typeof confirm === "string" ? translate(confirm) : "Do you confirm this action?"

  const onHandle = async (payload?) => {
    const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
    if (process) await mutate({ ids: selectedIds, payload })
  }

  return <ActionButtonBase {...props} onHandle={onHandle} isPending={isPending} />
}

function ActionButtonBase({
  label,
  title,
  onHandle,
  isPending,
  icon,
  schema,
  id,
}: Omit<AdminAction, "paths"> & {
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

export function CommonPayload({ active, onClose, onHandle, schema, title }: AdminPayloadProps) {
  schema[0][1] = { ...schema[0][1], autoFocus: true }
  const inputs = buildRA(schema)
  const translate = useTranslate()
  const { form, formHandleSubmit } = useAugmentedForm({
    onSubmit: (data) => {
      onClose()
      onHandle(data)
      form.reset()
    },
    record: {},
  })

  return (
    <FormProvider {...form}>
      <FormGroupsProvider>
        <AdminModal
          maxWidth="sm"
          open={active}
          onClose={onClose}
          title={translate(title, { _: title })}
          actions={
            <PayloadButtons
              onClose={onClose}
              onSubmit={formHandleSubmit}
              isValid={form.formState.isValid}
            />
          }
        >
          {inputs}
        </AdminModal>
      </FormGroupsProvider>
    </FormProvider>
  )
}
