import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    barColor: 'rgba(0, 0, 0, .8), rgba(0, 0, 0, .8)',
    barImage: './images/CNCpic.png',
    drawer: null,
    isLoggedIn: false,
    userID: '007',
  },
  mutations: {
    SET_BAR_IMAGE (state, payload) {
      state.barImage = payload
    },
    SET_DRAWER (state, payload) {
      state.drawer = payload
    },
    SET_SCRIM (state, payload) {
      state.barColor = payload
    },
    updateUser(state, id){
      state.userID = id
      state.isLoggedIn = true
    },  
  },
  getters: {
    userID: state => state.userID,
    isLoggedIn: state => state.isLoggedIn,  
  },
  actions: {

  },
})
