import Card from "@mui/material/Card"
import CardContent from "@mui/material/CardContent"
import Grid from "@mui/material/Grid"
import Table from "@mui/material/Table"
import TableBody from "@mui/material/TableBody"
import TableCell from "@mui/material/TableCell"
import TableRow from "@mui/material/TableRow"
import Typography from "@mui/material/Typography"
import { AdminDashboardBlock, AdminOpts } from "./types"

export function MuffinDashboard(props: AdminOpts["dashboard"]) {
  return (
    <Grid container spacing={1}>
      {Array.isArray(props) ? (
        props.map((card, idx) => <DashboardCard key={idx} {...card} />)
      ) : (
        <DashboardCard {...props} />
      )}
    </Grid>
  )
}

function DashboardCard(title, value: AdminDashboardBlock) {
  return (
    <Grid item xs>
      <Card>
        <CardContent>
          <Typography variant="h5" component="h2" m={2} style={{ textAlign: "center" }}>
            {title}
          </Typography>
          {(Array.isArray(value) && <AdminTableView src={value} />) || (
            <pre>{JSON.stringify(value, null, 2)}</pre>
          )}
        </CardContent>
      </Card>
    </Grid>
  )
}

const AdminTableView = ({ src }) => (
  <Table>
    <TableBody>
      {src.map((row, idx) => (
        <TableRow key={idx} hover>
          {row.map((cell, idx) => (
            <TableCell key={idx}>{cell}</TableCell>
          ))}
        </TableRow>
      ))}
    </TableBody>
  </Table>
)
