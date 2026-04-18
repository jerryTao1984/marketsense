import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import Vant from 'vant'
import 'vant/lib/index.css'
import App from './App.vue'
import './styles/main.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(Vant)
app.mount('#app')
