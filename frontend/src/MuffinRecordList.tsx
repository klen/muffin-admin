import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography"
import {
  Datagrid,
  type SortPayload,
  useGetList,
  useRecordContext,
  useTheme,
  useTranslate,
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
  const translate = useTranslate()
  const {
    list: { fields },
  } = useMuffinResourceOpts(resource)
  const { data, isPending } = useGetList(resource, { sort, filter: filter(record) })
  const rowSx = (row: any) => {
    if (!highlightBy) return {}
    const { field, value } = highlightBy(record)
    const selectColor = theme === "dark" ? "#646D7E" : "#B4CFEC"
    return { backgroundColor: row[field] === value ? selectColor : "" }
  }
  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6">
        {translate(`resources.${resource}.name`, { smart_count: 2 })}
      </Typography>
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
