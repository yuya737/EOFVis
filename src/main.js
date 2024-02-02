import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import './style.css'
import App from './App.vue'

import 'primevue/resources/themes/aura-light-green/theme.css'


const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(PrimeVue)
app.mount('#app')

