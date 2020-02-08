<template>
  <v-container fluid>
    <v-row>
      <v-col
        cols="12"
        lg="12"
      >

    <base-material-card
      color="success"
      icon="mdi-clipboard-text"
      inline
      title="Jobs"
      class="px-5 py-3 mb-5"
    >
      <v-simple-table
        height="300px"
      >
        <thead>
          <tr>
            <th>Name</th>
            <th>Last Updated</th>
            <th># Files</th>
            <th class="text-right">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>


          <tr
            v-for="(job, ijk) in jobs" 
            :key="ijk"
          >
            <td>{{ job.name }}</td>
            <td>{{ job.created_at }}</td>
            <td>{{ job.files.length }}</td>
            <td class="text-right">
              <v-btn
                color="green"
                class="ml-1"
                fab
                icon
                x-small
                @click="downloadjobfiles(job.id)"
              >
                <v-icon
                  small
                >
                mdi-download
              </v-icon>
              </v-btn>
              <v-btn
                color="blue"
                class="ml-1"
                fab
                icon
                x-small
                @click="viewjobfiles(job.id)"
              >
                <v-icon
                  small
                >
                mdi-view-split-vertical
                </v-icon>
              </v-btn>
              <v-btn
                color="red"
                class="ml-1"
                fab
                icon
                x-small
                @click="deletejob(job.id)"
              >
                <v-icon
                  small
                >
                mdi-delete
                </v-icon>
              </v-btn>

            </td>
          </tr>

        </tbody>
      </v-simple-table>
    </base-material-card>

      </v-col>
      
      <v-col
        col="12"
        sm="5"
        v-for="(file, i) in files" 
        :key="i"
        >
        <base-material-card
          color="success"
          icon="mdi-file"
          :title="file.name"
          class="px-4 py-3"
        >
          <v-divider class="ma-3" />

          <div class="px-3">
            <div class="body-2 text-uppercase grey--text font-weight-bold mb-3">
              Actions
            </div>

            <v-row
              align="center"
              class="ma-0"
            >
              <v-btn
                color="green"
                class="ml-1"
                fab
                icon
                x-small
                @click="downloadfile(file)"
              >
                <v-icon
                  small
                >
                mdi-download
              </v-icon>
              </v-btn>
              <v-btn
                color="blue"
                class="ml-1"
                fab
                icon
                x-small
                @click="openpreview(file.id)"
              >
                <v-icon
                  small
                >
                mdi-open-in-new
                </v-icon>
              </v-btn>
            </v-row>
          </div>
        </base-material-card>

      </v-col>

    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios'
  
  export default {
    data () {
      return {
        selectedjobid: '',
        jobs : [],
        files:[],
        jobobjects: {},
      }
    },
    mounted: function(){
      this.getAllJobs()
    },
    methods: {
      downloadfile(file){
        var fileurl = new URL("/api/v1/downloadFile?id=" + file.id, document.baseURI);
        console.log('downloading file: ',file.id);
        // window.open(fileurl, '_blank');
        let self = this
        axios({
          method: 'get',
          url: fileurl,
          responseType: 'arraybuffer'
        })
          .then(function(response) {
            //response.data.pipe(fs.createWriteStream('ada_lovelace.jpg'))
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', file.name) //or any other extension
            document.body.appendChild(link)
            link.click()
        })

      },
      openpreview(fid){
        alert(fid)
      },
      deletejob (jid){
        alert(jid)
      },
      viewjobfiles(jid){
        this.selectedjobid = jid
        this.files = []
        for (let fid of this.jobobjects[jid].files){
          axios.get('/api/v1/file', {
            params: {
              id: fid
            }
          })
          .then((response) => {
            console.log(response.data)
            this.files.push(response.data)
          })
          .catch((error) => {
            console.log(error)
          })

        }
      },
      downloadjobfiles(jid){
        alert(jid)
      },
      complete (index) {
        this.list[index] = !this.list[index]
      },
      getAllJobs () {
            // $.get('/api/v1/jobs',function (response) {
            //     self.jobIDs.removeAll();
            //     self.jobs.removeAll();
            //     for(var i = 0 ; i<response.length;i++){
            //         self.addJob(response[i]);
            //         self.jobIDs.push(response[i]);
            //     }
            //     console.log("Jobs Found:", self.jobIDs());
            // })
        let config = {
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

        let self = this
        axios.get('/api/v1/jobs', config)
          .then((response)=>{
            console.log(response.data)
            self.jobs = []
            self.jobobjects = {}
            for (let jobid of response.data){
              axios.get('/api/v1/job', {
                params: {
                  job_id: jobid
                }
              })
              .then((response)=>{
                console.log(response.data)
                self.jobs.push(response.data)
                self.jobobjects[response.data.id] = response.data
              })
              .catch((error) => {
                console.log(error)
              })
            }
          }).catch((error) => {
            console.log(error)
          })

      }
    },
  }
</script>

<style lang="sass">
  #coloured-line
    .ct-series-a .ct-line,
    .ct-series-a .ct-point
      stroke: #00cae3 !important

  #multiple-bar
    .ct-series-a .ct-bar
      stroke: #00cae3 !important

    .ct-series-b .ct-bar
      stroke: #f44336 !important

  #pie
    .ct-series-a .ct-slice-pie
      fill: #00cae3 !important

    .ct-series-b .ct-slice-pie
      fill: #f44336 !important
</style>
