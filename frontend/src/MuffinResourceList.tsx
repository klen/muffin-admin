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

export function MuffinList() {
  const { name, list } = useMuffinResourceOpts()
  const { limit, limitMax, filters, sort } = list

  const DataGrid = findBuilder(["list-grid", name])
  const Toolbar = findBuilder(["list-toolbar", name])
  const BulkActions = findBuilder(["list-bulk-actions", name])

  return (
    <List
      sort={sort}
      perPage={limit}
      actions={<Toolbar />}
      filters={buildAdmin(["list-filters", name], filters)}
      bulkActionButtons={<BulkActions />}
      pagination={
        <Pagination rowsPerPageOptions={sortBy(uniq([10, 25, 50, 100, limit, limitMax]))} />
      }
    >
      <DataGrid />
    </List>
  )
}

setupAdmin(["list"], MuffinList)
setupAdmin(["list-fields"], buildRA)
setupAdmin(["list-filters"], buildRA)

function MuffinListDatagrid() {
  const { name, list } = useMuffinResourceOpts()
  const { fields, edit, show } = list
  return (
    <DatagridConfigurable rowClick={show ? "show" : edit ? "edit" : false}>
      {buildAdmin(["list-fields", name], fields)}
      {buildAdmin(["list-grid-buttons", name])}
    </DatagridConfigurable>
  )
}

setupAdmin(["list-grid"], MuffinListDatagrid)

function MuffinListGridButtons() {
  const { list } = useMuffinResourceOpts()
  const { edit } = list
  if (!edit) return null
  return <EditButton />
}

setupAdmin(["list-grid-buttons"], MuffinListGridButtons)

function MuffinListToolbar() {
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
setupAdmin(["list-toolbar"], MuffinListToolbar)

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
