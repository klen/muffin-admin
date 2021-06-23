import React from 'react';

import get from 'lodash/get';
import { useRecordContext } from 'ra-core';
import Avatar from '@material-ui/core/Avatar';


const AvatarField = ({ source, record, alt, style, nameProp, ...props }) => {

  let sourceValue = get(record, source),
      letters = null,
      name = record[nameProp];

  if (name) letters = name.split(' ').map( n => n[0].toUpperCase() ).join('');

  return <Avatar src={ record[source] } alt={ alt } style={ style }>{ letters }</Avatar>

}

AvatarField.displayName = 'AvatarField';
AvatarField.defaultProps = {
  addLabel: true,
}

export default AvatarField;
