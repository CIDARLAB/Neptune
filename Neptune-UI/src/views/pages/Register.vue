<template>
  <v-container
    id="register"
    class="fill-height justify-center"
    tag="section"
  >
    <v-row justify="center">
      <v-col
        cols="12"
        md="9"
      >
        <v-slide-y-transition appear>
          <v-card
            class="pa-3 pa-md-5 mx-auto"
            light
          >
            <pages-heading class="text-center display-3">
              Register
            </pages-heading>

            <v-row>
              <v-col
                cols="12"
                md="6"
              >
                <v-row no-gutters>
                  <v-col
                    v-for="(section, i) in sections"
                    :key="i"
                    cols="12"
                  >
                    <v-list-item three-line>
                      <v-list-item-icon class="mr-4 mt-5 mt-md-4">
                        <v-icon
                          :large="$vuetify.breakpoint.mdAndUp"
                          :color="section.iconColor"
                          v-text="section.icon"
                        />
                      </v-list-item-icon>

                      <v-list-item-content>
                        <v-list-item-title
                          class="font-weight-light mb-4 mt-3"
                          v-text="section.title"
                        />

                        <v-list-item-subtitle v-text="section.text" />
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                </v-row>
              </v-col>

              <v-col
                cols="12"
                md="6"
              >
                  <v-alert
                    v-if="alertmessage!=''"
                    type="error">
                    {{ alertmessage }}
                  </v-alert>

                <div class="text-center">

                  <div class="my-2" />

                  <div class="text-center grey--text body-1 font-weight-light">
                    Sign up here...
                  </div>


                  <v-text-field
                    color="primary"
                    label="Email..."
                    prepend-icon="mdi-email"
                    v-model="email"
                  />

                  <v-text-field
                    class="mb-8"
                    color="secondary"
                    label="Password..."
                    prepend-icon="mdi-lock-outline"
                    type="password"
                    v-model="password"
                  />

                  <v-text-field
                    class="mb-8"
                    color="secondary"
                    label="Repeat Password..."
                    prepend-icon="mdi-lock-outline"
                    type="password"
                    v-model="repeat_password"
                  />

                  <v-checkbox
                    :input-value="true"
                    color="secondary"
                  >
                    <template v-slot:label>
                      <span class="text-no-wrap">I agree to the&nbsp;</span>

                      <a
                        class="secondary--text ml-6 ml-sm-0"
                        href="#"
                      >
                        terms and conditions
                      </a>.
                    </template>
                  </v-checkbox>

                  <pages-btn color="success" @click="registerUser">
                    Get Started
                  </pages-btn>
                </div>
              </v-col>
            </v-row>
          </v-card>
        </v-slide-y-transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
    import axios from 'axios'
    import router from '../../router'
    export default {
        name: 'PagesRegister',

        components: {
        PagesBtn: () => import('./components/Btn'),
        PagesHeading: () => import('./components/Heading'),
        },

        data: () => ({
        email: '',
        password: '',
        repeat_password: '',
        alertmessage: '',
        sections: [
            {
            icon: 'mdi-code-tags',
            iconColor: 'primary',
            title: 'Open Source',
            text: 'Source code available at https://github.com/CIDARLAB',
            },
            {
            icon: 'mdi-code-tags',
            iconColor: 'secondary',
            title: 'Automated Design Generation',
            text: 'Create devices sytematically using the automated tools',
            },
        ],
        }),

        methods:{
        registerUser: function(){
            //Check if the passwords match
            if(this.password !== this.repeat_password){
            this.alertmessage = 'Passwords do not match'
            return
            }

            //Since the passwords are correct, we are going to post the registration
            axios.post('/api/v2/register', {
                'email': this.email,
                'password': this.password
            })
            .then(response => {
                console.log(response)
                //TODO: If successful create the user and forward the person the login sreen
                this.$store.commit('updateUser', response.data.user)
                this.$router.push('/dashboard')
            })
            .catch(e => {
                console.error(e.message)
                this.alertmessage = e.message
            })
        }
        }
    }
</script>

<style lang="sass">
  #register
    .v-list-item__subtitle
      -webkic-line-clamp: initial
      -webkit-box-orient: initial
</style>
