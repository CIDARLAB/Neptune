<template>
  <base-material-card
    :icon="icon"
    class="v-card--material-stats"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <template v-slot:after-heading>
      <div class="ml-auto text-right">
        <div
          class="body-3 grey--text font-weight-light"
          v-text="title"
        />

        <h3 class="display-2 font-weight-light text--primary">
          {{ value }} <small>{{ smallValue }}</small>
        </h3>
      </div>
    </template>
    
    <v-col
      cols="12"
      class="px-0"
    >
      <span
        class="body-3 grey--text font-weight-light"
        >
      </span> 
      <span class="text--darken-4"> {{ name }} </span>
      <v-btn 
        text 
        icon 
        color="blue"
        @click="editfile(id)"
        >
          <v-icon>mdi-pen</v-icon>
      </v-btn>
      <v-btn 
        text 
        icon 
        color="red"
        @click="deletefile(id)"
        >
          <v-icon>mdi-delete</v-icon>
      </v-btn>
      <v-divider />
    </v-col>

    <v-icon
      class="mr-1"
      small
    >
      <!-- {{ subIcon }} -->
      mdi-clockwise
    </v-icon>

    <span
      :class="subTextColor"
      class="caption grey--text font-weight-light"
      v-text="subText"
    />
  </base-material-card>
</template>

<script>
  import Card from './Card'
  import axios from 'axios'
  import router from '../../router'

  export default {
    name: 'MaterialStatsCard',

    inheritAttrs: false,

    props: {
      ...Card.props,
      icon: {
        type: String,
        required: true,
      },
      subIcon: {
        type: String,
        default: undefined,
      },
      subIconColor: {
        type: String,
        default: undefined,
      },
      subTextColor: {
        type: String,
        default: undefined,
      },
      subText: {
        type: String,
        default: undefined,
      },
      title: {
        type: String,
        default: undefined,
      },
      value: {
        type: String,
        default: undefined,
      },
      smallValue: {
        type: String,
        default: undefined,
      },
      name: {
        type: String,
        default: undefined,
      },
      id: {
        type: String,
        default: undefined
      },
      workspaceid: {
        type: String,
        default: undefined
      },
    },

    methods: {
      deletefile(fid){
        console.log(fid, this.id, this.$store.getters.currentWorkspace)
        let wid = this.$store.getters.currentWorkspace
        const config = {
          data: {
            fileid: fid,
            workspaceid: wid
          },
          withCredentials: true,
          crossorigin: true,
          headers: { 'Content-Type': 'application/json' },
        }

        axios.delete('/api/v1/file', config)
              .then((response)=>{
                console.log("Delete Data",response)
              })
              .catch((error)=>{ console.log(error) })
      },
      editfile(id){
        console.log("edit:",id)
        this.$store.commit('SET_CURRENT_FILE', id)
        router.push('/editor')
      }
    }
  }
</script>

<style lang="sass">
.v-card--material-stats
  display: flex
  flex-wrap: wrap
  position: relative

  > div:first-child
    justify-content: space-between

  .v-card
    border-radius: 4px
    flex: 0 1 auto

  .v-card__text
    display: inline-block
    flex: 1 0 calc(100% - 120px)
    position: absolute
    top: 0
    right: 0
    width: 100%

  .v-card__actions
    flex: 1 0 100%
</style>
