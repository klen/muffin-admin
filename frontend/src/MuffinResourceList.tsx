import sortBy from "lodash/sortBy"
import uniq from "lodash/uniq"
import { BulkDeleteButton, Datagrid, EditButton, List, ListActions, Pagination } from "react-admin"
import { buildRA } from "./buildRA"
import { BulkActionButton } from "./buttons"
import { useMuffinResourceOpts } from "./hooks"
import { AdminAction } from "./types"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinResourceList() {
  const { name, list } = useMuffinResourceOpts()
  const { fields, create, edit, show, limit, limitMax, filters, actions, remove, sort } = list

  const Actions = findBuilder(["list-actions", name])

  return (
    <List
      sort={sort}
      perPage={limit}
      actions={<ListActions hasCreate={create} />}
      filters={buildAdmin(["list-filters", name], filters)}
      bulkActionButtons={<Actions actions={actions} remove={remove} />}
      pagination={
        <Pagination rowsPerPageOptions={sortBy(uniq([10, 25, 50, 100, limit, limitMax]))} />
      }
    >
      <Datagrid rowClick={show ? "show" : edit ? "edit" : false}>
        {buildAdmin(["list-fields", name], fields)}
        {edit && <EditButton />}
      </Datagrid>
    </List>
  )
}

setupAdmin(["list"], MuffinResourceList)
setupAdmin(["list-fields"], buildRA)

setupAdmin(["list-filters"], buildRA)

function MuffinResourceListActions({
  actions,
  remove,
}: {
  actions: AdminAction[]
  remove?: boolean
}) {
  return (
    <>
      {actions.map((props) => (
        <BulkActionButton key={props.id} {...props} />
      ))}
      {remove && <BulkDeleteButton />}
    </>
  )
}

setupAdmin(["list-actions"], MuffinResourceListActions)
