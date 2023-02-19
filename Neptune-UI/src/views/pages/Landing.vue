<template>
  <v-container
    id="login"
    class="fill-height justify-center"
    tag="section"
  >
    <v-row justify="center">
      <v-slide-y-transition appear>
        <v-img
          :src="require(`@/assets/Neptune-logo-white-text.png`)"
          height="300px"
          />
      </v-slide-y-transition>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: '',

    components: {
      // PagesBtn: () => import('./components/Btn'),
    },
    data: () => ({
      socials: [
        {
          href: '#',
          icon: 'mdi-facebook-box',
        },
        {
          href: '#',
          icon: 'mdi-twitter',
        },
        {
          href: '#',
          icon: 'mdi-github-box',
        },
      ],
    }),
    mounted () {
      console.log('Landing.vue mounted hook')
      this.$socket.client.emit('echo', 'Hello World!')
    },
    sockets: {
      connect () {
        console.log('socket connected')
      },
      echo (val) {
        console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)')
        console.log(val)
      },
    },
    methods:{
      login: function(event){
        console.log("TEST")
      }
    }
  }
</script>
