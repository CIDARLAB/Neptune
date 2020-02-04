<template>
  <v-app-bar
    id="app-bar"
    absolute
    app
    color="transparent"
    flat
    height="75"
  >
    <v-btn
      class="mr-3"
      elevation="1"
      fab
      small
      @click="$vuetify.breakpoint.smAndDown ? setDrawer(!drawer) : $emit('input', !value)"
    >
      <v-icon v-if="value">
        mdi-view-quilt
      </v-icon>

      <v-icon v-else>
        mdi-dots-vertical
      </v-icon>
    </v-btn>

    <v-toolbar-title
      class="hidden-sm-and-down font-weight-light"
      v-text="$route.name"
    />

    <v-spacer />

    <!-- <v-text-field
      :label="$t('search')"
      color="secondary"
      hide-details
      style="max-width: 165px;"
    >
      <template
        v-if="$vuetify.breakpoint.mdAndUp"
        v-slot:append-outer
      >
        <v-btn
          class="mt-n2"
          elevation="1"
          fab
          small
        >
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
      </template>
    </v-text-field> -->

    <div class="mx-3" />

    <v-btn
      class="ml-2"
      min-width="0"
      text
    >
      <v-icon>mdi-view-dashboard</v-icon>
    </v-btn>

    <v-menu
      bottom
      left
      offset-y
      origin="top right"
      transition="scale-transition"
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn
          class="ml-2"
          min-width="0"
          text
          v-bind="attrs"
          v-on="on"
        >
          <v-badge
            color="red"
            :content="totalNotifications"
            :value="totalNotifications"
            overlap
            bordered
          >
            <v-icon>mdi-bell</v-icon>
          </v-badge>
        </v-btn>
      </template>

      <v-list
        :tile="false"
        nav
      >
        <div>
          <app-bar-item
            v-for="(n, i) in notifications"
            :key="`item-${i}`"
          >
            <v-list-item-title v-text="n.text" />
          </app-bar-item>
          
          <v-divider
            class="mb-2 mt-2"
          />

          <app-bar-item
            :key="3"
          >
            <v-list-item-title
            v-text="'Clear Notifications'" 
            v-on:click="clearNotifications"            
            />
          </app-bar-item>

        </div>
      </v-list>
    </v-menu>

    <v-menu
      bottom
      left
      min-width="200"
      offset-y
      origin="top right"
      transition="scale-transition"
    >
      <template v-slot:activator="{ attrs, on }">
        <v-btn
          class="ml-2"
          min-width="0"
          text
          v-bind="attrs"
          v-on="on"
        >
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </template>

      <v-list
        :tile="false"
        flat
        nav
      >
          <app-bar-item
            :key="1"
          >
            <v-list-item-title
            v-text="'Profile'" 
            />
          </app-bar-item>
          <app-bar-item
            :key="2"
          >
            <v-list-item-title
            v-text="'Settings'" 
            />
          </app-bar-item>
          
          <v-divider
            class="mb-2 mt-2"
          />

          <app-bar-item
            :key="3"
          >
            <v-list-item-title
            v-text="'Logout'" 
            v-on:click="logout"            
            />
          </app-bar-item>

        <!-- <template v-for="(p, i) in profile">
          <v-divider
            v-if="p.divider"
            :key="`divider-${i}`"
            class="mb-2 mt-2"
          />

          <app-bar-item
            v-else
            :key="`item-${i}`"
          >
            <v-list-item-title
            v-text="p.title" 
            v-on:click="itemClick"            
            />
          </app-bar-item>
        </template> -->
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
  // Components
  import { VHover, VListItem } from 'vuetify/lib'

  // Utilities
  import { mapState, mapMutations } from 'vuex'

  import axios from 'axios'
  import router from '../../../../router'

  let self = this
  export default {
    name: 'DashboardCoreAppBar',

    components: {
      AppBarItem: {
        render (h) {
          return h(VHover, {
            scopedSlots: {
              default: ({ hover }) => {
                return h(VListItem, {
                  attrs: this.$attrs,
                  class: {
                    'black--text': !hover,
                    'white--text secondary elevation-12': hover,
                  },
                  props: {
                    activeClass: '',
                    dark: hover,
                    link: true,
                    ...this.$attrs,
                  },
                }, this.$slots.default)
              },
            },
          })
        },
      },
    },

    props: {
      value: {
        type: Boolean,
        default: false,
      },
    },

    data: () => ({
      notifications: [
        {
          text: "This is a test notification",
          jobid: 0,
        },
        {
          text: "This is also a test notification",
          jobid: 1,
        }
      ],
      profile: [
        { title: 'Profile' },
        { title: 'Settings' },
        { divider: true },
        { title: 'Log out',
          action: 'logout' 
        },
      ],
    }),

    computed: {
      ...mapState(['drawer']),
      totalNotifications: function() {
        return this.notifications.length
      }
    },

    methods: {
      ...mapMutations({
        setDrawer: 'SET_DRAWER',
      }),

      logout: function(event, context) {
        const config = {
          withCredentials: true,
          crossorigin: true,
          headers: {
            'Content-Type': 'application/json' //,
            // 'Access-Control-Allow-Origin': 'http://localhost:8080',
            // 'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            // 'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,OPTIONS',
            // 'Access-Control-Allow-Credentials': 'true'
          },
        }

        axios.get("/api/v2/logout", config)
          .then((response)=>{
            console.log(response)
            router.push('/login')
          })
          .catch((error)=>{
            console.log(error)
          })
      },

      clearNotifications: function(event){
        console.log("test", this)
        this.notifications = []
      }
    },
  }
</script>
