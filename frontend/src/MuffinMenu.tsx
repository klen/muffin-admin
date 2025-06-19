import ExpandLess from "@mui/icons-material/ExpandLess"
import ExpandMore from "@mui/icons-material/ExpandMore"
import Collapse from "@mui/material/Collapse"
import ListItemButton from "@mui/material/ListItemButton"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemText from "@mui/material/ListItemText"
import { matchPath, useLocation } from "react-router-dom"

import { Menu, MenuProps, useBasename, useTheme, useTranslate } from "react-admin"

import find from "lodash/find"
import groupBy from "lodash/groupBy"
import { useContext, useState } from "react"
import { MuffinAdminContext } from "./context"
import { AdminResourceProps } from "./types"
import { findIcon, setupAdmin } from "./utils"

export function MuffinMenu(props: MenuProps) {
  const { resources } = useContext(MuffinAdminContext)

  const groups = groupBy(
    resources.filter((r) => r.group),
    "group"
  )
  const groupRendered = []

  return (
    <Menu {...props}>
      <Menu.DashboardItem />
      {resources.map(({ name, group }) => {
        if (!group) return <Menu.ResourceItem name={name} key={name} />
        if (groupRendered.includes(group)) return null
        groupRendered.push(group)
        const groupResources = groups[group]
        return <MenuGroup name={group} resources={groupResources} key={group} />
      })}
    </Menu>
  )
}

setupAdmin(["menu"], MuffinMenu)

function MenuGroup({ name, resources }: { name: string; resources: AdminResourceProps[] }) {
  const iconRes = find(resources, "icon")
  const Icon = iconRes ? findIcon(iconRes.icon) : null
  const translate = useTranslate()
  const basename = useBasename()
  const { pathname } = useLocation()
  const match = resources.some(
    (resource) => !!matchPath({ path: `${basename}/${resource.name}/*` }, pathname)
  )
  const [groupOpen, setGroupOpen] = useState(match)
  const theme = useTheme()[0]
  const colors =
    theme == "dark"
      ? {
          text: "rgba(255, 255, 255, 0.87)",
          textSecondary: "rgba(255, 255, 255, 0.6)",
        }
      : {
          text: "rgba(0, 0, 0, 0.87)",
          textSecondary: "rgba(0, 0, 0, 0.6)",
        }

  return (
    <div>
      <ListItemButton
        onClick={() => setGroupOpen(!groupOpen)}
        sx={{
          color: match ? colors.text : colors.textSecondary,
        }}
      >
        {Icon && (
          <ListItemIcon sx={{ minWidth: 40 }}>
            <Icon />
          </ListItemIcon>
        )}
        <ListItemText primary={translate(`groups.${name}`)} />
        {groupOpen ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>
      <Collapse in={groupOpen} timeout="auto" unmountOnExit>
        {resources.map(({ name }) => (
          <Menu.ResourceItem name={name} key={name} />
        ))}
      </Collapse>
    </div>
  )
}
