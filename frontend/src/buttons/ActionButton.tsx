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

import { Link, Stack } from "@mui/material"
import { useState } from "react"
import { buildRA } from "../buildRA"
import { AdminModal, PayloadButtons, useConfirmation } from "../common"
import { HelpLink } from "../common/HelpLink"
import { useMuffinAdminOpts } from "../hooks"
import { useAction } from "../hooks/useAction"
import { AdminAction, AdminPayloadProps } from "../types"
import { buildIcon, findBuilder, requestHeaders } from "../utils"

export type ActionPayloadProps = {
  active: boolean
  onClose: () => void
  onHandle: (payload: any) => void
}

export function ActionButton({ paths, confirm, file, ...props }: AdminAction) {
  const translate = useTranslate()
  const record = useRecordContext()
  const confirmation = useConfirmation()

  const path = paths.find((p) => p.includes("{id}")) || paths[paths.length - 1]
  const { mutate, isPending } = useAction(path)

  if (file) return <FileButton path={path} record={record} {...props} />

  const confirmMessage =
    typeof confirm === "string" ? translate(confirm) : "Do you confirm this action?"

  const onHandle = async (payload?) => {
    const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
    if (process) await mutate({ record, payload })
  }

  return <ActionButtonBase {...props} isPending={isPending} onHandle={onHandle} />
}

export function ListActionButton({ paths, confirm, file, ...props }: AdminAction) {
  const translate = useTranslate()
  const confirmation = useConfirmation()
  const path = paths.find((p) => !p.includes("{id}")) || paths[paths.length - 1]
  const { mutate, isPending } = useAction(path)

  const { filterValues } = useListContext()
  if (file) return <FileButton path={path} filterValues={filterValues} {...props} />

  const confirmMessage =
    typeof confirm === "string" ? translate(confirm) : "Do you confirm this action?"

  const onHandle = async (payload?) => {
    const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
    if (process) await mutate({ payload })
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
  help,
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
          help={help}
        />
      )}
    </>
  )
}

export function CommonPayload({
  active,
  onClose,
  onHandle,
  schema,
  title,
  help,
}: AdminPayloadProps) {
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
          title={
            help
              ? ((
                <Stack alignItems="flex-start">
                  <span>{translate(title, { _: title })}</span>
                  <HelpLink href={help} style={{ alignSelf: "flex-end" }} />
                </Stack>
              ) as any)
              : translate(title, { _: title })
          }
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

function FileButton({
  path,
  record,
  label,
  icon,
  filterValues,
}: {
  path: string
  label: string
  icon: string
  record?: any
  filterValues?: any
}) {
  const { apiUrl } = useMuffinAdminOpts()
  let url = `${apiUrl}${path}?f`
  if (record) url = url.replace("{id}", record.id as string)
  const authorization = requestHeaders["Authorization"]
  if (authorization) url += `&t=${authorization}`
  if (Object.keys(filterValues).length) url += `&where=${JSON.stringify(filterValues)}`

  return (
    <Button href={url} label={label} component={Link}>
      {buildIcon(icon)}
    </Button>
  )
}
