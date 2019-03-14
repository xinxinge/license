import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex)
const state = {
  globalLoading: false,
  globalDialog: false,
  dcArr: [],
  token: '',
  code: '',
  user_permission: {},
  role_permission: {}
}
const mutations = {
  set_code(state,code){
    this.state.code = code
  },
  set_list(state,date){
    state.dcArr = date
  }
}
const store = new Vuex.Store({
  modules: {
    chooseArr: [],
    app,

  },
  state,
  mutations
})

export default store
