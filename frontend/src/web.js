import { createRoot } from 'react-dom/client'

import { setupAdmin, processAdmin } from './utils'

import './admin'

const initAdmin = (globalThis.initAdmin = (props) => {
  const container = document.getElementById('root')
  const root = createRoot(container)
  root.render(processAdmin('admin', props))
})

export { setupAdmin, processAdmin }

export default initAdmin
