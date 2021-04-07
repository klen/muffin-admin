import Cookies from 'js-cookie'
import { makeRequest, requestHeaders } from './utils';


export default (props) => {

  const { identityURL, authorizeURL, loginURL, logoutURL, required, storage, storage_name } = props;

  const authorize = (name, value) => {
    if (value === undefined) {
      return storage == 'localstorage' ?  localStorage.getItem(name) : Cookies.get(name);
    }

    if (storage == 'localstorage') requestHeaders['Authorization'] = value;
    storage == 'localstorage' ?  localStorage.setItem(name, value) : Cookies.set(name, value);
    return value;
  }

  // Initialize request headers
  authorize(storage_name, authorize(storage_name));

  if (required) return {

      checkAuth: (data) => {
        const auth = authorize(storage_name);
        return auth ? Promise.resolve(auth) : Promise.reject();
      },

      checkError: (error) => {
        const {message, status, body} = error;

        if (status == 401 || status == 403) {
          authorize(storage_name, '');
          return Promise.reject();
        }

        return Promise.resolve();
      },

      getIdentity: async () => {
        let user = {};
        if (identityURL) {
          const {json} = await makeRequest(identityURL);
          user = json;
        }
        return user;
      },

      login: (data) => {
        if (!authorizeURL) return Promise.reject();
        return makeRequest(authorizeURL, {data, method: 'POST'}).then(response => {
          const token = response.json;
          authorize(storage_name, token);
          return token;
        })
      },

      logout: async () => {
        authorize(storage_name, '');
        const url = logoutURL || loginURL;
        if (url) globalThis.location = url;
        return true;
      },

      getPermissions: (data) => {
        const role = authorize(storage_name + '_role');
        return role ? Promise.resolve(role) : Promise.reject();
      },

  }

}
