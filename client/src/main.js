

import { createApp } from 'vue'
import "vuetify/dist/vuetify.min.css";
import '@fortawesome/fontawesome-free/css/all.css'
import App from './App.vue'
import router from './router'
import '../src/style.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, fa } from 'vuetify/iconsets/fa-svg'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import OpenLayersMap from "vue3-openlayers";


import store from './clients/vuex'

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'fa',
        aliases,
        sets: {
          fa,
        },
      },
  })
const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
library.add(fas)
library.add(far)
app.use(vuetify)
app.use(router)
app.use(store)
app.use(OpenLayersMap);
app.mount('#app')
