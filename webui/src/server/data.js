/**
 * author: sailing
 * date: 2018/4/2
 * **/

import Axios from 'axios'
/**
 * post: 增
 * delete: 删
 * get: 查 所有参数和url 一起
 * put: 改
 * **/

// Axios.defaults.headers.common['Authentication-Token'] = store.state.token;
// console.log(18, x)
// console.log(19, state)
// 添加请求拦截器
Axios.interceptors.request.use(config => {
  // 在发送请求之前做些什么
  // 判断是否存在token，如果存在将每个页面header都添加token

  return config
}, error => {
  // 对请求错误做些什么
  return Promise.reject(error)
})
// http response 拦截器
Axios.interceptors.response.use(
  response => {
    if (response.data.code == -1 && response.data.message == '未登录') {
    }
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:

          router.replace({
            path: '/login',
            query: {
              redirect: router.currentRoute.fullPath
            } // 登录成功后跳入浏览的当前页面
          })
      }
    }
    return Promise.reject(error.response.data)
  })
function fetchServer(config) {
  // Axios.defaults.headers.common['iAuthToken'] = store.state.token


  var callback = config.callback || function() {}
  var errorBack = config.error || function() {}
  // if (!config.url.indexOf('http') == 0) {
  //     config.url = 'api' + config.url
  //   }
  if (window.location.href.indexOf('localhost') !== -1) {
    config.url = '/upload' + config.url
  }
  var c = {
    method: config.method || 'GET',
    url: config.url,
    data: config.data,
    headers: config.headers || {}
  }
  Axios(c).then(function(response) {
    return callback(response.data)
  }).catch(function(error) {
    if (errorBack) errorBack(error)
  })
}
export default fetchServer
