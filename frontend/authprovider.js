import Cookies from 'js-cookie'
import { makeRequest, requestHeaders } from './utils';


export default (props) => {

  const { identityURL, authorizeURL, logoutURL, required, storage, storage_name } = props;

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

  let getIdentity = async () => {
      if (identityURL) {
        let {json} = await makeRequest(identityURL);
        return json;
      }
  }

  if (required) return {

      getIdentity,

      checkAuth: async (data) => {
        const auth = authorize(storage_name);
        if (!auth) throw {redirectTo: logoutURL, message: 'Authorization required'}

        if (!identityURL) return auth;

        let user = await getIdentity();
        if (!user)  throw {redirectTo: logoutURL, message: 'Authorization required'};

        return user;
      },

      checkError: async (error) => {
        const {message, status, body} = error;

        if (status == 401 || status == 403) {
          authorize(storage_name, '');
          throw {redirectTo: logoutURL, message: 'Invalid authorization'};
        }

      },

      login: async (data) => {
        if (!authorizeURL) throw {message: 'Authorization is not supported'}

        let {json} = await makeRequest(authorizeURL, {data, method: 'POST'})
        authorize(storage_name, json);
      },

      logout: async () => {
        authorize(storage_name, '');
        return logoutURL;
      },

      getPermissions: (data) => {
        const role = authorize(storage_name + '_role');
        return role ? Promise.resolve(role) : Promise.reject();
      },

  }

}
