<template>
  <v-container
    id="login"
    class="fill-height justify-center"
    tag="section"
  >
    <v-row justify="center">
      <v-slide-y-transition appear>
        <base-material-card
          color="success"
          light
          max-width="100%"
          width="400"
          class="px-5 py-3"
        >
          <template v-slot:heading>
            <div class="text-center">
              <h1 class="display-2 font-weight-bold mb-2">
                Login
              </h1>
              <!-- <v-btn
                v-for="(social, i) in socials"
                :key="i"
                :href="social.href"
                class="ma-1"
                icon
                rel="noopener"
                target="_blank"
              >
                <v-icon
                  v-text="social.icon"
                />
              </v-btn> -->
            </div>
          </template>

          <v-card-text class="text-center">
            <div class="text-center grey--text body-1 font-weight-light">
              Or <a href="./register"> Register </a>
            </div>

            <v-text-field
              color="secondary"
              label="Email..."
              prepend-icon="mdi-email"
            />

            <v-text-field
              class="mb-8"
              color="secondary"
              label="Password..."
              prepend-icon="mdi-lock-outline"
              type="password"
            />

            <pages-btn
              large
              color=""
              depressed
              class="v-btn--text success--text"
              v-on:click="login"
            >
              Let's Go
            </pages-btn>
          </v-card-text>
        </base-material-card>
      </v-slide-y-transition>
    </v-row>
  </v-container>
</template>

<script>
  import router from '../../router'
  import axios from 'axios'
  export default {
    name: 'PagesLogin',

    components: {
      PagesBtn: () => import('./components/Btn'),
    },

    data: () => ({
      email: 'rkrishnasanka@gmail.com',
      password: 'potter',
    }),

    methods: {
      login: function(event) {
        event.preventDefault()
        console.log(this.email, this.password)
        // let email = "rkrishnasanka@gmail.com"   
        // let password = "potter"

        let data = {    
            email: this.email,    
            password: this.password    
        }
        let self = this

        axios.post("/api/v2/login", data)    
            .then((response) => {    
                console.log("Logged in",response)
                self.$store.commit('updateUser', response.data.user)    
                router.push("/dashboard")
                console.log("Testing store access2", self.$store.getters.isLoggedIn)

            })    
            .catch((errors) => {    
                console.log("Cannot log in", errors)    
            })    
      }
    }
  }
</script>
