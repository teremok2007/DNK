#!/bin/sh
DNK=$(pwd)

export PATH="$DNK/bin/node-v13.1.0-linux-x64/bin/:$PATH"

node app.js
