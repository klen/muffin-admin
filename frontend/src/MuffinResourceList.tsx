import React from "react"
import {
  BulkDeleteButton,
  Datagrid,
  EditButton,
  List,
  Pagination,
  useResourceContext,
} from "react-admin"
import { buildAdmin, setupAdmin } from "./utils"
import { AdminAction, AdminResourceProps } from "./types"
import { buildRA } from "./buildRA"
import uniq from "lodash/uniq"
import sortBy from "lodash/sortBy"
import { BulkActionButton } from "./buttons"

export function MuffinResourceList(props: AdminResourceProps["list"]) {
  const resourceName = useResourceContext()
  const { fields, edit, show, limit, limitMax, filters, actions } = props
  return (
    <List
      bulkActionButtons={buildAdmin(["list-actions", resourceName], actions)}
      filters={buildAdmin(["list-filters", resourceName], filters) || undefined}
      perPage={limit}
      pagination={
        <Pagination
          rowsPerPageOptions={sortBy(uniq([10, 25, 50, 100, limit, limitMax]))}
        />
      }
    >
      <Datagrid rowClick={show ? "show" : edit ? "edit" : false}>
        {buildAdmin(["list-fields", resourceName], fields)}
        {edit && <EditButton />}
      </Datagrid>
    </List>
  )
}

setupAdmin(["list"], (props) => <MuffinResourceList {...props} />)
setupAdmin(["list-fields"], buildRA)
setupAdmin(["list-filters"], buildRA)
setupAdmin(["list-actions"], (actions: AdminAction[]) => (
  <>
    {actions.map((props, idx) => (
      <BulkActionButton key={idx} {...props} />
    ))}
    <BulkDeleteButton />
  </>
))
