<template>
  <v-container
    id="grid"
    fluid
    tag="section"
  >
    <v-row>

      <v-col
        cols="12"
        sm="9"
        class="pt-0"
      >
        <v-btn color="success" v-on:click="savefile"><v-icon small left light>mdi-content-save</v-icon> Save</v-btn>
        <v-btn color="info" @click="compiledialog = true"><v-icon small left light>mdi-play</v-icon> Compile</v-btn>
        <v-btn color="error" v-on:click="deletefile"><v-icon small left light>mdi-delete</v-icon> Delete</v-btn>
        <v-btn color="secondary" v-on:click="downloadfile"><v-icon small left light>mdi-cloud-download</v-icon> Download</v-btn>
        <v-btn color="secondary" v-on:click="createfile"><v-icon small left light>mdi-cloud-upload</v-icon> Upload</v-btn>
            
      </v-col>
    </v-row>

    <v-row>

      <v-col
        cols="12"
        sm="8"
        class="pt-0"
      >
        <v-card class="mt-0">
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1" > <span v-text="fileobject.name"></span> </v-list-item-title>
              <v-list-item-subtitle>Workspace: <span v-text="currentworkspace.name"></span></v-list-item-subtitle>
            </v-list-item-content>

            <!-- <v-list-item-avatar
              tile
              size="80"
              color="grey"
            ></v-list-item-avatar> -->
          </v-list-item>

          <v-card-text class="red--text text--darken-4">
            <MonacoEditor class="editor" v-model="code" language="javascript" />
          </v-card-text>
        </v-card>

      </v-col>
      <v-col
        cols="12"
        sm="4"
        class="pt-0"
      >
        <v-card class="mt-0">
          <v-card-text class="red--text text--darken-4">
            <div id="terminal"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  <v-dialog
          v-model="compiledialog"
          max-width="500px"
        >
        <v-card>
          <v-card-title>
            Compile
          </v-card-title>
          <v-card-text>
            <v-select
              :items="configfiles"
              label="Select Confg File"
              item-value="id"
              item-text="name"
              v-model="selectedconfig"
              :return-object="true"
            ></v-select>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              text
              @click="compiledialog = false"
            >
              Close
            </v-btn>
            <v-btn
              color="info"
              text
              @click="compilefile"
            >
              Compile
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

  </v-container>

</template>      

<script>
import MonacoEditor from 'vue-monaco'
import VueTerminal from 'vue-terminal-ui'
import axios from 'axios'
import { Terminal } from 'xterm'
import router from '../../router'

const term = new Terminal();

