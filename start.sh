#!/bin/sh

redis-server --daemonize yes

cd /var/www/fluigicad.org/
npm start app.js
