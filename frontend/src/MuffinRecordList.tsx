import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography"
import { Datagrid, SortPayload, useGetList, useRecordContext, useTranslate } from "react-admin"
import { useMuffinResourceOpts } from "./hooks"
import { buildAdmin } from "./utils"

type TProps = {
  resource: string
  filter: (record: any) => Record<string, any>
  sort?: SortPayload
}
export function MuffinRecordList({ resource, filter, sort }: TProps) {
  const record = useRecordContext()
  const translate = useTranslate()
  const {
    list: { fields },
  } = useMuffinResourceOpts(resource)
  const { data, isPending } = useGetList(resource, { sort, filter: filter(record) })
  return (
    <Box p={2}>
      <Typography variant="h6">
        {translate(`resources.${resource}.name`, { smart_count: 2 })}
      </Typography>
      <Datagrid resource={resource} bulkActionButtons={false} isPending={isPending} data={data}>
        {buildAdmin(["list-fields", resource], fields)}
      </Datagrid>
    </Box>
  )
}
