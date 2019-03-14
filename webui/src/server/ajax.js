import axios from 'axios'
import {
  Loading,
  Message
} from 'element-ui'
import store from '../store/index.js'
import NProgress from 'nprogress'

const axiosIns = axios.create()
axiosIns.interceptors.request.use(function(config) {
  // 在发送请求之前做些什么
  if (store.state.token) {
    config.headers.common['iAuthToken'] = store.state.token
  }
  return config
}, function(error) {
  console.log('错误的传参')
  return Promise.reject(error)
})

axiosIns.interceptors.response.use((res) => {
  // 对响应数据做些事
  if (!res.data) {
    return Promise.reject(res)
  }
  return res
}, (error) => {
  return Promise.reject(error)
})
const ajaxMethod = ['get', 'post', 'put', 'delete']
const ajax = {}
ajaxMethod.forEach((method) => {
  NProgress.start()
  NProgress.inc()
  ajax[method] = function(uri, data, config) {
    // if (!uri.indexOf('http') == 0) {
    //   uri = 'api' + uri
    // }
    if (window.location.href.indexOf('localhost') !== -1) {
      uri = '/upload/' + uri
    }
    return new Promise(function(resolve, reject) {
      axiosIns[method](uri, data, config).then((response) => {
        NProgress.done()
        NProgress.remove()
        if (response.data.code === 0) {
          resolve(response.data)
        } else {
          Message.error(response.data.strcode)
        }
      }).catch(function(error) {
        reject(error)
        NProgress.done()
        NProgress.remove()
      })
    })
  }
})
export default ajax
