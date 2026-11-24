import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography"
import {
  Datagrid,
  type SortPayload,
  useGetList,
  useGetResourceLabel,
  useRecordContext,
  useTheme,
} from "react-admin"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin } from "./utils"

type TProps = {
  resource: string
  filter: (record: any) => Record<string, any>
  sort?: SortPayload
  highlightBy?: (record: any) => { field: string; value: string }
}
export function MuffinRecordList({ resource, filter, sort, highlightBy }: TProps) {
  const record = useRecordContext()
  const theme = useTheme()[0]
  const getResourceLabel = useGetResourceLabel()
  const {
    list: { fields, sort: defaultSort },
  } = useMuffinResourceOpts(resource)
  const { data, isPending } = useGetList(
    resource,
    { sort: sort ?? defaultSort, filter: record ? filter(record) : {} },
    { enabled: Boolean(record) }
  )
  const rowSx = (row: any) => {
    if (!highlightBy || !record) return {}
    const { field, value } = highlightBy(record)
    const selectColor = theme === "dark" ? "#646D7E" : "#B4CFEC"
    return { backgroundColor: row[field] === value ? selectColor : "" }
  }
  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6">{getResourceLabel(resource, 2)}</Typography>
      <Datagrid
        resource={resource}
        bulkActionButtons={false}
        isPending={isPending}
        data={data}
        rowSx={rowSx}
      >
        {buildAdmin(["list-fields", resource], fields)}
      </Datagrid>
    </Box>
  )
}
