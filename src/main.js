import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router/index.js'
import axios from "axios"
import VueCookies from 'vue-cookies'
import * as echarts from "echarts"
// 全局引入global
import global from "@/global/global.js"

const app = createApp(App)

app.config.globalProperties.$http = axios
app.config.globalProperties.$cookies = VueCookies
app.config.globalProperties.$echarts = echarts
app.config.globalProperties.$global = global

axios.defaults.baseURL = global.baseURL

app.use(ElementPlus, {locale: zhCn})
app.use(router)
app.mount('#app')
