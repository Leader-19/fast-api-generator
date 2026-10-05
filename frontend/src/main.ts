import { createApp } from 'vue'
import App from './App.vue'
import router from './router'   // ← import the router
import './assets/main.css'      // or your Tailwind CSS file

const app = createApp(App)

app.use(router)                 // ← this is the important line
app.mount('#app')