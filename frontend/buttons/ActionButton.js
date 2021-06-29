import React from 'react';

import { Button, CreateButton, useRefresh, useUnselectAll, useMutation, useNotify } from 'react-admin';
import * as icons from "@material-ui/icons"


export const BulkActionButton = ({label, icon, title, action, resource, selectedIds, ...props}) => {
  const refresh = useRefresh(), unselectAll = useUnselectAll(),
        notify = useNotify(), [mutate, { loading }] = useMutation(),
        Icon = icons[icon];

  let onClick = event => {
      mutate({
        resource,
        type: 'runAction',
        payload: {action, ids: selectedIds},
      }, {
        onSuccess: res => {
            if (res && res.data && res.data.message) notify(res.data.message, 'success');
            refresh();
            unselectAll(resource);
        },
        onFailure: err => {
          notify(typeof err === 'string' ? err : err.message, 'error')
        }
      })
  }

  return (
    <Button label={ label } title={ title } onClick={ onClick } disabled={ loading }>
      { Icon && <Icon /> }
    </Button>
  )
}

export const ActionButton = ({icon, label, title, record, resource, action}) => {
  const refresh = useRefresh(), notify = useNotify(),
        [mutate, { loading }] = useMutation(), Icon = icons[icon];

  let onClick = event => {
      mutate({
        resource,
        type: 'runAction',
        payload: {action, record},
      }, {
        onSuccess: res => {
            if (res && res.data && res.data.message) notify(res.data.message, 'success');
            refresh();
        },
        onFailure: err => {
          notify(typeof err === 'string' ? err : err.message, 'error')
        }
      })
  }

  return (
    <Button label={ label } title={ title } onClick={ onClick } disabled={ loading }>
      { Icon && <Icon /> }
    </Button>
  )

}
