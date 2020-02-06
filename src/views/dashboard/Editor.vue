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
        <v-btn color="info" v-on:click="compilefile"><v-icon small left light>mdi-play</v-icon> Compile</v-btn>
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
              <v-list-item-title class="headline mb-1">Filename</v-list-item-title>
              <v-list-item-subtitle>Workspace Job ID</v-list-item-subtitle>
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

  </v-container>

</template>      

<script>
import MonacoEditor from "vue-monaco";
import VueTerminal from "vue-terminal-ui";
import axios from "axios"
import { Terminal } from 'xterm';

export default {
  name: "Editor",
  components: {
    MonacoEditor,
    VueTerminal,
  },
  mounted: function() {
    var term = new Terminal();
    term.open(document.getElementById('terminal'));
    term.write('Neptune Console $ ')


    let currentfile = this.$store.getters.currentFile
    if (currentfile == null || currentfile === ''){
      return
    }
    console.log("Opened the editor: ", currentfile)
    const config = {
        withCredentials: true,
        crossorigin: true,
        headers: { 'Content-Type': 'application/json' },
        params: {
          id: currentfile
        }
    }

    axios.get('/api/v1/fs', config)
      .then((response) => {
        console.log(response)
        this.code = JSON.stringify(response.data)
      })
      .error((error) => {
        console.log(error)
      })
  },
  data() {
    return {
      filename: "Test File",
      code: '',
      fileid: '',
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
  methods: {
    createfile: function(event) {
      console.log("TEST");
    },
    savefile: function(event) {
      console.log("save the file", this.code);
      console.log(this.$store.getters.userID)

      const config = {
        withCredentials: true,
        crossorigin: true,
        headers: { 'Content-Type': 'application/json' },
      }
      let data = {
        fileid: currentfile._id,
        name: currentfile._id,
        body: code,
      }

      // console.log("fileid: " + req.body.fileid);
      // console.log("name: " + req.body.name);
      // console.log("name: " + req.body.text);

      axios.put('/api/v1/file', config, data)
        .then((response) => {
          console.log(response)
        })
        .error((error) => {
          console.log(error)
        })

    },
    compilefile: function(event) {
      console.log("compile the file");
      this.dialog2 = false;
    },
    deletefile: function(event) {
      console.log("delete the file");
      axios.get("/api/v1/workspaces")
        .then((response)=>{
          console.log(response)
        })
    },
    downloadfile: function(event) {
      console.log("download the file");
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
