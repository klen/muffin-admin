import ExpandLess from "@mui/icons-material/ExpandLess"
import ExpandMore from "@mui/icons-material/ExpandMore"
import Collapse from "@mui/material/Collapse"
import ListItemButton from "@mui/material/ListItemButton"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemText from "@mui/material/ListItemText"

import { Menu, MenuProps, useTranslate } from "react-admin"

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
  const [groupOpen, setGroupOpen] = useState(false)

  return (
    <div>
      <ListItemButton onClick={() => setGroupOpen(!groupOpen)}>
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
