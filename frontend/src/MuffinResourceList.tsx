import sortBy from "lodash/sortBy"
import uniq from "lodash/uniq"
import {
  BulkDeleteButton,
  Datagrid,
  EditButton,
  List,
  Pagination,
  useResourceContext,
} from "react-admin"
import { buildRA } from "./buildRA"
import { BulkActionButton } from "./buttons"
import { AdminAction, AdminResourceProps } from "./types"
import { buildAdmin, setupAdmin } from "./utils"

export function MuffinResourceList(props: AdminResourceProps["list"]) {
  const resourceName = useResourceContext()
  const { fields, edit, show, limit, limitMax, filters, actions, remove } = props
  return (
    <List
      bulkActionButtons={buildAdmin(["list-actions", resourceName], { actions, remove })}
      filters={buildAdmin(["list-filters", resourceName], filters) || undefined}
      perPage={limit}
      pagination={
        <Pagination rowsPerPageOptions={sortBy(uniq([10, 25, 50, 100, limit, limitMax]))} />
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
setupAdmin(
  ["list-actions"],
  ({ actions, remove }: { actions: AdminAction[]; remove?: boolean }) => (
    <>
      {actions.map((props) => (
        <BulkActionButton key={props.id} {...props} />
      ))}
      {remove && <BulkDeleteButton />}
    </>
  )
)
