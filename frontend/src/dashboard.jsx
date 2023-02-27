import React from "react"

import {
  Grid,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableRow,
  TableCell,
} from "@mui/material"

import { setupAdmin } from "./utils"

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

const AdminCard = ({ src }) => {
  if (Array.isArray(src)) {
    return (
      <Grid container item spacing={2}>
        {src.map((card, idx) => (
          <AdminCard key={idx} src={card} />
        ))}
      </Grid>
    )
  }

  let { title, value } = src

  return (
    <Grid item xs>
      <Card>
        <CardContent>
          <Typography
            variant="h5"
            component="h2"
            m={2}
            style={{ textAlign: "center" }}
          >
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

// Process dashboard
setupAdmin("dashboard", (props) => {
  if (!props) return

  const Dashboard = () => (
    <Grid container spacing={1}>
      <AdminCard src={props} />
    </Grid>
  )
  return Dashboard
})
