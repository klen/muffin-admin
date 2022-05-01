import React, { useEffect } from 'react'
import {
  Button,
  useRefresh,
  useUnselectAll,
  useNotify,
  useRecordContext,
} from 'react-admin'
import * as icons from '@mui/icons-material'

import useAction from '../hooks/useAction'

export const BulkActionButton = ({
  label,
  icon,
  title,
  action,
  resource,
  selectedIds,
}) => {
  const refresh = useRefresh(),
    unselectAll = useUnselectAll(resource),
    notify = useNotify(),
    Icon = icons[icon]

  const mutation = useAction(resource, action)

  let onClick = () => {
    mutation.mutate(
      {
        action,
        ids: selectedIds,
      },
      {
        onSuccess: ({ data }) => {
          if (data && data.message) notify(data.message, { type: 'success' })
          refresh()
          unselectAll()
        },
        onError: (err) => {
          notify(typeof err === 'string' ? err : err.message, { type: 'error' })
        },
      }
    )
  }

  return (
    <Button
      label={label}
      title={title}
      onClick={onClick}
      disabled={mutation.isLoading}
    >
      {Icon && <Icon />}
    </Button>
  )
}

export const ActionButton = (props) => {
  const { icon, label, title, resource, action } = props
  const record = useRecordContext()
  const mutation = useAction(resource, action)

  const refresh = useRefresh(),
    notify = useNotify(),
    Icon = icons[icon]

  let onClick = () => {
    mutation.mutate(
      { record },
      {
        onSuccess: ({ data }) => {
          refresh()
          if (data && data.redirectTo) window.location = data.redirectTo
          if (data && data.message) notify(data.message, { type: 'success' })
        },
        onError: (error) => {
          notify(typeof error === 'string' ? error : error.message, {
            type: 'error',
          })
        },
      }
    )
  }

  return (
    <Button
      label={label}
      title={title}
      onClick={onClick}
      disabled={mutation.isLoading}
    >
      {Icon && <Icon />}
    </Button>
  )
}

export default ActionButton
