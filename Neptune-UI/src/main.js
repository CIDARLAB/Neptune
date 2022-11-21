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

import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./plugins/base";
import "./plugins/chartist";
import "./plugins/vee-validate";
import "./plugins/vue-world-map";
import vuetify from "./plugins/vuetify";
import i18n from "./i18n";


import * as Sentry from "@sentry/vue";
import { Integrations } from "@sentry/tracing";

import VueSocketIOExt from 'vue-socket.io-extended';
import { io } from 'socket.io-client';



Sentry.init({
  Vue,
  dsn:
    "https://f3be65f5f52c4d10848f481cc1230e99@o522267.ingest.sentry.io/5633457",
  integrations: [new Integrations.BrowserTracing()],
  logErrors: true,
  // We recommend adjusting this value in production, or using tracesSampler
  // for finer control
  tracesSampleRate: 1.0
});

Vue.config.productionTip = false;

const socket = io('http://localhost:8080');

Vue.use(VueSocketIOExt, socket);


// Vue.use(
//   new VueSocketIO({
//     debug: true,
//     connection: "localhost:8080" //"http://" + window.location.hostname
//     // vuex: {
//     //     store,
//     //     actionPrefix: 'SOCKET_',
//     //     mutationPrefix: 'SOCKET_'
//     // },
//     // options: { path: "/my-app/" } //Optional options
//   })
// );

router.beforeEach((to, from, next) => {
  const authRequired = to.matched.some(route => route.meta.requiresAuth);
  const loggedin = store.getters.isLoggedIn;
  console.log("To:", to.path, "loggedin:", loggedin, "AuthReq:", authRequired);

  if (loggedin && to.path == "") {
    console.log("Case -1");
    next("/dashboard");
  }

  if (loggedin && authRequired) {
    console.log("Case 0");
    next();
  }

  if (!loggedin && !authRequired) {
    console.log("Case 1");
    // if (to.path !== '/login') {
    //   console.log("Case 2")
    //   next('/login')
    // } else {
    // console.log("Case 3")
    next();
    // }
  } else if (!loggedin && authRequired) {
    if (to.path !== "/login") {
      console.log("Case 4");
      next("/login");
    } else {
      console.log("Case 5");
      next();
    }
  }
  next();
});

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: h => h(App)
}).$mount("#app");
