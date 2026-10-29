import { Stack } from "@mui/material"
import { useState } from "react"
import {
  Button,
  FormGroupsProvider,
  useAugmentedForm,
  useListContext,
  useNotify,
  useRecordContext,
  useResourceContext,
  useTranslate,
} from "react-admin"
import { FormProvider } from "react-hook-form"
import { buildRA } from "../buildRA"
import { AdminModal, PayloadButtons, useConfirmation } from "../common"
import { HelpLink } from "../common/HelpLink"
import { useMuffinAdminOpts } from "../hooks"
import { useAction } from "../hooks/useAction"
import type { AdminAction, AdminPayloadProps } from "../types"
import { buildIcon, findBuilder, prepareFilters, requestHeaders } from "../utils"

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

  const onHandle = async (payload?: any) => {
    const process = confirm ? await confirmation.confirm({ message: confirmMessage }) : true
    if (process) mutate({ record, payload })
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

  const onHandle = async (payload?: any) => {
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

  const PayloadForm =
    findBuilder(["action-form", id, resource]) || (schema?.length ? CommonPayload : null)
  if (!PayloadForm)
    return (
      <Button label={label} title={title} onClick={() => onHandle()} disabled={isPending}>
        {buildIcon(icon)}
      </Button>
    )

  return (
    <>
      <Button
        label={label}
        title={title}
        onClick={() => setPayloadActive(true)}
        disabled={isPending}
      >
        {buildIcon(icon)}
      </Button>
      <PayloadForm
        active={payloadActive}
        onHandle={onHandle}
        onClose={() => setPayloadActive(false)}
        title={title || label}
        schema={schema}
        help={help}
      />
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
  if (schema?.length) schema[0][1] = { ...schema[0][1], autoFocus: true }
  const inputs = buildRA(schema || [])
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
                  <Stack sx={{ alignItems: "flex-start" }}>
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

export function buildFileUrl(apiUrl: string, path: string, id?: any, filterValues?: any) {
  let url = `${apiUrl}${path.replace("{id}", encodeURIComponent(String(id ?? "")))}?f`
  if (filterValues && Object.keys(filterValues).length) {
    url += `&where=${encodeURIComponent(prepareFilters(filterValues))}`
  }
  return url
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
  const notify = useNotify()

  const onClick = async () => {
    const url = buildFileUrl(apiUrl, path, record?.id, filterValues)

    try {
      const response = await fetch(url, { headers: new Headers(requestHeaders) })
      if (!response.ok) throw new Error(`Download failed (${response.status})`)

      const blob = await response.blob()
      const link = document.createElement("a")
      link.href = URL.createObjectURL(blob)
      link.download = path.split("/").pop() || "download"
      link.click()
      URL.revokeObjectURL(link.href)
    } catch (err: any) {
      notify(err?.message || "Download failed", { type: "error" })
    }
  }

  return (
    <Button onClick={onClick} label={label}>
      {buildIcon(icon)}
    </Button>
  )
}
