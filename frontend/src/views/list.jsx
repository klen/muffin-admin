import React from 'react'
import {
  BulkDeleteButton,
  Datagrid,
  EditButton,
  Filter,
  List,
  Pagination,
} from 'react-admin'
import uniq from 'lodash/uniq'
import sortBy from 'lodash/sortBy'

import initRAItems from '../ui'
import { checkParams, processAdmin, setupAdmin } from '../utils'
import { BulkActionButton } from '../buttons/ActionButton'

const defaultPagination = <Pagination rowsPerPageOptions={[10, 25, 50, 100]} />

// Initiliaze a list component
setupAdmin(
  'list',
  checkParams((props, res) => {
    let {
      children,
      filters,
      edit,
      pagination,
      show,
      limit,
      limitMax,
      actions,
      ...listProps
    } = props

    children = processAdmin('list-fields', children, res)
    if (edit) children.push(<EditButton key='edit-button' />)

    pagination = pagination || (
      <Pagination
        rowsPerPageOptions={sortBy(uniq([10, 25, 50, 100, limit, limitMax]))}
      />
    )

    return function MAList(props) {
      let Filters = (props) => (
        <Filter {...props}>{processAdmin('list-filters', filters, res)}</Filter>
      )
      let Actions = processAdmin('list-bulkActions', actions)

      props = { ...props, ...listProps }
      return (
        <List
          filters={<Filters />}
          bulkActionButtons={<Actions />}
          perPage={limit}
          pagination={pagination || defaultPagination}
          {...props}
        >
          <Datagrid rowClick={show ? 'show' : null}>{children}</Datagrid>
        </List>
      )
    }
  })
)

setupAdmin(
  'list-bulkActions',
  (actions) =>
    function MABulkActions(props) {
      let buttons = actions.map((action, idx) => {
        let aProps = { ...action, ...props }
        return <BulkActionButton key={idx} {...aProps} />
      })

      return (
        <>
          {buttons}
          <BulkDeleteButton {...props} />
        </>
      )
    }
)

setupAdmin('list-filters', initRAItems)
setupAdmin('list-fields', initRAItems)
