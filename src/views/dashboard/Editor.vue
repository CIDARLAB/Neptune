<template>
  <v-container fill-height fluid grid-list-xl>
    <v-layout justify-center wrap>
      <v-flex xs12 md8>
        <material-card color="green">
          <div slot="header">
            <div class="title font-weight-light mb-2">Design Editor</div>
            <div class="category font-weight-thin">
              --File Name--
              <v-btn absolute dark fab top right color="pink" v-on:click="createfile">
                <v-icon>mdi-plus</v-icon>
              </v-btn>

              <v-btn
                absolute
                dark
                fab
                top
                right
                color="grey"
                v-on:click="downloadfile"
                style="right: 90px"
              >
                <v-icon>mdi-cloud-download</v-icon>
              </v-btn>
              <v-btn
                absolute
                dark
                fab
                top
                right
                color="red"
                v-on:click="deletefile"
                style="right: 165px"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>

              <v-btn
                absolute
                dark
                fab
                top
                right
                color="blue"
                @click="dialog2 = true"
                style="right: 240px"
              >
                <v-icon>mdi-play-circle</v-icon>
              </v-btn>
              <v-btn
                absolute
                dark
                fab
                top
                right
                color="lime"
                v-on:click="savefile"
                style="right: 315px"
              >
                <v-icon>mdi-content-save</v-icon>
              </v-btn>
            </div>
          </div>

          <MonacoEditor class="editor" v-model="code" language="javascript" />
        </material-card>
      </v-flex>
      <v-flex xs12 md4>
        <VueTerminal :intro="intro" console-sign="$" allow-arbitrary height="5000px" width="500px"></VueTerminal>

          <div>
            <v-dialog v-model="dialog2" max-width="500px">
              <v-card>
                <v-card-title>Compile</v-card-title>
                <v-card-text>
                  <span class="subtitle-2">Compiling:</span>
                  <span class="body-2">{{filename}}</span>
                  <v-select :items="select" label="Select Config File"></v-select>
                </v-card-text>
                <v-card-actions>
                  <v-btn color="primary" text @click="dialog2 = false">Close</v-btn>
                  <v-btn color="primary" text v-on:click="compilefile">Compile</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>      

<script>
import MonacoEditor from "vue-monaco";
import VueTerminal from "vue-terminal-ui";
import axios from "axios"

export default {
  name: "Editor",
  components: {
    MonacoEditor,
    VueTerminal
  },
  data() {
    return {
      filename: "Test File",
      code: "const noop = () => {}",
      fileid: "5e2a2b307be87c80bf1b6de4",
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
  height: 500px;
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
