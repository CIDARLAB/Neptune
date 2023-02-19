# Development / Debugging Guide

## SocketIO Debugging

The route `<host>:<port>/test/socketio` that renders a page that automatically connects to the socketio server and pings the `echo` event. This basically returns the message that was sent to the server. This returned data is printed to the console (This will need to be changed in the future).

# Job Runner

Async Task Running infrastructure for the fluigi command line tool.



# Getting Started with Dev


## Load the Enviroment Variables

```bash
set -a; source .env; set +a
```