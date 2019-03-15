import Vue from 'vue'
import Router from 'vue-router'
import Register from '@/views/register/Register'
import Login from '@/views/login/Login'
import Choose from '@/views/choose/ChooseDroduct'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/choose',
      name: 'Choose',
      component: Choose
    }
  ]
})
