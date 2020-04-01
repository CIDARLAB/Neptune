#!/bin/sh

redis-server &
cd /var/www/fluigicad.org/
npm start app.js
