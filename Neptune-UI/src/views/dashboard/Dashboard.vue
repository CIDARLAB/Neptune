<template>
  <v-container
    id="dashboard"
    fluid
    tag="section"
  >
    <v-row>
      <!-- <v-col cols="12">
        <base-material-card
          icon="mdi-earth"
          title="Global Sales by Top Locations"
        >
          <v-row>
            <v-col
              cols="12"
              md="6"
              class="mt-10"
            >
              <v-simple-table
                class="ml-2"
              >
                <tbody>
                  <tr
                    v-for="(sale, i) in sales"
                    :key="i"
                  >
                    <td>
                      <v-img
                        :src="sale.flag"
                        width="18"
                      />
                    </td>
                    <td v-text="sale.country" />
                    <td v-text="sale.salesInM" />
                    <td v-text="((sale.salesInM / totalSales) * 100).toFixed(2) + '%'" />
                  </tr>
                </tbody>
              </v-simple-table>
            </v-col>

            <v-col
              cols="12"
              md="6"
            >
              <v-world-map
                :country-data="countryData"
                high-color="#838383"
                low-color="#BBBBBB"
              />
            </v-col>
          </v-row>
        </base-material-card>
      </v-col> -->
      <!-- <v-col 
        cols="12"
        v-if="selectedworkspace == null"
        >
        <v-card
        >
          
            <!-- <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title class="headline mb-1">Getting Started</v-list-item-title>
              </v-list-item-content>

              <v-list-item-avatar
                tile
                size="64"
              >
              <img
                src="/images/NeptuneLogo.png"
                alt="John"
              >
              </v-list-item-avatar>
            </v-list-item>
            -->
        <!-- <v-card-title>
            <span class="headline mb-1">Getting Started</span>
        </v-card-title>
          <v-card-text>
            <v-row>
            <v-col
              cols="12"
              md="6"
              class="mt-10"
            >
              <iframe width="100%" height="300px" src="https://www.youtube.com/embed/WO4xAA6XlrY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


            </v-col>

            <v-col
              cols="12"
              md="6"
            >
              <img src="/images/neptunedark.png" width="100%" />
              <br />
              <br />
              <br />
              <p>
                Neptune is really cool its a tool that lets you synthesize microfluidic designs from a high level specification system.
              </p>
            </v-col>
          </v-row>

          </v-card-text>
        </v-card>
      </v-col> -->


      <v-col
        cols="12"
      >
        <div
          class="font-weight-light mt-1"
          style="font-size: 25px"
        >
          Workspaces
        </div>
      </v-col>
      <v-col
        cols="12"
        lg="3"
        v-for="(workspace, key, i) in workspaces" 
        :key="i"
      >
        <base-material-workspace-chart-card
          :id="workspace._id"
          hover-reveal
          color="info"
          type="Line"
        >
          <template v-slot:reveal-actions>
            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn
                  v-bind="attrs"
                  color="info"
                  icon
                  v-on="on"
                >
                  <v-icon
                    color="info"
                  >
                    mdi-refresh
                  </v-icon>
                </v-btn>
              </template>

              <span>Refresh</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn
                  v-bind="attrs"
                  light
                  icon
                  v-on="on"
                  v-on:click="selectworkspace(workspace._id)"
                >
                  <v-icon>mdi-view-split-vertical</v-icon>
                </v-btn>
              </template>

              <span>View Files</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn
                  v-bind="attrs"
                  light
                  icon
                  v-on="on"
                  v-on:click="deleteworkspace(workspace._id)"
                >
                  <v-icon color="error">mdi-delete</v-icon>
                </v-btn>
              </template>

              <span>Delete Workspace</span>
            </v-tooltip>
          </template>

          <h3 class="card-title font-weight-light mt-2 ml-2">
            {{workspace.name}}
          </h3>
          <template v-slot:actions>
            <v-icon
              class="mr-1"
              small
            >
              mdi-clock-outline
            </v-icon>
            <span class="caption grey--text font-weight-light">Last Update: {{formattimestamp(workspace.updated_at)}}</span>
          </template>
        </base-material-workspace-chart-card>
      </v-col>

        <v-col
            cols="12"
            sm="3"
            lg="3"
            align="center"
        >
            <div class="my-2">
            <v-tooltip top>
                <template v-slot:activator="{ on }">
                <v-btn 
                    v-on="on" 
                    class="newbutton" 
                    color="success" 
                    fab 
                    x-large 
                    dark
                    @click="newworkspacedialog = true"
                    >
                    <v-icon>mdi-plus</v-icon>
                </v-btn>
                </template>
                <span>Create New Workspace</span>
            </v-tooltip>
                <v-dialog
                    v-model="newworkspacedialog"
                    max-width="300px"
                    >
                    <v-card>
                    <v-card-title>
                        Create New Workspace
                    </v-card-title>
                    <v-card-text>
                        <v-text-field
                            v-model="newworkspacename"
                            label="Workspace Name"
                            ></v-text-field>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="success"
                            text
                            @click="createworkspace()"
                            >
                            Create
                        </v-btn>

                        <v-btn
                            color="primary"
                            text
                            @click="newworkspacedialog = false"
                            >
                            Cancel
                        </v-btn>

                    </v-card-actions>
                    </v-card>
                </v-dialog>


            </div>
        </v-col>

    </v-row>
            <v-row
                v-if="files.length > 0"
                >
                <v-col
                    cols="12"
                    
                >
                    <div
                    class="font-weight-light mt-1"
                    style="font-size: 25px"
                    >
                    Files
                    </div>
                </v-col>
                <v-col
                    cols="12"
                    sm="3"
                    lg="3"
                    v-for="(file, i) in files" :key="i"
                >
                    <base-material-workspace-stats-card
                        color="info"
                        icon="mdi-file"
                        title="File Type:"
                        :value="file.ext"
                        :name="file.name"
                        sub-icon="mdi-clockwise-outline"
                        :sub-text=" 'Modified: ' + formattimestamp(file.updated_at)"
                        :id="file.id"
                        :workspaceid="selectedworkspace._id"
                        v-on:onFileDeleted="refreshFiles"
                    />
                </v-col>
                <v-col
                    cols="12"
                    sm="3"
                    lg="3"
                    v-if="files.length > 0"
                    align="center"
                >
                    <div class="my-2">
                    <v-tooltip top>
                        <template v-slot:activator="{ on }">
                        <v-btn 
                            v-on="on" 
                            class="newbutton" 
                            color="success" 
                            fab 
                            x-large 
                            dark
                            @click="newfiledialog = true"
                            >
                            <v-icon>mdi-plus</v-icon>
                        </v-btn>
                        </template>
                        <span>Create New File</span>
                    </v-tooltip>
                                    <v-dialog
                    v-model="newfiledialog"
                    max-width="300px"
                    >
                    <v-card>
                    <v-card-title>
                        Create New File
                    </v-card-title>
                    <v-card-text>
                        <v-text-field
                            v-model="newfilename"
                            label="File Name"
                            :rules="rules"
                            hide-details="auto"
                            ></v-text-field>
                        <v-select
                          v-model="extname"
                          :items="exts"
                          label="Extension Name"
                          :rules="rules"
                        />
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="success"
                            text
                            @click="createfile()"
                            >
                            Create
                        </v-btn>

                        <v-btn
                            color="primary"
                            text
                            @click="newfiledialog = false"
                            >
                            Cancel
                        </v-btn>

                    </v-card-actions>
                    </v-card>
                </v-dialog>

            </div>
        </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios'
  import { log } from 'util'
  import * as Utils from '../../utils'

  export default {
    name: 'DashboardDashboard',

    mounted: async function() {
        // console.log('Selected Workspace:', this.selectedworkspace, currentworkspace)
        // console.log(this.$store.getters.userID)
        this.refreshworkspacedata()
    },
    data: () => ({
      // set rules for the file extension
      rules: [
        value => !!value || 'Required',
      ],
        newworkspacename: '',
        newworkspacedialog: false,
        newfilename: '',
        extname: '',
        newfiledialog: false,
        selectedworkspace: {
            name: '',
            id: '',
        },          
        files: [],
        workspaces:[],
        workspacesobjects: {},
        actions: [
            {
            color: 'info',
            icon: 'mdi-account',
            },
            {
            color: 'success',
            icon: 'mdi-pencil',
            },
            {
            color: 'error',
            icon: 'mdi-close',
            },
        ],
        exts: ['.mint', '.lfr']
    }),
    computed: {
      totalSales () {
        return this.sales.reduce((acc, val) => acc + val.salesInM, 0)
      },
    },

    methods: {
      formattimestamp(datestring){
        return Utils.getprettytimestamp(datestring)
      },
        refreshworkspacedata(){
          this.workspaces = []
          this.workspacesobjects = {}
          this.files =[]
          this.workspacesobjects = {}
          let data = { 
            user: { 
            _id: this.$store.getters.userID
            }
        } 
        
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

        axios.get('/api/v2/user', config)
          .then((response) => {
            console.log('User info:', response.data)
            this.$store.commit('SET_CURRENT_USER', response.data)
          })
          .catch((error) => {
            console.error(error)
          })

        axios.get('/api/v1/workspaces', config)
            .then((response)=>{
                console.log(response)
                console.log("TEST:", this.workspaces)
                for (let wid of response.data){
                    console.log(wid)
                    axios.get('/api/v1/workspace',{
                    params: {
                        workspace_id: wid
                    }}).then((response)=>{
                        console.log(response.data)
                        this.workspaces.push(response.data)
                        this.workspacesobjects[response.data._id] = (response.data)

                        if (this.$store.getters.currentWorkspace != null && this.$store.getters.currentWorkspace != undefined){
                            console.log(" current workspace",this.$store.getters.currentWorkspace, this.selectedworkspace)
                            this.selectworkspace(this.$store.getters.currentWorkspace._id)
                        }

                    })
                    .catch((error)=>{console.log(error)})
                }

                console.log(this.workspaces)

            })
            .catch((error)=>{
            console.log(error)
            });

        },
        deleteworkspace (wid){
            console.log(wid)
            const config = {
                data: {
                    id: wid
                },
                withCredentials: true,
                crossorigin: true,
                headers: { 'Content-Type': 'application/json' },
            }

            axios.delete('/api/v1/workspace', config)
                .then((response)=>{
                    console.log("Delete Data",response)
                    this.refreshworkspacedata()
                    console.log("Selected workspace:", this.selectworkspace.id)
                    this.selectworkspace(this.selectedworkspace.id)
                })
                .catch((error)=>{ console.log(error) })
        },

        createworkspace() {
            const config = {
                withCredentials: true,
                crossorigin: true,
                headers: { 'Content-Type': 'application/json' },
                name: this.newworkspacename,
            }
            console.log(config)
             axios.post('/api/v1/workspace', config)
                .then((response) => {
                    console.log("Created new file", response)
                    this.refreshworkspacedata()
                })
                .catch((errors) => {
                    console.log("Could not create file:", errors)
                })
            this.newworkspacedialog = false
        },
        createfile() {
            const config = {
                withCredentials: true,
                crossorigin: true,
                headers: { 'Content-Type': 'application/json' },
                file_name: this.newfilename + this.extname,
                ext: this.extname.match(/\.[0-9a-z]+$/i)[0],
                workspaceid: this.$store.getters.currentWorkspace
            }
            console.log(config)
            axios.post('/api/v1/file', config)
                .then((response) => {
                    console.log("Created new file", response)
                    this.refreshworkspacedata()
                })
                .catch((errors) => {
                    console.log("Could not create file:", errors)
                })
            this.newfiledialog = false
        },
        complete (index) {
            this.list[index] = !this.list[index]
        },

        refreshFiles(id){
          console.log("Refreshing Files", this.selectedworkspace.id)
          this.selectworkspace(id)
        },
        selectworkspace(workspace_id){
            let self = this
            console.log("Select workspace event",workspace_id)
            this.selectedworkspace = this.workspacesobjects[workspace_id]
            const config = {
                withCredentials: true,
                crossorigin: true,
                headers: { 'Content-Type': 'application/json' },
            }
            console.log("Setting workspace", workspace_id)
            let obj = this.workspacesobjects[workspace_id]
            if (obj != null && obj != undefined){
              this.$store.commit('SET_WORKSPACE', obj)
            }
            // alert("TEST")
            axios.get('/api/v1/files',{
                params: {
                    id: workspace_id
                }})
                .then((response)=>{
                    console.log("File Data",response.data)
                    self.files=[]
                    for(let f of response.data){
                        axios.get('/api/v1/file',{
                            params: {
                                id: f
                            }})
                            .then((response)=>{
                                console.log(response.data)
                                this.files.push(response.data)
                                console.log("File Data",this.files)
                            })
                            .catch((error)=>{console.log(error)})
                    }
                })
                .catch((error)=>{ console.log(error) })
            
            }
    },

  }
</script>
<style>
    .newbutton{
        margin-top: 85px;
    }
</style>