export default {
  name: "Editor",
  components: {
    MonacoEditor,
    VueTerminal,
  },
  mounted: function() {
    term.open(document.getElementById('terminal'))
    term.setOption('fontSize', 10 )
   
    // setOption(key: 'fontSize' | 'letterSpacing' | 'lineHeight' | 'tabStopWidth' | 'scrollback', value: number): void; 

    term.writeln('Neptune Console $\n')
    let currentfile = this.$store.getters.currentFile
    this.currentworkspace = this.$store.getters.currentWorkspace
    console.log("Currnet workspace:",this.currentworkspace,this.currentworkspace._id )
    if (currentfile == null || currentfile === ''){
      return
    }
    console.log("Opened the editor: ", currentfile)

    let config = {
        withCredentials: true,
        crossorigin: true,
        headers: { 'Content-Type': 'application/json' },
        params: {
          id: currentfile
        }
    }
    axios.get('/api/v1/file',{
        params: {
            id: currentfile
        }})
        .then((response)=>{
            console.log(response.data)
            this.fileobject = (response.data)
        })
        .catch((error)=>{console.log(error)})

    
    axios.get('/api/v1/fs',{
      params: {
          id: currentfile
      }})
      .then((response)=>{
          console.log(response.data)
          if (typeof response.data !== 'string'){
            alert('Cannot open file in default editor')
            //this.code = response.data
          }else{
            this.code = response.data
          }
      })
      .catch((error)=>{console.log(error)})
           
            
    this.downloadconfigfiles()
    // axios.get('/api/v1/fs', config)
    //   .then((response) => {
    //     console.log(response)
    //     this.code = JSON.stringify(response.data)
    //   })
    //   .error((error) => {
    //     console.log(error)
    //   })
  },
  data() {
    return {
      selectedconfig: '',
      compiledialog: false,
      currentworkspace: {
        name:''
      },
      code: '',
      fileobject: {
        name: '',
        id: ''
      },
      configfiles: [],
      dialog: false,
      dialog2: false,
      dialog3: false,
      notifications: false,
      sound: true,
      widgets: false,
      select: [
        "State 1",
        "State 2",
        "State 3",
        "State 4",
        "State 5",
        "State 6",
        "State 7"
      ]
    };
  },
  sockets: {
    // //This signals the end of the output
    // socket.on('EOP', function(data){
    //     //TODO: Figure out how to close the monitoring
    //     editorViewModel.updateJobs();
    //     setTimeout(function() {
    //         //self.jobs()[0]
    //         editorViewModel.setAsCurrentJob(editorViewModel.currentJob());
    //     },1000);
    // });
    stdout: function(data){
      //console.log(data)
      term.write(data.replace(/\n/g, '\n\r'))

    },
  
    EOP: function(data){
      console.log(data)
    }

  },
  methods: {
    downloadconfigfiles: function(event){
      this.configfiles= []
      const config = {
        withCredentials: true,
        crossorigin: true,
        headers: { 'Content-Type': 'application/json' },
        params: {
          id: this.$store.getters.currentWorkspace._id
        }
      }
      let self = this
      axios.get('/api/v1/files', config)
        .then((response) => {
          console.log(response)
          for(let fid of response.data){
            console.log("FID:" , fid)
            const config = {
              withCredentials: true,
              crossorigin: true,
              headers: { 'Content-Type': 'application/json' },
              params: {
                id: fid
              }
            }
            console.log("Config:", config)
            axios.get('/api/v1/file',config)
              .then((response)=>{
                  console.log(response.data)
                  let ext = response.data.ext
                  if( ext === '.ini' || ext === '.json' ){
                    self.configfiles.push(response.data)
                  }
                  
              })
              .catch((error)=>{console.log(error)})

          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    createfile: function(event) {
      console.log("TEST");
    },
    savefile: function(event) {
      console.log("save the file", this.code);
      console.log(this.$store.getters.userID)
      console.log(this.fileobject)
      const config = {
        withCredentials: true,
        crossorigin: true,
        headers: { 'Content-Type': 'application/json' }
      }

      // console.log("fileid: " + req.body.fileid);
      // console.log("name: " + req.body.name);
      // console.log("name: " + req.body.text);

      axios.put('/api/v1/file',{
        fileid: this.fileobject.id,
        name: this.fileobject.name,
        text: this.code,
      }, config)
        .then((response) => {
          console.log(response)
        })
        .catch((error) => {
          console.log(error)
        })

    },
    compilefile: function(event) {
      let self = this
      console.log("compile the file");
      this.compiledialog = false;
      // $.post('/api/v1/fluigi', {
      //             sourcefileid: (self.currentFile()).id,
      //             sourcefilename: (self.currentFile()).name,
      //             configfileid: (self.currentConfigFile()).id,
      //             configfilename: (self.currentConfigFile()).name,
      //             workspace:    (self.currentWorkSpace()).id,
      //             user:          localStorage.Email
      //         },
      //         function(response){
      //             //TODO - Connect to fluigicad's console output based on job id.
      //             console.log("jobid: " + response);
      //             socket.emit('monitor', response);
      //             NProgress.done();
      //             //self.setAsCurrentWorkSpace(self.currentWorkSpace());
      //         });
      const config = {
        withCredentials: true,
        crossorigin: true,
        headers: { 'Content-Type': 'application/json' }
      }

      console.log("Selected config",this.$store.getters.currentWorkspace)
      let data = {
        sourcefileid: this.fileobject.id,   //(self.currentFile()).id,
        sourcefilename: this.fileobject.name,   //(self.currentFile()).name,
        configfileid: this.selectedconfig.id,   //(self.currentConfigFile()).id,
        configfilename: this.selectedconfig.name,   //(self.currentConfigFile()).name,
        workspace:    this.$store.getters.currentWorkspace._id,
        user: this.$store.getters.currentUser.email,           //localStorage.Email
      }

      axios.post('/api/v1/fluigi', data, config)
        .then((response) => {
          console.log('Jobid:', response.data)
          let jobid = response.data
          self.$socket.emit('monitor', jobid)
        })
        .catch((error) => {
          console.error(error)
        })

      //we get jobid from the response
      
    },
    deletefile: function(event) {
        let fid = this.fileobject.id
        let wid = this.$store.getters.currentWorkspace._id
        console.log(fid, wid)
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
                router.push('/dashboard')
              })
              .catch((error)=>{ console.log(error) })

    },
    downloadfile: function(event) {
      console.log("download the file");
      var fileurl = new URL("/api/v1/downloadFile?id=" + this.fileobject.id, document.baseURI);
      console.log('currentfile: ',this.fileobject.id);
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
          link.setAttribute('download', self.fileobject.name) //or any other extension
          document.body.appendChild(link)
          link.click()
      })
    },
    uploadfile: function(event){
      alert("Feature not yet implemented !")
    }
  }
}
</script>

<style>
.editor {
  height: 385px;
  width: 100%;
}

.terminal {
  width: 300px;
  height: 500px;
}

.fab-container {
  position: fixed;
  bottom: 0;
  right: 0;
}
</style>
