import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router/index.js'
import axios from "axios"
import VueCookies from 'vue-cookies'
import * as echarts from "echarts"



const app = createApp(App)

axios.defaults.baseURL = "http://127.0.0.1:5000"
// axios.defaults.baseURL = "http://192.168.101.31:5000"

app.config.globalProperties.$http = axios
app.config.globalProperties.$cookies = VueCookies
app.config.globalProperties.$echarts = echarts;

app.use(ElementPlus, {locale: zhCn})
app.use(router)
app.mount('#app')
