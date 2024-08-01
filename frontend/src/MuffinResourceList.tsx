import sortBy from "lodash/sortBy"
import uniq from "lodash/uniq"
import {
  BulkDeleteButton,
  BulkExportButton,
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
import { ActionButton, BulkActionButton } from "./buttons"
import { HelpLink } from "./common/HelpLink"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinList() {
  const { name, list } = useMuffinResourceOpts()
  const { limit, limitMax, filters, sort } = list

  const DataGrid = findBuilder(["list-grid", name])
  const Toolbar = findBuilder(["list-toolbar", name])

  return (
    <List
      sort={sort}
      perPage={limit}
      actions={<Toolbar />}
      filters={buildAdmin(["list-filters", name], filters)}
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
  const BulkActions = findBuilder(["list-bulk-actions", name])
  return (
    <DatagridConfigurable
      rowClick={show ? "show" : edit ? "edit" : false}
      bulkActionButtons={<BulkActions />}
    >
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
    actions: baseActions = [],
    help,
    list: { create },
  } = useMuffinResourceOpts()
  const actions = baseActions.filter((a) => a.view?.includes("list"))
  const hasExport = actions.some((a) => a.id === "export")
  return (
    <TopToolbar>
      {help && <HelpLink href={help} />}
      <SelectColumnsButton />
      <FilterButton />
      {create && <CreateButton />}
      {actions.length ? actions.map((props) => <ActionButton key={props.id} {...props} />) : null}
      {!hasExport && <ExportButton />}
    </TopToolbar>
  )
}
setupAdmin(["list-toolbar"], MuffinListToolbar)

function MuffinListBulkActions() {
  const {
    actions: baseActions = [],
    list: { remove },
  } = useMuffinResourceOpts()
  const actions = baseActions.filter((a) => a.view?.includes("bulk"))
  return (
    <>
      {actions.map((props) => (
        <BulkActionButton key={props.id} {...props} />
      ))}
      <BulkExportButton />
      {remove && <BulkDeleteButton />}
    </>
  )
}

setupAdmin(["list-bulk-actions"], MuffinListBulkActions)
