import sortBy from "lodash/sortBy"
import uniq from "lodash/uniq"
import {
  BulkDeleteButton,
  CreateButton,
  DatagridConfigurable,
  EditButton,
  ExportButton,
  FilterButton,
  List,
  Pagination,
  SelectColumnsButton,
  TopToolbar,
} from "react-admin"
import { buildRA } from "./buildRA"
import { BulkActionButton } from "./buttons"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinResourceList() {
  const { name, list } = useMuffinResourceOpts()
  const { fields, edit, show, limit, limitMax, filters, sort } = list

  const Actions = findBuilder(["list-actions", name])
  const BulkActions = findBuilder(["list-bulk-actions", name])

  return (
    <List
      sort={sort}
      perPage={limit}
      actions={<Actions />}
      filters={buildAdmin(["list-filters", name], filters)}
      bulkActionButtons={<BulkActions />}
      pagination={
        <Pagination rowsPerPageOptions={sortBy(uniq([10, 25, 50, 100, limit, limitMax]))} />
      }
    >
      <DatagridConfigurable rowClick={show ? "show" : edit ? "edit" : false}>
        {buildAdmin(["list-fields", name], fields)}
        {edit && <EditButton />}
      </DatagridConfigurable>
    </List>
  )
}

setupAdmin(["list"], MuffinResourceList)
setupAdmin(["list-fields"], buildRA)

setupAdmin(["list-filters"], buildRA)

function MuffinListActions() {
  const {
    list: { create },
  } = useMuffinResourceOpts()
  return (
    <TopToolbar>
      <SelectColumnsButton />
      <FilterButton />
      {create && <CreateButton />}
      <ExportButton />
    </TopToolbar>
  )
}
setupAdmin(["list-actions"], MuffinListActions)

function MuffinListBulkActions() {
  const {
    list: { actions, remove },
  } = useMuffinResourceOpts()
  return (
    <>
      {actions.map((props) => (
        <BulkActionButton key={props.id} {...props} />
      ))}
      {remove && <BulkDeleteButton />}
    </>
  )
}

setupAdmin(["list-bulk-actions"], MuffinListBulkActions)
