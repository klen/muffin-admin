import React from "react";
import ReactDOM from 'react-dom';

import initAdmin from "./admin"


globalThis.initAdmin = (props) => ReactDOM.render(initAdmin(props), document.getElementById('root'))
