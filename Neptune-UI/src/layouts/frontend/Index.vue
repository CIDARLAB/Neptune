<template>
  <v-app>
    <frontend-view />
  </v-app>
</template>

<script>
  export default {
    name: 'LayoutsFrontend',

    components: {
      FrontendView: () => import('./View'),
    },
  }
</script>
