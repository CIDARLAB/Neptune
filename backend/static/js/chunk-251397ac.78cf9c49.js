(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-251397ac"],{7496:function(e,t,n){"use strict";var a=n("5530"),r=(n("df86"),n("7560")),o=n("58df");t["a"]=Object(o["a"])(r["a"]).extend({name:"v-app",props:{dark:{type:Boolean,default:void 0},id:{type:String,default:"app"},light:{type:Boolean,default:void 0}},computed:{isDark:function(){return this.$vuetify.theme.dark}},beforeCreate:function(){if(!this.$vuetify||this.$vuetify===this.$root)throw new Error("Vuetify is not properly initialized, see https://vuetifyjs.com/getting-started/quick-start#bootstrapping-the-vuetify-object")},render:function(e){var t=e("div",{staticClass:"v-application--wrap"},this.$slots.default);return e("div",{staticClass:"v-application",class:Object(a["a"])({"v-application--is-rtl":this.$vuetify.rtl,"v-application--is-ltr":!this.$vuetify.rtl},this.themeClasses),attrs:{"data-app":!0},domProps:{id:this.id}},[t])}})},cd59:function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app",[n("dashboard-core-app-bar",{model:{value:e.expandOnHover,callback:function(t){e.expandOnHover=t},expression:"expandOnHover"}}),n("dashboard-core-drawer",{attrs:{"expand-on-hover":e.expandOnHover},on:{"update:expandOnHover":function(t){e.expandOnHover=t},"update:expand-on-hover":function(t){e.expandOnHover=t}}}),n("dashboard-core-view")],1)},r=[],o=(n("d3b7"),{name:"DashboardIndex",components:{DashboardCoreAppBar:function(){return n.e("chunk-f24548a6").then(n.bind(null,"8e07"))},DashboardCoreDrawer:function(){return n.e("chunk-08042682").then(n.bind(null,"09ae"))},DashboardCoreSettings:function(){return n.e("chunk-0162d498").then(n.bind(null,"51c9"))},DashboardCoreView:function(){return n.e("chunk-e0b36f76").then(n.bind(null,"2038"))}},data:function(){return{expandOnHover:!1}}}),i=o,d=n("2877"),s=n("6544"),u=n.n(s),p=n("7496"),c=Object(d["a"])(i,a,r,!1,null,null,null);t["default"]=c.exports;u()(c,{VApp:p["a"]})},df86:function(e,t,n){}}]);
//# sourceMappingURL=chunk-251397ac.78cf9c49.js.map