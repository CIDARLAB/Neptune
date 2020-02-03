<template>
  <v-app-bar
    absolute
    color="transparent"
    flat
    height="85"
  >
    <v-container class="px-0 text-right d-flex align-center">
      <v-toolbar-title
        class="font-weight-light hidden-xs-only"
        v-text="title"
      />

      <v-spacer />

      <v-btn
        v-for="(item, i) in items"
        :key="i"
        :to="item.to"
        min-height="48"
        min-width="40"
        text
      >
        <v-icon
          :left="$vuetify.breakpoint.mdAndUp"
          size="20"
          v-text="item.icon"
        />

        <span
          class="hidden-sm-and-down"
          v-text="item.text"
        />
      </v-btn>
    </v-container>
  </v-app-bar>
</template>

<script>
  export default {
    name: 'PagesCoreAppBar',

    data: () => ({
      items: [
        {
          icon: 'mdi-view-dashboard',
          text: 'Dashboard',
          to: '/',
        },
        {
          icon: 'mdi-currency-usd',
          text: 'Pricing',
          to: '/pages/pricing',
        },
        {
          icon: 'mdi-account-multiple-plus',
          text: 'Register',
          to: '/pages/register',
        },
        {
          icon: 'mdi-fingerprint',
          text: 'Login',
          to: '/pages/login',
        },
        {
          icon: 'mdi-lock-open-outline',
          text: 'Lock',
          to: '/pages/lock',
        },
      ],
      titles: {
        '/pages/lock': 'Lock Page',
        '/pages/login': 'Login Page',
        '/pages/pricing': 'Pricing Page',
        '/pages/register': 'Register Page',
      },
    }),

    computed: {
      title () {
        return this.titles[this.$route.path]
      },
    },
  }
</script>
