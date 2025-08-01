import sortBy from "lodash/sortBy"
import uniq from "lodash/uniq"
import { PropsWithChildren } from "react"
import {
  BulkDeleteButton,
  BulkExportButton,
  CreateButton,
  DatagridConfigurable,
  EditButton,
  ExportButton,
  FilterButton,
  InfiniteList,
  List,
  Pagination,
  SelectColumnsButton,
  TopToolbar,
} from "react-admin"
import { buildRA, buildRAComponent } from "./buildRA"
import { BulkActionButton, ListActionButton } from "./buttons"
import { HelpLink } from "./common/HelpLink"
import { useMuffinResourceOpts } from "./hooks"
import { AdminInput } from "./types"
import { buildAdmin, findBuilder, setupAdmin } from "./utils"

export function MuffinList({ children }: PropsWithChildren) {
  const { name, list, key } = useMuffinResourceOpts()
  const { limit, limitMax, limitTotal, sort, filters } = list

  const DataGrid = findBuilder(["list-grid", name])
  const Toolbar = findBuilder(["list-toolbar", name])
  const raFilters = buildAdmin(["list-filters", name], filters)

  return limitTotal ? (
    <List
      sort={sort}
      perPage={limit}
      filters={raFilters}
      actions={<Toolbar />}
      queryOptions={{ meta: { key } }}
      pagination={
        <Pagination rowsPerPageOptions={sortBy(uniq([10, 25, 50, 100, limit, limitMax]))} />
      }
    >
      {children}
      <DataGrid />
    </List>
  ) : (
    <InfiniteList
      sort={sort}
      perPage={limit}
      filters={raFilters}
      actions={<Toolbar />}
      queryOptions={{ meta: { key } }}
    >
      {children}
      <DataGrid />
    </InfiniteList>
  )
}

setupAdmin(["list"], MuffinList)
setupAdmin(["list-fields"], buildRA)

function muffinListFilters(filters: AdminInput[]) {
  return filters.map((props) => {
    const [rtype, opts] = props
    return buildRAComponent(rtype, {
      ...opts,
      variant: "outlined",
    })
  })
}
setupAdmin(["list-filters"], muffinListFilters)

function MuffinListDatagrid() {
  const { name, list } = useMuffinResourceOpts()
  const { fields, edit, show } = list
  const BulkActions = findBuilder(["list-actions", name])
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
      {actions.length
        ? actions.map((props) => <ListActionButton key={props.id} {...props} />)
        : null}
      {!hasExport && <ExportButton />}
    </TopToolbar>
  )
}
setupAdmin(["list-toolbar"], MuffinListToolbar)

function MuffinListActions() {
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

setupAdmin(["list-actions"], MuffinListActions)
