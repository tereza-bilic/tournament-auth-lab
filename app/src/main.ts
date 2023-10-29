import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import authConfig from "../auth_config.json";
import envConfig from "../env_config.json";
import { createAuth0 } from "@auth0/auth0-vue";
import { Quasar } from 'quasar'
import axios from 'axios'
import VueAxios from 'vue-axios'

// Import icon libraries
import '@quasar/extras/roboto-font/roboto-font.css'
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/src/css/index.sass'


const app = createApp(App)

app.use(router(app))

app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
})
app.use(VueAxios, axios)

app.use(
  createAuth0({
    domain: authConfig.domain,
    clientId: authConfig.clientId,
    authorizationParams: {
      redirect_uri: envConfig.app_redirect,
    }
  })
)

app.mount('#app')
