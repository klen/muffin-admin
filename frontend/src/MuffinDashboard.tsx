import Card from "@mui/material/Card"
import CardContent from "@mui/material/CardContent"
import Grid from "@mui/material/Grid"
import Stack from "@mui/material/Stack"
import Table from "@mui/material/Table"
import TableBody from "@mui/material/TableBody"
import TableCell from "@mui/material/TableCell"
import TableRow from "@mui/material/TableRow"
import Typography from "@mui/material/Typography"
import { useTranslate } from "react-admin"
import { HelpLink } from "./common/HelpLink"
import { useMuffinAdminOpts } from "./hooks"
import type { AdminDashboardBlock } from "./types"
import { buildAdmin, setupAdmin } from "./utils"
import { VERSION } from "./version"

export function MuffinDashboard() {
  const { dashboard, help } = useMuffinAdminOpts()
  const translate = useTranslate()
  return (
    <Stack sx={{ gap: 2, pt: 1 }}>
      <Stack direction="row" sx={{ flexWrap: "wrap", gap: 1 }}>
        {help && <HelpLink href={help} label={translate("muffin.how_to_use_admin")} />}
        {buildAdmin(["dashboard-actions"])}
      </Stack>
      <Grid container spacing={1}>
        {buildAdmin(["dashboard-content"])}
        <AdminCards src={dashboard} />
      </Grid>
      {VERSION && (
        <Typography variant="body2" color="textSecondary" align="center" sx={{ my: 1 }}>
          Muffin Admin v.{VERSION}
        </Typography>
      )}
    </Stack>
  )
}

setupAdmin(["dashboard"], MuffinDashboard)
setupAdmin(["dashboard-actions"], () => null)
setupAdmin(["dashboard-content"], () => null)

function AdminCards({ src }: { src: AdminDashboardBlock | AdminDashboardBlock[] }) {
  if (Array.isArray(src))
    return (
      <Grid container spacing={2}>
        {src.map((card, idx) => (
          <AdminCards key={idx} src={card} />
        ))}
      </Grid>
    )

  return <DashboardCard {...src} />
}

function DashboardCard({ title, value }: AdminDashboardBlock) {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h2" sx={{ m: 2, textAlign: "center" }}>
          {title}
        </Typography>
        {(Array.isArray(value) && <AdminTableView src={value} />) || (
          <pre>{JSON.stringify(value, null, 2)}</pre>
        )}
      </CardContent>
    </Card>
  )
}

const AdminTableView = ({ src }) => (
  <Table width="100%" sx={{ tableLayout: "fixed" }}>
    <TableBody>
      {src.map((row: any, idx: number) => (
        <TableRow key={idx} hover>
          {row.map((cell: any, idx: number) => (
            <TableCell key={idx}>{cell}</TableCell>
          ))}
        </TableRow>
      ))}
    </TableBody>
  </Table>
)
