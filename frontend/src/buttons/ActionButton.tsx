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

import { useAction } from "../hooks/useAction"
import { buildIcon } from "../utils"

export function BulkActionButton({ label, icon, title, action }) {
  const resource = useResourceContext()
  const { selectedIds } = useListContext()
  const refresh = useRefresh(),
    unselectAll = useUnselectAll(resource),
    notify = useNotify()

  const mutation = useAction(resource, action)

  const onClick = () => {
    mutation.mutate(
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
    <Button label={label} title={title} onClick={onClick} disabled={mutation.isLoading}>
      {buildIcon(icon)}
    </Button>
  )
}

export function ActionButton(props) {
  const { icon, label, title, resource, action } = props
  const record = useRecordContext()
  const { mutate, isLoading } = useAction(resource, action)

  const refresh = useRefresh(),
    notify = useNotify(),
    Icon = icons[icon]

  const onClick = () => {
    mutate(
      { record },
      {
        onSuccess: ({ data }) => {
          refresh()
          if (data && data.redirectTo) window.location = data.redirectTo
          if (data && data.message) notify(data.message, { type: "success" })
        },
        onError: (err) => {
          notify(typeof err === "string" ? err : err.message, {
            type: "error",
          })
        },
      }
    )
  }

  return (
    <Button label={label} title={title} onClick={onClick} disabled={isLoading}>
      {Icon && <Icon />}
    </Button>
  )
}
