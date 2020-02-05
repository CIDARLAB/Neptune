// =========================================================
// * Vuetify Material Dashboard PRO - v2.1.0
// =========================================================
//
// * Product Page: https://www.creative-tim.com/product/vuetify-material-dashboard-pro
// * Copyright 2019 Creative Tim (https://www.creative-tim.com)
//
// * Coded by Creative Tim
//
// =========================================================
//
// * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/base'
import './plugins/chartist'
import './plugins/vee-validate'
import './plugins/vue-world-map'
import vuetify from './plugins/vuetify'
import i18n from './i18n'

Vue.config.productionTip = false


// router.beforeEach((to, from, next) => {
//   const authRequired = to.matched.some((route) => route.meta.requiresAuth)
//   const loggedin = store.getters.isLoggedIn
//   console.log("To:", to.path, "loggedin:",loggedin, "AuthReq:", authRequired)

//   if (loggedin && authRequired) {
//     console.log("Case 0")
//     next()
//   }

//   if (!loggedin && !authRequired) {
//     console.log("Case 1")
//     // if (to.path !== '/login') {
//     //   console.log("Case 2")
//     //   next('/login')
//     // } else {
//       // console.log("Case 3")
//       next()
//     // }
// } else if (!loggedin && authRequired) {
//       if (to.path !== '/login') {
//         console.log("Case 4")
//         next('/login')
//       } else {
//         console.log("Case 5")
//         next()
//       }
//   }
// })

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: h => h(App),
}).$mount('#app')


