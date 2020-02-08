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
        v-for="(file, i) in fileobjects" 
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
                @click="downloadfile(file.id)"
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
        fileobjects:[],
        jobobjects: {},
        colouredLine: {
          data: {
            labels: ["'06", "'07", "'08", "'09", "'10", "'11", "'12", "'13", "'14", "'15"],
            series: [
              [275, 500, 290, 55, 700, 700, 500, 750, 630, 900, 930],
            ],
          },
          options: {
            low: 0,
            high: 1000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
            chartPadding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
            },
          },
        },
        dailySalesChart: {
          data: {
            labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
            series: [
              [12, 17, 7, 17, 23, 18, 38],
            ],
          },
          options: {
            low: 0,
            high: 50, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
            chartPadding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
            },
            showPoint: false,
          },
        },
        dataCompletedTasksChart: {
          data: {
            labels: ['12am', '3pm', '6pm', '9pm', '12pm', '3am', '6am', '9am'],
            series: [
              [230, 750, 450, 300, 280, 240, 200, 190],
            ],
          },
          options: {
            low: 0,
            high: 1000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
            chartPadding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
            },
          },
        },
        emailsSubscriptionChart: {
          data: {
            labels: ['Ja', 'Fe', 'Ma', 'Ap', 'Mai', 'Ju', 'Jul', 'Au', 'Se', 'Oc', 'No', 'De'],
            series: [
              [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],

            ],
          },
          options: {
            lineSmooth: this.$chartist.Interpolation.none(),
            axisX: {
              showGrid: false,
            },
            low: 0,
            high: 1000,
            chartPadding: {
              top: 0,
              right: 5,
              bottom: 0,
              left: 0,
            },
          },
          responsiveOptions: [
            ['screen and (max-width: 640px)', {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function (value) {
                  return value[0]
                },
              },
            }],
          ],
        },
        multipleBar: {
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            series: [
              [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],
              [400, 200, 250, 575, 450, 300, 285, 370, 370, 410, 620, 690],
            ],
          },
          options: {
            seriesBarDistance: 10,
            lineSmooth: this.$chartist.Interpolation.none(),
            axisX: {
              showGrid: false,
            },
            low: 0,
            high: 900,
            chartPadding: {
              top: 0,
              right: 5,
              bottom: 0,
              left: 0,
            },
          },
          responsiveOptions: [
            ['screen and (max-width: 640px)', {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function (value) {
                  return value[0]
                },
              },
            }],
          ],
        },
        multipleLine: {
          data: {
            labels: ["'06", "'07", "'08", "'09", "'10", "'11", "'12", "'13", "'14", "'15"],
            series: [
              [275, 500, 290, 55, 700, 700, 500, 750, 630, 900, 930],
              [575, 600, 490, 75, 300, 400, 700, 450, 130, 200, 330],
              [575, 300, 890, 155, 640, 540, 800, 250, 230, 400, 630],
            ],
          },
          options: {
            low: 0,
            high: 1000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
            chartPadding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0,
            },
          },
        },
        pie: {
          data: {
            series: [62, 32, 6],
          },
          options: {
            labelInterpolationFnc: (value) => `${value}%`,
          },
        },
        headers: [
          {
            sortable: false,
            text: 'ID',
            value: 'id',
          },
          {
            sortable: false,
            text: 'Name',
            value: 'name',
          },
          {
            sortable: false,
            text: 'Salary',
            value: 'salary',
            align: 'right',
          },
          {
            sortable: false,
            text: 'Country',
            value: 'country',
            align: 'right',
          },
          {
            sortable: false,
            text: 'City',
            value: 'city',
            align: 'right',
          },
        ],
        items: [
          {
            id: 1,
            name: 'Dakota Rice',
            country: 'Niger',
            city: 'Oud-Tunrhout',
            salary: '$35,738',
          },
          {
            id: 2,
            name: 'Minerva Hooper',
            country: 'Curaçao',
            city: 'Sinaai-Waas',
            salary: '$23,738',
          },
          {
            id: 3,
            name: 'Sage Rodriguez',
            country: 'Netherlands',
            city: 'Overland Park',
            salary: '$56,142',
          },
          {
            id: 4,
            name: 'Philip Chanley',
            country: 'Korea, South',
            city: 'Gloucester',
            salary: '$38,735',
          },
          {
            id: 5,
            name: 'Doris Greene',
            country: 'Malawi',
            city: 'Feldkirchen in Kārnten',
            salary: '$63,542',
          },
        ],
        tabs: 0,
        list: {
          0: false,
          1: false,
          2: false,
        },
      }
    },
    mounted: function(){
      this.getAllJobs()
    },
    methods: {
      downloadfile(fid){

      },
      openpreview(fid){
        alert(fid)
      },
      deletejob (jid){
        alert(jid)
      },
      viewjobfiles(jid){
        this.selectedjobid = jid
        this.fileobjects = []
        for (let fid of this.jobobjects[jid].files){
          axios.get('/api/v1/file', {
            params: {
              id: fid
            }
          })
          .then((response) => {
            console.log(response.data)
            this.fileobjects.push(response.data)
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
