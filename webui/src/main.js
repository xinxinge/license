// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Vue from 'vue'
import App from './App'
import './icons'
import router from './router'
import VueResourse from 'vue-resource'
import axios from 'axios'
import Vuex from 'vuex'
import store from './store/index'

Vue.prototype.$axios = axios


Vue.config.productionTip = false

Vue.use(ElementUI,VueResourse)
Vue.use(Vuex)
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
