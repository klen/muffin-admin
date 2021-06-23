import React from "react";

import { Resource } from "react-admin";
import * as icons from "@material-ui/icons"

import { checkParams, processAdmin, initRAItems, setupAdmin } from './utils'

import './views/list'
import './views/show'
import './views/edit'
import './views/create'


// Initialize Resources Components
setupAdmin('resources', resources => resources.map(res => processAdmin('resource', res, res.name)));

// Initialize a resource's component
setupAdmin('resource', checkParams((props, res) => {
    let { create, edit, icon, list, name, show, ...resProps } = props;

    return <Resource key={ name } name={ name } icon={ icons[icon] }
                        create={ processAdmin('create', create, res) }
                        edit={ processAdmin('edit', edit, res) }
                        list={ processAdmin('list', list, res) }
                        show={ processAdmin('show', show, res) }
                        { ...resProps } />;
}));
