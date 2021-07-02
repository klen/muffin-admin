import React from 'react';

import { Button } from 'react-admin';
import { Link } from 'react-router-dom';
import * as icons from "@material-ui/icons"

// import LinkButton from '../buttons/LinkButton'
// <LinkButton label="Messages" icon="Message" resource="message" filters={{ user: data.id }} />
//
const LinkButton = ({label, icon, title, resource, filters, ...props}) => {
  let Icon = icons[icon], linkParams = {pathname: `/${resource}`};
  if (filters) linkParams.search = `filter=${JSON.stringify(filters)}`;

  return (
    <Button label={ label } title={ title } component={ Link } to={ linkParams }>
      { Icon && <Icon /> }
    </Button>
  )
}

export default LinkButton
