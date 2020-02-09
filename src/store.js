import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    barColor: 'rgba(0, 0, 0, .8), rgba(0, 0, 0, .8)',
    barImage: './images/CNCpic.png',
    drawer: null,
    isLoggedIn: true,
    userID: '007',
    currentFile: null,
    currentWorkspace: null,
    currentUser: null,
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
    updateCurrentFile(state, fid) {
      state.currentFile = fid
    },
    SET_WORKSPACE (state, payload) {
      state.currentWorkspace = payload
    },
    SET_CURRENT_FILE(state, payload) {
      state.currentFile = payload
    },
    SET_CURRENT_USER(state, payload){
      state.currentUser = payload
    }
  },
  getters: {
    userID: state => state.userID,
    isLoggedIn: state => state.isLoggedIn,
    currentFile: state => state.currentFile,
    currentWorkspace: state => state.currentWorkspace,
    currentUser: state => state.currentUser,
  },
  actions: {

  },
})
