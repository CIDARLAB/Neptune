(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-4d8c1835"],{"0fd9":function(t,a,i){"use strict";i("99af"),i("4160"),i("caad"),i("13d5"),i("4ec9"),i("b64b"),i("d3b7"),i("ac1f"),i("2532"),i("3ca3"),i("5319"),i("159b"),i("ddb0");var e=i("ade3"),s=i("5530"),n=(i("4b85"),i("2b0e")),r=i("d9f7"),o=i("80d2"),l=["sm","md","lg","xl"],c=["start","end","center"];function d(t,a){return l.reduce((function(i,e){return i[t+Object(o["E"])(e)]=a(),i}),{})}var p=function(t){return[].concat(c,["baseline","stretch"]).includes(t)},u=d("align",(function(){return{type:String,default:null,validator:p}})),h=function(t){return[].concat(c,["space-between","space-around"]).includes(t)},g=d("justify",(function(){return{type:String,default:null,validator:h}})),f=function(t){return[].concat(c,["space-between","space-around","stretch"]).includes(t)},m=d("alignContent",(function(){return{type:String,default:null,validator:f}})),v={align:Object.keys(u),justify:Object.keys(g),alignContent:Object.keys(m)},y={align:"align",justify:"justify",alignContent:"align-content"};function C(t,a,i){var e=y[t];if(null!=i){if(a){var s=a.replace(t,"");e+="-".concat(s)}return e+="-".concat(i),e.toLowerCase()}}var b=new Map;a["a"]=n["a"].extend({name:"v-row",functional:!0,props:Object(s["a"])({tag:{type:String,default:"div"},dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:p}},u,{justify:{type:String,default:null,validator:h}},g,{alignContent:{type:String,default:null,validator:f}},m),render:function(t,a){var i=a.props,s=a.data,n=a.children,o="";for(var l in i)o+=String(i[l]);var c=b.get(o);return c||function(){var t,a;for(a in c=[],v)v[a].forEach((function(t){var e=i[t],s=C(a,t,e);s&&c.push(s)}));c.push((t={"no-gutters":i.noGutters,"row--dense":i.dense},Object(e["a"])(t,"align-".concat(i.align),i.align),Object(e["a"])(t,"justify-".concat(i.justify),i.justify),Object(e["a"])(t,"align-content-".concat(i.alignContent),i.alignContent),t)),b.set(o,c)}(),t(i.tag,Object(r["a"])(s,{staticClass:"row",class:c}),n)}})},"91f7":function(t,a,i){"use strict";var e=i("e199"),s=i.n(e);s.a},"967a":function(t,a,i){"use strict";i.r(a);var e=function(){var t=this,a=t.$createElement,i=t._self._c||a;return i("v-container",{attrs:{fluid:""}},[i("v-row",[i("v-col",{attrs:{cols:"12",lg:"4"}},[i("base-material-chart-card",{staticClass:"px-4 py-3",attrs:{data:t.dailySalesChart.data,options:t.dailySalesChart.options,color:"success",type:"Line"}},[i("h4",{staticClass:"display-1 font-weight-light mt-2"},[t._v(" Rounded Line Chart ")]),i("div",{staticClass:"grey--text font-weight-light"},[t._v(" Line Chart ")])])],1),i("v-col",{attrs:{cols:"12",lg:"4"}},[i("base-material-chart-card",{staticClass:"px-4 py-3",attrs:{data:t.emailsSubscriptionChart.data,options:t.emailsSubscriptionChart.options,"responsive-options":t.emailsSubscriptionChart.responsiveOptions,color:"orange darken-1",type:"Line"}},[i("h4",{staticClass:"display-1 font-weight-light mt-2"},[t._v(" Line Chart With Points ")]),i("div",{staticClass:"grey--text font-weight-light"},[t._v(" Straight Lines Chart ")])])],1),i("v-col",{attrs:{cols:"12",lg:"4"}},[i("base-material-chart-card",{staticClass:"px-4 py-3",attrs:{data:t.dataCompletedTasksChart.data,options:t.dataCompletedTasksChart.options,color:"info",type:"Bar"}},[i("h4",{staticClass:"display-1 font-weight-light mt-2"},[t._v(" Simple Bar Chart ")]),i("div",{staticClass:"grey--text font-weight-light"},[t._v(" Last Last Campaign Performance ")])])],1),i("v-col",{attrs:{cols:"12",lg:"6"}},[i("base-material-card",{staticClass:"px-4 py-3",attrs:{id:"coloured-line",color:"info",icon:"mdi-chart-timeline-variant"},scopedSlots:t._u([{key:"after-heading",fn:function(){return[i("div",{staticClass:"display-1 mt-2 font-weight-light"},[t._v(" Coloured Line Chart "),i("span",{staticClass:"subtitle-1"},[t._v("— Rounded")])])]},proxy:!0}])},[i("chartist",{staticClass:"mt-3",staticStyle:{"max-height":"150px"},attrs:{data:t.colouredLine.data,options:t.colouredLine.options,type:"Line"}})],1),i("div",{staticClass:"py-3"}),i("base-material-card",{staticClass:"px-4 py-3",attrs:{id:"coloured-line",color:"warning",icon:"mdi-chart-timeline-variant"},scopedSlots:t._u([{key:"after-heading",fn:function(){return[i("div",{staticClass:"display-1 font-weight-light mt-2"},[t._v(" Coloured Line Chart "),i("span",{staticClass:"subtitle-1"},[t._v("— Multiple")])])]},proxy:!0}])},[i("chartist",{staticClass:"mt-3",staticStyle:{"max-height":"150px"},attrs:{data:t.multipleLine.data,options:t.multipleLine.options,type:"Line"}})],1)],1),i("v-col",{attrs:{cols:"12",lg:"6"}},[i("base-material-card",{staticClass:"px-4 py-3",attrs:{id:"multiple-bar",color:"success",icon:"mdi-poll-box"},scopedSlots:t._u([{key:"after-heading",fn:function(){return[i("div",{staticClass:"display-1 mt-2 font-weight-light"},[t._v(" Multiple Bars Chart "),i("span",{staticClass:"subtitle-1"},[t._v("— Bar Chart")])])]},proxy:!0}])},[i("chartist",{staticClass:"mt-3",staticStyle:{"max-height":"150px"},attrs:{data:t.multipleBar.data,options:t.multipleBar.options,type:"Bar"}})],1),i("div",{staticClass:"py-3"}),i("base-material-card",{staticClass:"px-4 py-3",attrs:{id:"pie",color:"success",icon:"mdi-chart-pie",title:"Pie Chart"}},[i("chartist",{staticStyle:{"max-height":"250px"},attrs:{data:t.pie.data,options:t.pie.options,type:"Pie"}}),i("v-divider",{staticClass:"ma-3"}),i("div",{staticClass:"px-3"},[i("div",{staticClass:"body-2 text-uppercase grey--text font-weight-bold mb-3"},[t._v(" Legend ")]),i("v-row",{staticClass:"ma-0",attrs:{align:"center"}},[i("v-avatar",{staticClass:"mr-1",attrs:{color:"info",size:"12"}}),i("span",{staticClass:"mr-3 font-weight-light"},[t._v("Apple")]),i("v-avatar",{staticClass:"mr-1",attrs:{color:"warning",size:"12"}}),i("span",{staticClass:"mr-3 font-weight-light"},[t._v("Samsung")]),i("v-avatar",{staticClass:"mr-1",attrs:{color:"red",size:"12"}}),i("span",{staticClass:"mr-3 font-weight-light"},[t._v("Windows Phone")])],1)],1)],1)],1)],1)],1)},s=[],n={data:function(){return{colouredLine:{data:{labels:["'06","'07","'08","'09","'10","'11","'12","'13","'14","'15"],series:[[275,500,290,55,700,700,500,750,630,900,930]]},options:{low:0,high:1e3,chartPadding:{top:0,right:0,bottom:0,left:0}}},dailySalesChart:{data:{labels:["M","T","W","T","F","S","S"],series:[[12,17,7,17,23,18,38]]},options:{low:0,high:50,chartPadding:{top:0,right:0,bottom:0,left:0},showPoint:!1}},dataCompletedTasksChart:{data:{labels:["12am","3pm","6pm","9pm","12pm","3am","6am","9am"],series:[[230,750,450,300,280,240,200,190]]},options:{low:0,high:1e3,chartPadding:{top:0,right:0,bottom:0,left:0}}},emailsSubscriptionChart:{data:{labels:["Ja","Fe","Ma","Ap","Mai","Ju","Jul","Au","Se","Oc","No","De"],series:[[542,443,320,780,553,453,326,434,568,610,756,895]]},options:{lineSmooth:this.$chartist.Interpolation.none(),axisX:{showGrid:!1},low:0,high:1e3,chartPadding:{top:0,right:5,bottom:0,left:0}},responsiveOptions:[["screen and (max-width: 640px)",{seriesBarDistance:5,axisX:{labelInterpolationFnc:function(t){return t[0]}}}]]},multipleBar:{data:{labels:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],series:[[542,443,320,780,553,453,326,434,568,610,756,895],[400,200,250,575,450,300,285,370,370,410,620,690]]},options:{seriesBarDistance:10,lineSmooth:this.$chartist.Interpolation.none(),axisX:{showGrid:!1},low:0,high:900,chartPadding:{top:0,right:5,bottom:0,left:0}},responsiveOptions:[["screen and (max-width: 640px)",{seriesBarDistance:5,axisX:{labelInterpolationFnc:function(t){return t[0]}}}]]},multipleLine:{data:{labels:["'06","'07","'08","'09","'10","'11","'12","'13","'14","'15"],series:[[275,500,290,55,700,700,500,750,630,900,930],[575,600,490,75,300,400,700,450,130,200,330],[575,300,890,155,640,540,800,250,230,400,630]]},options:{low:0,high:1e3,chartPadding:{top:0,right:0,bottom:0,left:0}}},pie:{data:{series:[62,32,6]},options:{labelInterpolationFnc:function(t){return"".concat(t,"%")}}},headers:[{sortable:!1,text:"ID",value:"id"},{sortable:!1,text:"Name",value:"name"},{sortable:!1,text:"Salary",value:"salary",align:"right"},{sortable:!1,text:"Country",value:"country",align:"right"},{sortable:!1,text:"City",value:"city",align:"right"}],items:[{id:1,name:"Dakota Rice",country:"Niger",city:"Oud-Tunrhout",salary:"$35,738"},{id:2,name:"Minerva Hooper",country:"Curaçao",city:"Sinaai-Waas",salary:"$23,738"},{id:3,name:"Sage Rodriguez",country:"Netherlands",city:"Overland Park",salary:"$56,142"},{id:4,name:"Philip Chanley",country:"Korea, South",city:"Gloucester",salary:"$38,735"},{id:5,name:"Doris Greene",country:"Malawi",city:"Feldkirchen in Kārnten",salary:"$63,542"}],tabs:0,list:{0:!1,1:!1,2:!1}}},methods:{complete:function(t){this.list[t]=!this.list[t]}}},r=n,o=(i("91f7"),i("2877")),l=i("6544"),c=i.n(l),d=i("8212"),p=i("62ad"),u=i("a523"),h=i("ce7e"),g=i("0fd9"),f=Object(o["a"])(r,e,s,!1,null,null,null);a["default"]=f.exports;c()(f,{VAvatar:d["a"],VCol:p["a"],VContainer:u["a"],VDivider:h["a"],VRow:g["a"]})},a523:function(t,a,i){"use strict";i("99af"),i("4de4"),i("b64b"),i("2ca0"),i("20f6"),i("4b85"),i("a15b"),i("498a");var e=i("2b0e");function s(t){return e["a"].extend({name:"v-".concat(t),functional:!0,props:{id:String,tag:{type:String,default:"div"}},render:function(a,i){var e=i.props,s=i.data,n=i.children;s.staticClass="".concat(t," ").concat(s.staticClass||"").trim();var r=s.attrs;if(r){s.attrs={};var o=Object.keys(r).filter((function(t){if("slot"===t)return!1;var a=r[t];return t.startsWith("data-")?(s.attrs[t]=a,!1):a||"string"===typeof a}));o.length&&(s.staticClass+=" ".concat(o.join(" ")))}return e.id&&(s.domProps=s.domProps||{},s.domProps.id=e.id),a(e.tag,s,n)}})}var n=i("d9f7");a["a"]=s("container").extend({name:"v-container",functional:!0,props:{id:String,tag:{type:String,default:"div"},fluid:{type:Boolean,default:!1}},render:function(t,a){var i,e=a.props,s=a.data,r=a.children,o=s.attrs;return o&&(s.attrs={},i=Object.keys(o).filter((function(t){if("slot"===t)return!1;var a=o[t];return t.startsWith("data-")?(s.attrs[t]=a,!1):a||"string"===typeof a}))),e.id&&(s.domProps=s.domProps||{},s.domProps.id=e.id),t(e.tag,Object(n["a"])(s,{staticClass:"container",class:Array({"container--fluid":e.fluid}).concat(i||[])}),r)}})},e199:function(t,a,i){}}]);
//# sourceMappingURL=chunk-4d8c1835.91720c2e.js.map