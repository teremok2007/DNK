#!/bin/sh
PRJ=$(pwd)

export PATH="$PRJ/bin/node-v13.1.0-linux-x64/bin/:$PATH"

node app.js
