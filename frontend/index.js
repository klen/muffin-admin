import ReactDOM from 'react-dom';

import { setupAdmin, processAdmin } from './utils.js'

import './admin.jsx';


let initAdmin = globalThis.initAdmin = (props) => ReactDOM.render(processAdmin('admin', props), document.getElementById('root'))

export { setupAdmin, processAdmin }

export default initAdmin
