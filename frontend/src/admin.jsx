import React from 'react'

import { Admin, AppBar, Layout, Login } from 'react-admin'
import { IconButton, SvgIcon, Tooltip, Typography } from '@mui/material'
import * as icons from '@mui/icons-material'

import authProvider from './authprovider'
import dataProvider from './dataprovider'
import { processAdmin, setupAdmin } from './utils'

import './dashboard.jsx'
import './resources.jsx'

// Initialize the admin
setupAdmin('admin', (props) => {
  const { apiUrl, auth, adminProps, appBarLinks, dashboard, resources } = props

  let appBar = (props) => (
    <AppBar {...props}>
      <Typography
        variant='h6'
        color='inherit'
        id='react-admin-title'
        style={{
          flex: 1,
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap',
          overflow: 'hidden',
        }}
      />
      {appBarLinks.map((info) => (
        <Tooltip key={info.url} title={info.title}>
          <IconButton color='inherit' href={info.url}>
            <SvgIcon component={icons[info.icon]} />
          </IconButton>
        </Tooltip>
      ))}
    </AppBar>
  )

  return (
    <Admin
      authProvider={processAdmin('auth', auth)}
      dataProvider={processAdmin('data', apiUrl)}
      dashboard={processAdmin('dashboard', dashboard)}
      loginPage={processAdmin('login', auth)}
      layout={(props) => <Layout appBar={appBar} {...props} />}
      {...adminProps}
    >
      {processAdmin('resources', resources)}
    </Admin>
  )
})

// Initialize authentication and data providers
setupAdmin('auth', authProvider)
setupAdmin('data', dataProvider)

// Initialize login page
setupAdmin('login', () => Login)
